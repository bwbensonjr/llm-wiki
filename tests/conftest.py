"""Shared test doubles for the capture/localization tests.

`FakeSession` stands in for a `requests` session so tests never hit the network.
It dispatches by URL: `head` answers the content-type probe, `get` answers both
the Jina endpoint (returning Markdown text) and image downloads (returning bytes
or raising for designated failure URLs).
"""

import pytest
import requests

from wiki_ingest.convert import JINA_ENDPOINT


class FakeResponse:
    def __init__(self, *, text="", content=b"", headers=None, status_code=200):
        self.text = text
        self.content = content
        self.headers = headers or {}
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"status {self.status_code}")

    def close(self):
        pass


class FakeSession:
    def __init__(
        self,
        *,
        content_type="text/html",
        jina_markdown="",
        images=None,
        fail_urls=None,
        image_content_type="image/png",
    ):
        self.content_type = content_type
        self.jina_markdown = jina_markdown
        self.images = images or {}
        self.fail_urls = set(fail_urls or [])
        self.image_content_type = image_content_type

    def head(self, url, **kwargs):
        return FakeResponse(headers={"content-type": self.content_type})

    def get(self, url, **kwargs):
        if url in self.fail_urls:
            raise requests.ConnectionError(f"refused: {url}")
        if url.startswith(JINA_ENDPOINT):
            return FakeResponse(text=self.jina_markdown)
        if url in self.images:
            return FakeResponse(
                content=self.images[url],
                headers={"content-type": self.image_content_type},
            )
        return FakeResponse(status_code=404)


@pytest.fixture
def png_bytes():
    """A payload comfortably above MIN_IMAGE_BYTES so it is kept."""
    return b"\x89PNG\r\n\x1a\n" + b"0" * 6000
