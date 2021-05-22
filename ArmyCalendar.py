from datetime import datetime, timedelta
from flask import redirect

class CalendarEventManager:
    def __init__(self):
        self.events = []
    def addEvent(self, event):
        self.events.append(event)
    def getEvents(self):
        return self.events

class UserCalendarDayEvent:
    def __init__(self):
        self.Str = []
    def __repr__(self):
        return str(self.Str)
    def addHTMLString(self, strToAdd):
        self.Str.append(strToAdd)
    def getHTMLString(self):
        return self.Str

class CalendarEvent:
    def __init__(self, user, evt_number, title, description, cal_type, day, time, stop_day, stop_time):
        self.evt_number = evt_number
        self.title = title
        self.description = description
        self.cal_type = cal_type
        self.time = time
        self.day = day
        self.user = user
        self.stop_day = stop_day
        self.stop_time = stop_time
    def getUser(self):
        return self.user
    def getEventNumber(self):
        return self.evt_number
    def getTitle(self):
        return self.title
    def getDesc(self):
        return self.description
    def getType(self):
        return self.cal_type
    def getDay(self):
        return self.day
    def getTime(self):
        return self.time
    def getStopTime(self):
        return self.stop_time
    def getStopDay(self):
        return self.stop_day

class ArmyCalendarDay:
    def __init__(self, manager, fullDateString, dayName, day, muted):
        self.manager = manager
        self.fullDateString = fullDateString
        self.day = day
        self.muted = muted
        self.dayName = dayName
    def isMuted(self):
        return self.muted
    def getfullDateString(self):
        return self.fullDateString
    def getDay(self):
        return self.day
    def getName(self):
        return self.dayName
    def addEvent(self, x):
        self.events.append(x)
    def buildUserEvents(self, user):
        userEvents = []
        
        for event in self.manager.getEvents():
            dayDate = datetime.strptime('{0} 00:00:00'.format(self.fullDateString), '%Y-%B-%d %H:%M:%S')
            eventStartDate = datetime.strptime('{0}'.format(event.getDay()), '%Y-%m-%d %H:%M:%S')
            eventStopDate = datetime.strptime('{0}'.format(event.getStopDay()), '%Y-%m-%d %H:%M:%S')
            
            # Check if dates are within range
            if eventStopDate >= dayDate or dayDate >= eventStartDate:
                if event.getUser() == user:
                    hour = 6
                    minute = 30
                    added = False
                    htmlString = UserCalendarDayEvent()
                    for x in range(21):
                        # Get each date that the program will need to figure out checks
                        dayTime = dayDate.replace(hour=hour, minute=minute)
                        
                        # Be inclusive for both start and end date
                        if eventStopDate >= dayTime or dayTime >= eventStartDate:
                            # Format the startDate and endDate to get their time for comparring
                            eventStartTime = eventStartDate.replace(hour=int(event.getTime().split(':')[0]), minute=int(event.getTime().split(':')[1]))
                            eventStopTime = eventStopDate.replace(hour=int(event.getStopTime().split(':')[0]), minute=int(event.getStopTime().split(':')[1]))
                            
                            # The stop date/time is exlusive and the start time is inclusive
                            if eventStopTime > dayTime and dayTime >= eventStartTime:
                                htmlString.addHTMLString('<span class="cal_dot" data-bs-toggle="tooltip" data-bs-placement="top" title="' + event.getTitle() + '" style="background-color: ' + event.getType() + ';"></span>')
                                added = True
                        
                        if minute == 30:
                            hour += 1
                            minute = 0
                        else:
                            minute = 30
                        
                        if added:
                            added = False
                            continue
                        else:
                            htmlString.addHTMLString('<span class="cal_dot"></span>')
                    userEvents.append(htmlString)
        
        masterDay = []
        for x in range(21):
            masterDay.append('')
        
        for evt in userEvents:
            for x in range(len(evt.getHTMLString())):
                masterDay[x] = '{0}{1}'.format(masterDay[x], evt.getHTMLString()[x])
        return masterDay

class ArmyCalendar:
    def __init__(self, database):
        self.fullDate = datetime.today()
        self.manager = CalendarEventManager()
        self.calendarDays = []
        self.database = database
    def getMonth(self):
        return self.fullDate.strftime('%B')
    def setMonthYear(self, month, year):
        self.fullDate = datetime.strptime('{0}-{1}-1', '%Y-%M-%d')
    def getYear(self):
        return self.fullDate.year
    def addEvent(self, evt):
        self.manager.addEvent(evt)
    def getCalendarDays(self):
        return self.calendarDays
    def getPreviousDay(self, date):
        day = datetime.strptime(date, '%Y-%B-%d') - timedelta(days=1)
        return day.strftime('%Y-%B-%d')
    def getNextDay(self, date):
        day = datetime.strptime(date, '%Y-%B-%d') + timedelta(days=1)
        return day.strftime('%Y-%B-%d')
    def buildDayFor(self, fulldate, user):
        for days in self.calendarDays:
            if fulldate == days.getfullDateString():
                return days.buildUserEvents(user)
    def createCalendar(self):
        # Reset the calendar
        self.calendarDays = []
    
        # Get all days to compare them to the first day of current month
        weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        
        # Get the start of current months day (number) as well as the end of previous months day (number)
        startDay = datetime.today().replace(day=1)
        lastPrevDay = startDay - timedelta(days=1)
        #lastPrevDay = lastPrevDay.day
        
        # See how far into the week the start of the month is
        prevDays = 0
        for days in weekdays:
            if startDay.strftime('%A') == days:
                break
            prevDays += 1
        
        # Create a new empty array to populate with the previous months days to add to this months as a muted block
        daysToAdd = []
        
        # Get the last day and begin to countdown the days until its Sunday on the calendar
        x = 0
        while prevDays > 0:
            daysToAdd.append(ArmyCalendarDay(self.manager, (lastPrevDay - timedelta(days=x)).strftime('%Y-%B-%d'), weekdays[x], (lastPrevDay - timedelta(days=x)).day, True))
            x += 1
            prevDays -= 1
        
        # daysToAdd.reverse() was returning None for some reason, hot fix until I figure that out
        reversedDays = daysToAdd[::-1]
        
        # Add the muted days to the list
        self.calendarDays.extend(reversedDays)
        
        # Quick one-liner to get the end of the current months day (number)
        endDay = ((startDay + timedelta(days=32)).replace(day=1) - timedelta(days=1))
        
        # Each calender will hold 42 days. For a nice looking block. Subtract the length of currently added days AND the remaining days to add
        remaindingDays = 42-len(self.calendarDays)-endDay.day
        daysToAdd = 42 - len(self.calendarDays) - remaindingDays
        
        # Append all the days up to the last day as non-muted blocks
        day = 1
        while daysToAdd > 0:
            self.calendarDays.append(ArmyCalendarDay(self.manager, startDay.replace(day=day).strftime('%Y-%B-%d'), startDay.replace(day=day).strftime('%A'), day, False))
            day += 1
            daysToAdd -= 1
        
        # Append all the remainder of the 42 days as muted blocks
        endDay = endDay + timedelta(days=1)
        nextMonthDay = 1
        while remaindingDays > 0:
            self.calendarDays.append(ArmyCalendarDay(self.manager, endDay.replace(day=nextMonthDay).strftime('%Y-%B-%d'), endDay.replace(day=nextMonthDay).strftime('%A'), nextMonthDay, True))
            nextMonthDay += 1
            remaindingDays -= 1
        
        # Return the fully created month calendar
        return self.calendarDays