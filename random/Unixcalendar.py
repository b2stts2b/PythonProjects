import sys 
def printCal():	
	print(f"{currentYear:^66}")
	for j in range(0, 12, 3):
		print(f"{months[j]:^22}{months[j+1]:^22}{months[j+2]:^22}")
		print("  ".join(" ".join(week for week in weeks) for i in range(3)))
		for i in range(6):
			print(" ".join([f"{num:>2}" for num in dates[months[j]][i]]), end = "  ")
			print(" ".join([f"{num:>2}" for num in dates[months[j+1]][i]]), end= "  ")
			print(" ".join([f"{num:>2}" for num in dates[months[j+2]][i]]))

def isLeapYear(year):
	if year % 4 == 0:
		if year % 100 == 0:
			if year % 400 == 0:
				return True
			return False
		return True
	return False

months = ["January", "February", "March", "April", "May", "June",
		  "July", "August", "September", "October", "November", "December"]
weeks = ["Su", "Mo", "Tu", "We", "Th", "Fr" ,"Sa"]
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
dates = {}

for index in range(len(months)):
	dates[months[index]] = []
	for week in range(6):
		dates[months[index]].append(list(map(str, range(week*7+1, week*7+8))))

currentYear = int(sys.argv[1])
weekday = 1
for year in range(1, currentYear):
	daysInYear = 366 if isLeapYear(year) else 365 
	weekday = (weekday+daysInYear%7)%7
	
if isLeapYear(year):
	days[1] = 29
else:
	days[1] = 28

for monthIndex, month in enumerate(months):
	dates[month] = []
	firstweek = 7-weekday
	for i in range(6):
		week = [" " for day in range(weekday)]
		if i == 0:
			week.extend(list(map(str, range(1, firstweek+1))))
			weekday = 0
		else:
			day = min(days[monthIndex]-firstweek-7*(i-1), 7)
			day = max(day, 0)
			weekStart = firstweek+7*(i-1)+1
			week.extend(list(map(str, range(weekStart, weekStart+day))))
			week.extend([" " for left in range(7-len(week))])
			weekday = (weekday+day)%7
		dates[month].append(week)

printCal()