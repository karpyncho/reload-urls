"""
Author: Sebastian Quiles
Based on:
https://stackoverflow.com/questions/45173272/django-pytest-test-url-based-on-settings
"""
import sys
from importlib import import_module, reload
from types import TracebackType
from typing import Optional

from django.conf import settings as django_settings  # type: ignore
from django.test import TestCase  # type: ignore
from django.test.testcases import override_settings  # type: ignore
from django.urls import clear_url_caches  # type: ignore


class ReloadUrlsContextManager:
    """
    Context Manager cLass ReloadUrlsContextManager

    This class manages both context at the same time.
    + change a setting in django settings
    + reload the urls after changing the settings

    when the context finishes
    + first it dispose the setting context
    + and then the urls are reloaded again
    """
    @staticmethod
    def _reload_urlconf(urlconf: Optional[str] = None) -> None:
        """
        this internal procedure does the reload

        :param urlconf: if None, it will reload url file specified in settings.ROOT_URLCONF,
                        if is a str, it is the namespace of the url module to be reloaded
        """
        clear_url_caches()
        if urlconf is None:
            urlconf = django_settings.ROOT_URLCONF
        if urlconf in sys.modules:
            reload(sys.modules[urlconf])
        else:
            import_module(urlconf)

    def __init__(self, url_module: Optional[str],
                 test_case_instance: TestCase,
                 **settings: object) -> None:
        """
        Constructor of ReloadUrlsContextManager

        :param url_module: string of the module to be reloaded, if None the module specified in settings.ROOT_URLCONF
        will be reloaded
        :param test_case_instance: TestCase instance, used to call the setting method (override_settings
        context manager)
        :param settings: keyword params to be packed in settings variable, each parameter has the aspect:
        DJANGO_SETTING_TO_BE_OVERRIDE="new value for this setting"
        """
        self.settings_context_instance = None
        self.override_settings_context = test_case_instance.settings
        self.url_module = url_module
        self.settings = settings

    def __enter__(self) -> override_settings:
        """
        this method creates the override_settings passing the unpacked settings kwargs and his __enter_() magic method
        is called, this context is stored in an instance variable to be used in __exit__() method and dispose the
        context.

        after creating and entering the settings context manager, the _reload_urlconf method is called

        :return: the function return the override_settings context
        """
        self.settings_context_instance = self.override_settings_context(**self.settings)
        if self.settings_context_instance:
            self.settings_context_instance.__enter__()
        ReloadUrlsContextManager._reload_urlconf(self.url_module)
        return self.settings_context_instance

    def __exit__(self,
                 exc_type: Optional[type],  # type is subscriptable since python 3.9, correct annotation should be
                                            # Optional[Type[BaseException]]
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        if self.settings_context_instance:
            self.settings_context_instance.__exit__(exc_type, exc_val, exc_tb)
        ReloadUrlsContextManager._reload_urlconf()


class TestCaseReloadableURL(TestCase):
    """
    TestCaseReloadableURL is the class to be used in tests classes as inheritance instead of traditional
    Django TestCase.
    """
    def reload_urls(self, url_module: Optional[str], **settings: object) -> ReloadUrlsContextManager:
        """
        A class that inherits from TestCaseReloadableURL can use a context like:
        with self.reload_urls("module.urls", SETTING="new value"):
            sentence_1
            sentence_2

        Within the context block, the setting will be changed (just as self.settings()) but the urls routing will
        be reloaded.

        After the context is disposed, the settings will return to be the defined in DJANGO_SETTINGS_MODULE and
        the url routing will be reloaded again.

        :param url_module: string of the module to be reloaded, if None the module specified in settings.ROOT_URLCONF
        will be reloaded
        :param settings: keyword params, each parameter has the aspect:
        DJANGO_SETTING_TO_BE_OVERRIDE="new value for this setting"
        :return: a Context Manager
        """
        return ReloadUrlsContextManager(url_module, self, **settings)
