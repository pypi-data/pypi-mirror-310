"""A `requests.HTTPAdapter` that understands Pelican URIs.
"""

from __future__ import annotations

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import logging
import sys
from typing import (
    Any,
    Union,
)

import requests
import requests.utils
from requests.adapters import HTTPAdapter
from scitokens import SciToken
from urllib3.exceptions import MaxRetryError
from urllib3.util import parse_url

from .auth import scitoken_auth
from .director import (
    DirectorResponse,
    get_director_response,
)
from .federation import federation_url
from .pelican import pelican_uri

log = logging.getLogger(__name__)

TimeoutType = Union[float, tuple[float, float], tuple[float, None], None]


class PelicanAdapter(HTTPAdapter):
    """`HTTPAdapter` for Pelican federation URLs.

    This adapter handles accessing and caching the redirect links that
    the Pelican director supplies for each namespace, to transform a
    Pelican federation URI into an HTTP(S) URL.
    """
    def __init__(
        self,
        federation: str | None = None,
        max_retries: int = 3,
        **kwargs,
    ):
        super().__init__(
            max_retries=max_retries,
            **kwargs,
        )
        self.federation: str | None = None
        if federation:
            self.federation = federation_url(federation)

    @staticmethod
    def _scitoken_auth(
        request: requests.PreparedRequest,
        director: DirectorResponse,
        token: str | None = None,
        issuers: list[str] = [],
    ):
        return scitoken_auth(
            request,
            director,
            token=token,
            issuers=issuers,
        )

    def _resolve_requests(
        self,
        request: requests.PreparedRequest,
        federation: str | None = None,
        token: SciToken | None = None,
        timeout: TimeoutType = 60,
        **kwargs,
    ):
        """Query the Pelican federation director for URLs that could serve us.
        """
        # parse the Pelican federation information
        uri = parse_url(pelican_uri(
            request.url,
            federation=federation or self.federation,
        ))
        # and query the director for information about this namespace
        director = get_director_response(
            str(uri),
            adapter=super(),
            request=request,
            timeout=timeout,
            **kwargs,
        )

        # if request didn't come with its own auth header, and the
        # director tells us we need a token, try and find one now
        if (
            "Authorization" not in request.headers
            and director.namespace["require-token"]
        ):
            auth = self._scitoken_auth(
                request,
                director,
                token=token,
            )
        else:
            auth = None

        # construct a request for each URL we got from the director
        for url in director.urls(uri.path):
            req = request.copy()
            req.url = url
            req.prepare_auth(auth)
            yield req

    def send(
        self,
        request: requests.PreparedRequest,
        stream: bool = False,
        timeout: TimeoutType = 60,
        verify: bool | str = True,
        cert: Any = None,
        proxies: Any = None,
        federation: str | None = None,
    ):
        """Send a request using this adapter.

        This will loop over the Pelican cache URLs in an attempt to download
        the requested URI.
        """
        if timeout is None:
            timeout = 60
        retries = self.max_retries
        responses = []
        error = None
        reqs = list(self._resolve_requests(
            request,
            federation=federation,
            timeout=timeout,
            verify=True,
            cert=cert,
            proxies=proxies,
        ))
        log.debug(
            f"Identified {len(reqs)} endpoints for {request.url}, "
            f"will attempt at most {retries.total}",
        )
        for req in reqs:
            try:
                resp = super().send(
                    req,
                    stream=stream,
                    timeout=timeout,
                    verify=verify,
                    cert=cert,
                    proxies=proxies,
                )
            except requests.ConnectionError as exc:
                if error is None:
                    error = exc
                retries = retries.increment(
                    request.method,
                    request.url,
                    error=exc,
                    _stacktrace=sys.exc_info()[2],
                )
                log.debug(
                    "Connection error from {request.url}, moving to next target",
                )
                continue
            responses.append(resp)
            if resp.status_code >= 400:
                try:
                    retries = retries.increment(
                        method=request.method,
                        url=request.url,
                        response=resp.raw,
                    )
                except MaxRetryError:
                    break
                continue
            else:
                break

        # if we got out response
        if responses:
            # attach history of our attempts
            r = responses.pop(-1)
            r.history = responses + r.history
            return r

        # if we identified an error, use that
        if error:
            raise error
        # otherwise panic
        raise RuntimeError("No responses received, but no error identified")
