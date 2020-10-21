import math

def progressBar(progressPercentage, tot = 10):
    done = round((progressPercentage/100) * tot)
    return '|' + done * '■' + (tot - done) * '□' + '|'

def timestampToDH(timestamp):
    """note: floor is used instead of round"""
    hours = math.floor(timestamp / 3600) % 24
    days = math.floor(timestamp / 86400)
    return [days,hours]

def _test():
    print ('demo of progress bar with progressPercentage = 56,tot = 15')
    print (progressBar(56,15) + '56% done')
    print ('demo of timestamp to day hour converter with timestamp = 100000')
    print (timestampToDH(100000), ' = 1d 4hrs')

if __name__ == '__main__':
    _test()