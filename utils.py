from datetime import datetime, timedelta

def weekendDate():
    dateToday= datetime.now()
    day_of_week=dateToday.weekday()+1
    last7days= dateToday - timedelta(days=7)
    prevDays= dateToday- timedelta(days=1)

    last7daysFrmt= last7days.strftime("%b %d")
    dateTodayFrmt=prevDays.strftime("%b %d")

    weekFormatShort = str(last7daysFrmt) +' - '+ str(dateTodayFrmt)
    return weekFormatShort