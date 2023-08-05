"""Preconditions module."""
from typing import Optional

from ..decorators import given
from .base_request import BaseRequest


class Preconditions(BaseRequest):
    """Precondition methods."""

    def __init__(
        self,
        method: Optional[str] = None,
        endpoint: Optional[str] = None
    ):
        super().__init__(method, endpoint)

    @given
    def to(self, endpoint, **kwargs):
        """Set endpoint to request."""
        self.endpoint = endpoint
        if kwargs:
            self.endpoint = self.endpoint.format(**kwargs)

    @given
    def with_method(self, method):
        """Set HTTP request method."""
        self.method = method

    @given
    def with_body(self, body):
        """Set request Content-Type: appliaction/json body."""
        self.body = body

    @given
    def with_headers(self, headers):
        """Set request header or headers."""
        self.headers = headers

    @given
    def with_params(self, params):
        """Set request query parameters."""
        self.params = params
