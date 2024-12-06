"""Session wrappers for Pelican.
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

from requests import (
    Session as _Session,
)

from .adapters import PelicanAdapter
from .federation import KNOWN_FEDERATIONS
from .utils import default_user_agent


class SessionMixin:
    """`requests.Session` mixin to mount adapters for Pelican URIs.
    """
    def __init__(  # type: ignore
        self: _Session,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)  # type: ignore
        self.headers["User-Agent"] = default_user_agent()
        self.mount("pelican://", PelicanAdapter())
        for fed in KNOWN_FEDERATIONS:  # mount them all
            self.mount(f"{fed}://", PelicanAdapter(fed))


class Session(SessionMixin, _Session):
    """`requests.Session` that understands Pelican URIs.
    """
