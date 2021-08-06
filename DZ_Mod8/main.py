from datetime import datetime, date, timedelta


users = [{'name':'Vlad', 'birthday':date(year=1991, month=8, day=9)},
         {'name':'John', 'birthday':date(year=1990, month=8, day=10)},
         {'name':'Alina', 'birthday':date(year=1990, month=8, day=9)},
         {'name':'Lena', 'birthday':date(year=1990, month=8, day=7)},
         {'name':'Stas', 'birthday':date(year=1990, month=8, day=8)},
         {'name':'Igor', 'birthday':date(year=1990, month=8, day=12)},
         {'name':'Святополк', 'birthday':date(year=1990, month=7, day=9)}]


def congratulate(users):
    current_date = datetime.now().date()
    next_week_monday = current_date - timedelta(days=current_date.weekday()) + timedelta(weeks=1)
    cong = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[]}
    for user in users:
        if current_date.month == user['birthday'].month:
            if user['birthday'].day in [next_week_monday.day, next_week_monday.day-1, next_week_monday.day-2]:
                cong['Monday'].append(user['name'])
            elif user['birthday'].day == next_week_monday.day + 1:
                cong['Tuesday'].append(user['name'])
            elif user['birthday'].day == next_week_monday.day + 2:
                cong['Wednesday'].append(user['name'])
            elif user['birthday'].day == next_week_monday.day + 3:
                cong['Thursday'].append(user['name'])
            elif user['birthday'].day == next_week_monday.day + 4:
                cong['Friday'].append(user['name'])
    for day in cong:
        if len(cong[day]) > 0:
            a = ', '.join(cong[day])
            print(f'{day}: {a}')

congratulate(users)
