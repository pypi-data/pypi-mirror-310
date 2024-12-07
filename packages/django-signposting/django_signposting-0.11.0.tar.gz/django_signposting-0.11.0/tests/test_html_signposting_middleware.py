from bs4 import BeautifulSoup
from django.http import HttpResponse, JsonResponse
from django_signposting.middleware import HtmlSignpostingMiddleware
from signposting import LinkRel, Signpost
import pytest


def assert_links_exist(response: HttpResponse, signposts: list[Signpost] = None):
    if signposts is None:
        signposts = response._signposts

    soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
    for signpost in signposts:
        links = soup.find_all("link", href=signpost.target, rel=signpost.rel)
        assert len(links) == 1

    assert len(soup.find_all("link")) == len(signposts)


def test_middleware_no_signposting():
    response = HttpResponse("<html><head></head><body></body></html>")
    response.status_code = 200

    middleware = HtmlSignpostingMiddleware(lambda request: response)
    response = middleware(None)

    assert_links_exist(response, [])


def test_middleware_no_html():
    response = JsonResponse({"hello": "world"})
    response.status_code = 200
    response._signpost = [Signpost(LinkRel.author, "http://example.com")]

    middleware = HtmlSignpostingMiddleware(lambda request: response)
    middleware(None)
    assert_links_exist(response, [])


def test_middleware_malformed_html():
    response = HttpResponse("Hello world")
    response.status_code = 200
    response.content_type = "text/html"
    response._signposts = [Signpost(LinkRel.author, "http://example.com")]

    middleware = HtmlSignpostingMiddleware(lambda request: response)
    with pytest.raises(Exception):
        middleware(None)


def test_middleware_signposting_without_head():
    response = HttpResponse("<html><body></body></html>")
    response.status_code = 200
    response._signposts = [Signpost(LinkRel.author, "http://example.com")]

    middleware = HtmlSignpostingMiddleware(lambda request: response)
    middleware(None)
    assert_links_exist(response)


def test_middleware_signposting():
    response = HttpResponse("<html><head></head><body></body></html>")
    response.status_code = 200
    response._signposts = [Signpost(LinkRel.author, "http://example.com")]

    middleware = HtmlSignpostingMiddleware(lambda request: response)
    middleware(None)
    assert_links_exist(response)


def test_middleware_multiple_signposts():
    response = HttpResponse("<html><head></head><body></body></html>")
    response.status_code = 200
    response._signposts = [
        Signpost(LinkRel.author, "http://example.com"),
        Signpost(LinkRel.author, "http://example2.com"),
        Signpost(LinkRel.cite_as, "http://example3.com"),
    ]

    middleware = HtmlSignpostingMiddleware(lambda request: response)
    response = middleware(None)
    assert_links_exist(response)


def test_middleware_signpost_with_content_type():
    response = HttpResponse("<html><head></head><body></body></html>")
    response.status_code = 200
    response._signposts = [Signpost(LinkRel.item, "http://example.com", "text/json")]

    middleware = HtmlSignpostingMiddleware(lambda request: response)
    response = middleware(None)
    assert_links_exist(response)


def test_middleware_ignore_error_responses():
    response = HttpResponse("<html><head></head><body></body></html>")
    response.status_code = 400
    response._signposts = [Signpost(LinkRel.author, "http://example.com")]

    middleware = HtmlSignpostingMiddleware(lambda request: response)
    response = middleware(None)
    assert_links_exist(response)


def test_middleware_type_link():
    response = HttpResponse("<html><head></head><body></body></html>")
    response.status_code = 200
    response._signposts = [Signpost(LinkRel.type, "http://schema.org/Dataset")]

    middleware = HtmlSignpostingMiddleware(lambda request: response)
    response = middleware(None)
    assert_links_exist(response)
