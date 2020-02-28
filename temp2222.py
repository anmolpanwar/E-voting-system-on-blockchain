import pdb
number = int(input())
dates = []
for i in range(number):
    dates.append(input())

years = [int(dates[i].split()[2]) for i in range(len(dates))]
years.sort()
years = list(dict.fromkeys(years))


def year(date):
    return int(date[7:])

Mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
months = {}
for i in range(len(years)):
    months[years[i]] = []

dates.sort(key= year)
# for i in range(len(dates)-1):
#     for j in range(1,len(dates)):
#         if int(dates[i][7:])==int(dates[j][7:]):

for i in range(len(years)):
    for j in range(len(dates)):
        if years[i] == int(dates[j][7:]):
            print("here")
            months[years[i]].append(dates[i][3:6])
pdb.set_trace()
