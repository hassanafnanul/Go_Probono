import datetime, pytz
from django.utils import timezone


def datetimepicker_to_datetime(mmddyyyyhhmm):
    arr = mmddyyyyhhmm.split('/')
    year = int(arr[0])
    month = int(arr[1])
    temp = arr[2].split(' ')
    day = int(temp[0])
    ret = [day, year, month]
    temp2 = temp[1].split(':')
    ret.append(int(temp2[0]))
    ret.append(int(temp2[1]))
    if temp[2] == 'PM':
        ret[3] += 12
    return datetime(ret[0], ret[1], ret[2], ret[3], ret[4])

def datetime_to_datetimepicker(utctime):
    fmt = '%m/%d/%Y %H:%M %p'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz.strftime(fmt)

def datetime_local_to_datetime(yyyymmddhhmm):
    ret = yyyymmddhhmm.split('T')
    ret[0] = ret[0].split('-')
    ret[1] = ret[1].split(':')
    return datetime.datetime(int(ret[0][0]), int(ret[0][1]), int(ret[0][2]), int(ret[1][0]), int(ret[1][1]))

def datetime_to_datetime_local(utctime):
    fmt = '%Y-%m-%dT%H:%M'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz.strftime(fmt)

