
import pandas as pd
from datetime import datetime, timedelta
from isoweek import Week


dateToday= datetime.now()
day_of_week=dateToday.weekday()+1
weekstarting =dateToday - timedelta(days=day_of_week)

weekending =dateToday + timedelta(days=6 - day_of_week)
last7days= dateToday - timedelta(days=7)
prevDays= dateToday- timedelta(days=1)

weekstart = weekstarting.strftime("%b %d, %Y")
weekend=weekending.strftime("%b %d, %Y")

weekstartShortLbl = weekstarting.strftime("%b %d")
weekendShortLbl=weekending.strftime("%b %d")
weekFormatShort = str(weekstartShortLbl) +' - '+ str(weekendShortLbl)

last7daysFrmt= last7days.strftime("%b %d")
dateTodayFrmt=prevDays.strftime("%b %d")

print(datetime.now()- timedelta(days=1))
print(dateToday - timedelta(days=7))
print(str(last7daysFrmt), str(dateTodayFrmt))


