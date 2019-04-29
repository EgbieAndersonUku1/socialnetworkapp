import time
from uuid import uuid4
import datetime
import arrow
import bleach


def linkify_text(text):
    """"""
    text = bleach.clean(text, tags=[], attributes={}, styles=[], strip=True)
    return bleach.linkify(text)


def ms_stamp_humanize(time_stamp):

    ts = datetime.datetime.fromtimestamp(int(time_stamp)/1000)
    return arrow.get(ts).humanize()


def time_stamp():
    return int(time.time())


def utc_time_stamp_mill_seconds():
    return lambda: int(round(time.time() * 1000))


def gen_code():
    return str(uuid4())