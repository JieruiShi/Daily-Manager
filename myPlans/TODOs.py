import json
import re
import datetime

def addTODOS(filepath, haveFlags = False):
    """this function gives hints to help create new TODO objects"""
    with open(filepath,'r') as fileread:
        data = json.load(fileread)

    def findEndTime(timeinput):
        """returns endtime in timestamp through considering 4 separate situations"""

        pattern1 = r"d|(hrs)"
        pattern2 = r'\d\.\d'
        pattern3 = r'(Jan)|(Feb)|(Mar)|(Apr)|(May)|(Jun)|(July)|(Aug)|(Sep)|(Oct)|(Nov)|(Dec)'
        pattern4 = r"\d/\d"
        logTime = round(datetime.datetime.timestamp(datetime.datetime.now()))

        if re.search(pattern3, timeinput):
            # eg: Oct 14
            months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'July': 7, 'Aug': 8, 'Sep': 9,
                      'Oct': 10, 'Nov': 11, 'Dec': 12}

            digitpos = re.search(r'\d', timeinput).span()[0]
            d = int(timeinput[digitpos:])
            m = months[timeinput[0:digitpos].strip()]
            today = datetime.datetime.now()
            if m < today.month or (m == today.month and d < today.day):
                y = today.year + 1
            else:
                y = today.year
            return datetime.datetime(y, m, d).timestamp() + 86400

        elif re.search(pattern4, timeinput):
            #eg: 10/14
            slashpos = timeinput.find('/')
            m = int(timeinput[0:slashpos])
            d = int(timeinput[(slashpos + 1):])
            today = datetime.datetime.now()
            if m < today.month or (m == today.month and d < today.day):
                y = today.year + 1
            else:
                y = today.year
            return datetime.datetime(y,m,d).timestamp() + 86400

        elif re.search(pattern1,timeinput):
            #eg: 1d 14hrs
            dpos = timeinput.find('d')
            hpos = timeinput.find('h')
            if dpos != -1:
                d = int(timeinput[0:dpos])
                if hpos != -1:
                    h = int(timeinput[(dpos + 1):hpos])
                else:
                    h = 0
            else:
                d = 0
                h = int(timeinput[0:hpos])
            return logTime + d * 86400 + h * 3600

        elif re.search(pattern2,timeinput):
            #eg: 1.14
            dotpos = timeinput.find('.')
            d = int(timeinput[0:dotpos])
            h = int(timeinput[(dotpos + 1):])
            return logTime + d * 86400 + h * 3600

        else:
            return 'time not defined'

    def addflags():
        """returns a list of flags with their progress count"""
        flags = []
        empties = 0  # record the flags not assigned with a percentage
        progressSum = 0  # record the current sum of assigned percentage
        index = 1

        while True:
            progressCount = 0

            flaginput = input('flag ' + str(index) + ' > ')
            if flaginput:
                search = re.search(r'\d', flaginput)
                # searches for digits (assigned percentage)
                if search:
                    digitpos = search.span()[0]
                    progressCount = int(flaginput[digitpos:].strip())
                    flagContent = flaginput[:digitpos].strip()
                    progressSum += progressCount
                else:
                    empties += 1
                    flagContent = flaginput.strip()

            else:
                break
            flags.append({'name': flagContent, 'progressCount': progressCount, 'done': False})
            index += 1

        if empties != 0:
            progressLeft = (100 - progressSum) / empties
            for flag in flags:
                if not flag['progressCount']:
                    flag['progressCount'] = progressLeft

        return flags

    while True:
        name = input('TODO name: ')
        time = input(
            'input timespan(in day & hours) or due date\n---timespan eg: 1d 14hrs / 1.14\n---due date eg: Oct 14 / 10/14\n')
        category = input('TODO Category:')
        if haveFlags:
            flags = addflags()
        else:
            flags = []
        data.append({
            'name': name,
            'logTime': round(datetime.datetime.timestamp(datetime.datetime.now())),
            'endTime': findEndTime(time),
            'category': category,
            'flags': flags
        })

        sortedData = sorted(data, key = lambda datum: datum['endTime'])
        #sort the data each time it is added
        if input('add more(y/n)') != 'y':
            break

    with open(filepath, 'w') as filewrite:
        json.dump(sortedData, filewrite)

def showTODOS(filepath):
    with open(filepath, 'r') as fileread:
        data = json.load(fileread)

    maxDistance = 100
    #TODO:maxDistance is to be determined by the length of the longest task
    #print title
    print(' ' * (maxDistance + 5) + 'Due Date' + ' ' * 6 + 'Time Left' + ' ' * 4 + 'Progress')

    for index, datum in enumerate(data):
        #name of TODO
        print (str(index + 1) + '.' + datum['category'] + '---' + datum['name'] + ' ' * (maxDistance - len(datum['category']) - len(datum['name']) - len(str(index + 1))), end = '')
        DH = publicstuff.timestampToDH(datum['endTime'] - datetime.datetime.timestamp(datetime.datetime.now()))
        #time left & deadline
        if DH[0] >= 0:
            print (datetime.datetime.fromtimestamp(datum['endTime']).strftime('%m/%d %H:%M'), end = '   ')
            print (str(DH[0]) + 'd ' + str(DH[1]) + 'hrs' + (5 - len(str(DH[0])) - len(str(DH[1]))) * ' ', end = '  ')
        else:
            print ('⚠ OVERDUE ⚠' + ' ' * 15, end = '')

        #progress made:
        progressMade = sum([flag['progressCount'] for flag in datum['flags'] if flag['done']])
        print (publicstuff.progressBar(progressMade) + str(progressMade) + '%')

def tickTODOS(filepath,filepath2,taskno, exitStatus):
    with open(filepath,'r') as fileread:
        data = json.load(fileread)

    with open(filepath2, 'r') as fileread:
        data2 = json.load(fileread)

    popDatum = data.pop(taskno)
    with open(filepath, 'w') as filewrite:
        json.dump(data,filewrite)

    popDatum['exitStatus'] = exitStatus
    popDatum['exitTime'] = round(datetime.datetime.timestamp(datetime.datetime.now()))

    data2.append(popDatum)

    with open(filepath2, 'w') as filewrite:
        json.dump(data2,filewrite)
    print('task "' + popDatum['name'] + '" is ticked successfully')

def main(filepath, filepath2):
    showTODOS(filepath)
    completed = False
    while not completed:
        choice = input('---add [+f for adding flagged TODOs]\n---list\n---t [+ tick option](+ task number) to tick a finished TODO options:a--abandoned c--cancelled default--finished\n---end\n---input index to see details or update\n')
        if 'add' in choice:
            if 'f' in choice:
                addTODOS(filepath, haveFlags = True)
            addTODOS(filepath)

        elif 'list' in choice:
            showTODOS(filepath)
        elif choice == 'end':
            completed = True
        elif choice[0] == 't':
            #TODO: check if out of range and taskno is legit
            if choice[1] == 'a':
                #task abandoned
                exitStatus = 'abandoned'
                taskno = int(choice[2:]) - 1
            elif choice[1] == 'c':
                #task cancelled
                exitStatus = 'cancelled'
                taskno = int(choice[2:]) - 1
            else:
                #default success
                taskno = int(choice[1:]) - 1
                exitStatus = 'finished'
            tickTODOS(filepath,filepath2,taskno,exitStatus)
        else:
            pass
if __name__ == '__main__':
    from myscripts import publicstuff, config
    main(config.ACTIVE_FILEPATH,config.ARCHIEVE_FILEPATH)
else:
    import publicstuff
