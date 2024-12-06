"""Tests for `requests_pelican.adapters`.
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

from requests_pelican import adapters as rp_adapters


class TestPelicanAdapter:
    Adapter = rp_adapters.PelicanAdapter

    def test_init(self):
        adapter = self.Adapter()
        assert adapter.federation is None

    def test_init_federation(self):
        adapter = self.Adapter(federation="osdf")
        assert adapter.federation == "osg-htc.org"

    # I don't know how to test our custom adapter using requests-mock,
    # see https://github.com/jamielennox/requests-mock/issues/83 for
    # a brief discussion of the problem.
    #
    # Real, internet-facing tests are performed in test_integration.py.
