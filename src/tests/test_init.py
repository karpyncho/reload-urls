from karpyncho.reload_urls import TestCaseReloadableURL


class TestTestCaseReloadableURL(TestCaseReloadableURL):
    def test_reload_urls(self):
        tc = TestCaseReloadableURL()
        with tc.reload_urls(None, MY_SETTING="My setting"):
            pass
