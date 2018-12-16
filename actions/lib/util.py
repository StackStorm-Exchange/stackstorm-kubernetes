from datetime import date, datetime


# pylint: disable=too-few-public-methods

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        serial = obj.isoformat()
        return serial
    if isinstance(obj, object):
        return {k.lstrip('_'): v for k, v in vars(obj).items()}
    raise TypeError("Type %s not serializable" % type(obj))
