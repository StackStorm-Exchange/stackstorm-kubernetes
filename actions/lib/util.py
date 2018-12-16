from datetime import date, datetime

# pylint: disable=too-few-public-methods


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type %s not serializable" % type(obj))
