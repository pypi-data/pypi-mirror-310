"""Authorisation utilities for requests_pelican.
"""

from __future__ import annotations

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import logging

import requests

from .director import DirectorResponse

log = logging.getLogger(__name__)


def scitoken_auth(
    request: requests.PreparedRequest,
    namespace: DirectorResponse,
    token: str | None = None,
    issuers: list[str] = [],
):
    log.debug(
        "Configuring HTTPSciTokenAuth for namespace "
        f"'{namespace.namespace}'",
    )
    try:
        from requests_scitokens import HTTPSciTokenAuth
    except ImportError as exc:
        log.debug(
            f"Failed to import HTTPSciTokenAuth ({exc})",
        )
        return

    auth = HTTPSciTokenAuth(token=token)
    if token is None:
        auth.token = auth.find_token(
            request.url,
            error=False,
        )
    if auth.token is None:
        log.debug(
            "Failed to find SciToken for namespace "
            f"'{namespace.namespace}'",
        )
    return auth
