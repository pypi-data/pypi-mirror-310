import logging
from pathlib import Path

from decouple import AutoConfig, Choices

from bitvavo_api_upgraded.type_aliases import ms

# don't use/import python-decouple's `config`` variable, because the search_path isn't set,
# which means applications that use a .env file can't override these variables :(
config = AutoConfig(search_path=Path.cwd())


class _BitvavoApiUpgraded:
    # default LOG_LEVEL is WARNING, so users don't get their ass spammed.
    LOG_LEVEL: str = config(
        "BITVAVO_API_UPGRADED_LOG_LEVEL",
        default="INFO",
        cast=Choices(list(logging._nameToLevel.keys())),  # noqa: SLF001
    )
    LOG_EXTERNAL_LEVEL: str = config(
        "BITVAVO_API_UPGRADED_EXTERNAL_LOG_LEVEL",
        default="WARNING",
        cast=Choices(list(logging._nameToLevel.keys())),  # noqa: SLF001
    )
    LAG: ms = config("BITVAVO_API_UPGRADED_LAG", default=ms(50), cast=ms)
    RATE_LIMITING_BUFFER: int = config("BITVAVO_API_UPGRADED_RATE_LIMITING_BUFFER", default=25, cast=int)


class _Bitvavo:
    """
    Changeable variables are handled by the decouple lib, anything else is just static, because they are based on
    Bitvavo's documentation and thus should not be able to be set outside of the application.
    """

    ACCESSWINDOW: int = config("BITVAVO_ACCESSWINDOW", default=10_000, cast=int)
    API_RATING_LIMIT_PER_MINUTE: int = 1000
    API_RATING_LIMIT_PER_SECOND: float = API_RATING_LIMIT_PER_MINUTE / 60
    APIKEY: str = config("BITVAVO_APIKEY", default="BITVAVO_APIKEY is missing")
    APISECRET: str = config("BITVAVO_APISECRET", default="BITVAVO_APISECRET is missing")
    DEBUGGING: bool = config("BITVAVO_DEBUGGING", default=False, cast=bool)
    RESTURL: str = "https://api.bitvavo.com/v2"
    WSURL: str = "wss://ws.bitvavo.com/v2/"


# Just import these variables to use the settings :)
BITVAVO_API_UPGRADED = _BitvavoApiUpgraded()
BITVAVO = _Bitvavo()
