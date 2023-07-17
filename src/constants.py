from charlogger import Logger
import json

logger = Logger(
    debug=True,
    default_prefix="[Bank]",
    color_text=True,
)

logger.info("Loading configuration")
config: dict = json.loads(open("config.json").read())

logger.info("Parsing configuration")
logger.info(config)

prefix: str = config.get("prefix")
currency_symbol: str = config.get("currency_symbol")
admins: list = config.get("admins")
income_delay_in_seconds: int = config.get("income_delay_in_seconds")
work_delay_in_seconds: int = config.get("work_delay_in_seconds")


embed_color = 0x5bcefa
embed_green = 0x57f287
embed_red = 0xed4245

x_emoji = "<:x_:1129945309305393232>"
check_emoji = "<:check:1129945323888984215>"