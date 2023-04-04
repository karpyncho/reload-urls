from django.urls import reverse, NoReverseMatch

from karpyncho.reload_urls import TestCaseReloadableURL


class TestTestCaseReloadableURL(TestCaseReloadableURL):
    def test_reload_urls(self):
        with self.reload_urls("tests.urls", ADD_HELLO_URL=True):
            self.client.get(reverse("hello"))
        with self.assertRaises(NoReverseMatch):
            reverse("hello")
    def test_reload_urls_by_root_urlconf(self):
        with self.reload_urls(None, ADD_HELLO_URL=True):
            self.client.get(reverse("hello"))
        with self.assertRaises(NoReverseMatch):
            reverse("hello")

    def test_not_hellow_if_not_reload(self):
        with self.settings(ADD_HELLO_URL=True):
            with self.assertRaises(NoReverseMatch):
                reverse("hello")

    def test_reload_another_urls(self):
        tc = TestCaseReloadableURL()
        with tc.reload_urls("tests.another_urls", ADD_HELLO_URL=True):
            self.client.get(reverse("another_hello"))
        with self.assertRaises(NoReverseMatch):
            reverse("another_hello")

    def test_not_another_hellow_if_not_reload(self):
        with self.settings(ADD_HELLO_URL=True):
            with self.assertRaises(NoReverseMatch):
                reverse("hello")
