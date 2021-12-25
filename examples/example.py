from pydantic import BaseSettings

from confjector import inject


class Params(BaseSettings):
    first: int
    second: str
    third: bool


@inject(conf_path="conf/config.yml")
def main(params: Params) -> None:
    print(params)
    assert params.first == 1
    assert params.second == "asd"
    assert params.third


if __name__ == "__main__":
    main()
