import json
from datetime import datetime

eventsCommand = {
    ('productive','-p'):'productive',
    ('waste','-w'):'waste'
} #dict holding the keywords for events to be called from command

Events = {
    'productive':['break','distracted','restrained'],
    'waste':[]
} #dict holding relevant properties of Events, namely the Incidents that can happen during the span of event

incidentsCommand = {
    ('break','-b'): 'break',
    ('distracted','-d'): 'distracted',
    ('restrained','-r'): 'restrained'
} #dict holding the keywords for incidents to be called from command

Incidents = {
    'break': {'count':0,'time':0},
    'distracted': {'count':0,'time':0},
    'restrained': {'count':0}
} #dict holding the properties of the incidents that can be changed during the whole course of an event

def findEvent(command):
    """Find the corresponding event from the keyword in command"""
    for keywords in eventsCommand:
        #get the tuple representing keywords from the eventsCommand dict, for iteration in the next for loop
        for keyword in keywords:
            #loop through each tuple of keywords, make a if check to see if this is the required event
            if keyword in command:
                return eventsCommand[keywords]
    else:
        return -1

def startEvent(event):
    now = datetime.now()
    status = 'ongoing'
    event = event
    date = now.timetuple()[0:3]
    startTime = round(now.timestamp())
    currentIncident = None
    incidents = {}
    data = {
        'status': status,
        'event': event,
        'date': date,
        'startTime': startTime,
        'currentIncident': currentIncident,
        'incidents': incidents
    }

    for incident in Events[event]:
        #pointing to the incidents allowed for this event
        data['incidents'][incident] = Incidents[incident]

    return data

def endEvent(data):
    if data['status'] == 'interrupted':
        #End the current incident first before ending the event as a whole
        data = endIncident(data)
    elif data['status'] != 'ongoing':
        raise Exception('Wrong Status, required: interrupted or ongoing')

    data['status'] = 'finished'
    timespan = round(datetime.now().timestamp()) - data['startTime']
    for incidentType in data['incidents'].values():
        #This for loop removes the time for interruptions from the timespan for the event
        if 'time' in incidentType:
            #check if the incident have the time attribute
            timespan -= incidentType['time']
    data['timespan'] = timespan
    return data

def findIncident(command):
    """Find the corresponding incident from the keyword in command"""
    for keywords in incidentsCommand:
        #get the tuple representing keywords from the eventsCommand dict, for iteration in the next for loop
        for keyword in keywords:
            #loop through each tuple of keywords, make a if check to see if this is the required event
            if keyword in command:
                return incidentsCommand[keywords]
    else:
        return -1

def startIncident(data, incident):
    if not incident in data['incidents']:
        #check if incident is present in the dict of incidents that the event can have
        print('The current event does not accept incident' + incident)
        return -1

    if 'time' in Incidents[incident]:
        data['status'] = 'interrupted'
        data['currentIncident'] = {
            'incident': incident,
            'startTime': round(datetime.now().timestamp())
        }

    if 'count' in Incidents[incident]:
        data['incidents'][incident]['count'] += 1

    return data

def endIncident(data):
    """function that takes in the data and end an Incident (must be an incident that cause interrupted status)"""
    if data['status'] != 'interrupted':
        raise Exception ('Wrong Status, required: interrupted')
    endedIncident = data['currentIncident']['incident'] #from the currentIncident, find the incident about to end
    timespan = round(datetime.now().timestamp()) - data['currentIncident']['startTime'] #The timespan of the incident
    data['incidents'][endedIncident]['time'] += timespan
    data['status'] = 'ongoing'
    data['currentIncident'] = None
    return data

def main(filepath, command):
    successRun = False
    try:
        with open(filepath,'r') as fileread:
            data = json.load(fileread)
    except FileNotFoundError:
        data = {'status':'idle'}
    # Try-except handles the first time using the script, creating a new focus cache

    if data['status'] == 'idle':
        # When during idle, looks for a new event to be added
        event = findEvent(command)
        if event != -1:
            data = startEvent(event)
            successRun = True
        else:
            print('The current state is idle, awaiting a new event input, but a correct event is not received')

    elif data['status'] == 'ongoing':
        # When during ongoing, looks for a new incident or to end the event
        if 'end' in command:
            data = endEvent(data)
            successRun = True
        else:
            incident = findIncident(command)
            if incident != -1:
                data = startIncident(data, incident)
                successRun = True
            else:
                print('The current state is ongoing, awaiting a new incident input or end current event, but a correct command is not received')

    elif data['status'] == 'interrupted':
        if 'end' in command:
            data = endEvent(data)
            successRun = True
        elif 'resume' in command:
            data = endIncident(data)
            successRun = True
        else:
            print('The current state is interrupted, waiting to return to ongoing or just to end the event')

    if successRun:
        with open(filepath,'w') as filewrite:
            json.dump(data, filewrite)
    else:
        if input('Re-enter? (y/n) ') == 'y':
            command = input("Your command: ")
            main(filepath, command)

if __name__ == '__main__':
    command = input('input: focus + ')
    main('focus.json',command)