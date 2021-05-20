from datetime import datetime, timedelta

class CalendarEventManager:
    def __init__(self):
        self.events = []
    def addEvent(self, event):
        self.events.append(event)
    def getEvents(self):
        return self.events

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
    '''def containsImportant(self):
        if len(self.getEvents()) == 0:
            return False
        for x in self.getEvents():
            if x.getType() == 'bg-danger':
                return True
        return False
    def containsInfo(self):
        if len(self.getEvents()) == 0:
            return False
        for x in self.getEvents():
            if x.getType() == 'bg-info':
                return True
        return False'''
    def addEvent(self, x):
        self.events.append(x)
    def buildUserEvents(self, user):
        userEvents = []
        
        hour = 6
        minute = 30
        added = False
        for x in range(21):
            for event in self.manager.getEvents():
                if event.getUser() == user:
                    if event.getDay().strftime('%Y-%B-%d') == self.fullDateString:
                        if event.getTime() == '{:02d}:{:02d}'.format(hour, minute):
                            userEvents.append('<span class="cal_dot" style="background-color: blue;"></span>')
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
                userEvents.append('')
        return userEvents

class ArmyCalendar:
    def __init__(self):
        self.fullDate = datetime.today()
        self.manager = CalendarEventManager()
    def getMonth(self):
        return self.fullDate.strftime('%B')
    def setMonthYear(self, month, year):
        self.fullDate = datetime.strptime('{0}-{1}-1', '%Y-%M-%d')
    def getYear(self):
        return self.fullDate.year
    def addEvent(self, evt):
        self.manager.addEvent(evt)
    def createCalendar(self):
        # Create an empty list to populate down below
        calendarDays = []
        
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
        # ---- DEBUG ----
        # Setting my days to refer to as I code the calendar out
        # May 2021
        # prevDays = 6
        # lastPrevDay = 30
        # ---- DEBUG ----
        
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
        calendarDays.extend(reversedDays)
        
        # Quick one-liner to get the end of the current months day (number)
        endDay = ((startDay + timedelta(days=32)).replace(day=1) - timedelta(days=1))
        
        # Each calender will hold 42 days. For a nice looking block. Subtract the length of currently added days AND the remaining days to add
        remaindingDays = 42-len(calendarDays)-endDay.day
        daysToAdd = 42 - len(calendarDays) - remaindingDays
        
        # Append all the days up to the last day as non-muted blocks
        day = 1
        while daysToAdd > 0:
            calendarDays.append(ArmyCalendarDay(self.manager, startDay.replace(day=day).strftime('%Y-%B-%d'), startDay.replace(day=day).strftime('%A'), day, False))
            day += 1
            daysToAdd -= 1
        
        # Append all the remainder of the 42 days as muted blocks
        endDay = endDay + timedelta(days=1)
        nextMonthDay = 1
        while remaindingDays > 0:
            calendarDays.append(ArmyCalendarDay(self.manager, endDay.replace(day=nextMonthDay).strftime('%Y-%B-%d'), endDay.replace(day=nextMonthDay).strftime('%A'), nextMonthDay, True))
            nextMonthDay += 1
            remaindingDays -= 1
        
        # Return the fully created month calendar
        return calendarDays