import base64
from datetime import datetime


def timestamp2str(stamp: float) -> str:
    return datetime.fromtimestamp(stamp).strftime("%Y-%m-%d %H:%M:%S")

def float2percent(rate: float) -> str:
    return format(rate, ".1%")

def base64transform(text: str) -> str:
    return base64.b64encode(text.encode("utf8")).decode("utf8")
