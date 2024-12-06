"""Python Requests wrappers for `requests_pelican`.
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

from functools import wraps as _wraps

import requests.api

from . import sessions


@_wraps(requests.request)
def request(method, url, *args, session=None, **kwargs):
    """Send a Pelican request.

    Parameters
    ----------
    method : `str`
        The method to use.

    url : `str`,
        The URL to request.

    session : `requests.Session`, optional
        The connection session to use, if not given one will be
        created on-the-fly.

    args, kwargs
        All other keyword arguments are passed directly to
        `requests.Session.request`

    Returns
    -------
    resp : `requests.Response`
        the response object

    See also
    --------
    igwn_auth_utils.requests.Session.request
        for information on how the request is performed
    """
    # user's session
    if session:
        return sessions.Session.request(
            session,
            url,
            *args,
            **kwargs,
        )
        return session.request(method, url, *args, **kwargs)

    # new session
    with sessions.Session() as sess:
        return sess.request(method, url, *args, **kwargs)


def _request_wrapper_factory(method):
    """Factor function to wrap a :mod:`requests` HTTP method to use
    our request function.
    """
    @_wraps(getattr(requests.api, method))
    def _request_wrapper(url, *args, session=None, **kwargs):
        return request(method, url, *args, session=session, **kwargs)

    _request_wrapper.__doc__ += f"""
    See also
    --------
    `requests.{method}`
        The upstream function of which this is a wrapper.
    """  # type: ignore

    return _request_wrapper


# request methods
delete = _request_wrapper_factory("delete")
get = _request_wrapper_factory("get")
head = _request_wrapper_factory("head")
patch = _request_wrapper_factory("patch")
post = _request_wrapper_factory("post")
put = _request_wrapper_factory("put")
