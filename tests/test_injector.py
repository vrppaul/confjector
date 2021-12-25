from unittest import mock

from pydantic import BaseSettings

from confjector import inject, parser


class Params(BaseSettings):
    first: int
    second: str
    third: bool


FAKE_PARSED_DATA = {
    "first": "1",
    "second": "text",
    "third": "true"
}


def test_parser():
    with mock.patch("confjector.parser._parse_file_to_dict", return_value=FAKE_PARSED_DATA):
        data = parser.parse(Params, "some.yml")

    assert isinstance(data, BaseSettings)
    assert data.first == 1
    assert data.second == "text"
    assert data.third