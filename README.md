# Karpyncho Reload-Urls

[![PyPI version](https://badge.fury.io/py/karpyncho-reload-urls.svg)](https://badge.fury.io/py/karpyncho-reload-urls)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/karpyncho-reload-urls.svg)](https://pypi.python.org/pypi/karpyncho-reload-urls/)
[![check](https://github.com/tox-dev/tox-gh/actions/workflows/check.yml/badge.svg)](https://github.com/tox-dev/tox-gh/actions/workflows/check.yml)
[![codecov](https://codecov.io/gh/karpyncho/reload-urls/branch/main/graph/badge.svg?token=M4IT5AXE88)](https://codecov.io/gh/karpyncho/reload-urls)
## Goal

> This package main goal is to extend unittest to have a context manager that can change a setting 
> and then reload the django urls routing.

> Without this package if a url.py file that defines the urlpatterns to be using by the django 
> routing module have a conditional url like:

```python
if setting.DEBUG:
    urlpatterns += [url("home", my_home_view, name="home")]
```

> this routing will be loaded only once in the pytest suit, and depending on the django_settings_module file 
> configuration, the routing will be loaded with (or without) the optional url.
> If in a test method, self.settings(DEBUG=True) is used the routing will not be reloaded

> With this package you can inherit from karpyncho.reload_urls.ReloadUrlsContextManager and then use the method
> self.reload_url(url_module, settings) within a context. When the context is freed, first the setting is removed, 
> and then the urls are reloaded again

> For example:

```python
from django.urls import reverse, NoReverseMatch

from karpyncho.reload_urls import TestCaseReloadableURL


class TestExample(TestCaseReloadableURL):
    def test_example(self):
        with self.reload_urls(None, ADD_HELLO_URL=True):
            self.client.get(reverse("home"))
        with self.assertRaises(NoReverseMatch):
            reverse("home")
```

### reload_url method

> this method is added to the class django.tests.TestCase, the paramters are:
> + urls_module: a string with the specific app url module to be reloaded (ie: "my_app.urls"). If None, 
> the url module definen in settings.ROOT_URLCONF is reloaded
> + **settings: the keywords parameters, each key is the setting to be overriden, just as the 
> with self.settings(**settings) works
## Install

```sh
pip install karpyncho_reload_urls
```

https://pypi.org/project/karpyncho-reload-urls/

## Future improvements

 * Fix potential bugs