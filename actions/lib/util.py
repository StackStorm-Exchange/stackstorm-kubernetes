from datetime import date, datetime


# pylint: disable=too-few-public-methods

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        serial = obj.isoformat()
        return serial
    elif isinstance(obj, (int, long, float, complex, bool, str, unicode, basestring)):
        return obj
    elif isinstance(obj, object):
        return {k.lstrip('_'): v for k, v in vars(obj).items()}
    raise TypeError("Type %s not serializable" % type(obj))
