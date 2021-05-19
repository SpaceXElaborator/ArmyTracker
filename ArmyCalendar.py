from datetime import datetime, timedelta

class CalendarEvent:
    def __init__(self, evt_number, title, description, cal_type):
        self.evt_number = evt_number
        self.title = title
        self.description = description
        self.cal_type = cal_type
    def getEventNumber(self):
        return self.evt_number
    def getTitle(self):
        return self.title
    def getDesc(self):
        return self.description
    def getType(self):
        return self.cal_type

class ArmyCalendarDay:
    def __init__(self, fullDateString, dayName, day, muted):
        self.fullDateString = fullDateString
        self.day = day
        self.muted = muted
        self.dayName = dayName
        self.events = []
    def isMuted(self):
        return self.muted
    def getfullDateString(self):
        return self.fullDateString
    def getDay(self):
        return self.day
    def getName(self):
        return self.dayName
    def getEvents(self):
        return self.events
    def containsImportant(self):
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
        return False
    def addEvent(self, x):
        self.events.append(x)

class ArmyCalendar:
    def __init__(self):
        self.fullDate = datetime.today()
    def getMonth(self):
        return self.fullDate.strftime('%B')
    def getYear(self):
        return self.fullDate.year
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
            daysToAdd.append(ArmyCalendarDay((lastPrevDay - timedelta(days=x)).strftime('%Y-%B-%d'), weekdays[x], (lastPrevDay - timedelta(days=x)).day, True))
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
            calendarDays.append(ArmyCalendarDay(startDay.replace(day=day).strftime('%Y-%B-%d'), startDay.replace(day=day).strftime('%A'), day, False))
            day += 1
            daysToAdd -= 1
        
        # Append all the remainder of the 42 days as muted blocks
        endDay = endDay + timedelta(days=1)
        nextMonthDay = 1
        while remaindingDays > 0:
            calendarDays.append(ArmyCalendarDay(endDay.replace(day=nextMonthDay).strftime('%Y-%B-%d'), endDay.replace(day=nextMonthDay).strftime('%A'), nextMonthDay, True))
            nextMonthDay += 1
            remaindingDays -= 1
        
        # ---- DEBUG ----
        # calendarDays[2].addEvent(CalendarEvent(len(calendarDays[2].getEvents()) + 1, 'Test{0}'.format(2), 'Test Description', 'bg-info'))
        # ---- DEBUG ----
        
        # Return the fully created month calendar
        return calendarDays