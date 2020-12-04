import math
from datetime import datetime
import numbers

def progressBar(progressPercentage, tot = 10):
    done = round((progressPercentage/100) * tot)
    return '|' + done * '■' + (tot - done) * '□' + '|'

def timestampToDH(timestamp):
    """note: floor is used instead of round"""
    hours = math.floor(timestamp / 3600) % 24
    days = math.floor(timestamp / 86400)
    return [days,hours]

def relativeTimestamp(*timeObj):
    """return relative timestamp (to the start of the day). When there is no input, the value is returned for now.
    Can take one numeric input(timestamp) or one datetime data type inputs"""
    if not timeObj:
        timeStamp = datetime.timestamp(datetime.now())
    elif isinstance(timeObj[0], datetime):
        timeStamp = datetime.timestamp(timeObj[0])
    elif isinstance(timeObj[0], numbers.Complex):
        timeStamp = timeObj[0]
    else:
        raise TypeError ('Wrong value type for relativeTimestamp function')
    return timeStamp % 86400

def _test():
    print ('demo of progressBar: \nprogressBar(56,15)')
    print (progressBar(56,15))
    print ('demo of timestamp to day hour converter: \ntimestampToDH(100000)')
    print (timestampToDH(100000), ' (= 1d 4hrs)')
    print('demo of relative timestamp (0 at 0:00) :')
    print('relativeTimestamp() ', relativeTimestamp())
    print('relativeTimestamp(datetime.now()) ', relativeTimestamp(datetime.now()))
    print('relativeTimestamp(500000) ', relativeTimestamp(500000))

if __name__ == '__main__':
    _test()