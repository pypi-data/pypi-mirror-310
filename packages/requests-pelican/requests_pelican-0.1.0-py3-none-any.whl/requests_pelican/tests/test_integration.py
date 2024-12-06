"""End-to-end integration tests for `requests_pelican`.
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import pytest
import requests

import requests_pelican


def _skip_exception(exc):
    return pytest.skip("caught {type(exc).__name__)}: {exc}")


@pytest.mark.remote_data
def test_osdf_gwdata_readme():
    """Test a real round-trip with `requests_pelican.Session`.

    This test talks to the internet, so has some default protections to
    redirect to `pytest.skip` on transient errors.
    """
    with requests_pelican.Session() as sess:
        # requests_session.Session auto-mounts the osdf:// adapter
        try:
            resp = sess.get("osdf:///gwdata/zenodo/README.zenodo")
            resp.raise_for_status()
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as exc:
            _skip_exception(exc)
        except requests.exceptions.HTTPError as exc:
            if exc.response.status_code >= 500:
                _skip_exception(exc)
            raise
    # assert that we got the real thing
    assert resp.text.startswith("## Mirror of IGWN Zenodo Communities")
