from datetime import date

from db.operations import simple_select
from db.db import conn, cur

week_day = {'понедельник': range(0, 5),
            'вторник': range(5, 10),
            'среда': range(10, 15),
            'четверг': range(15, 20),
            'пятница': range(20, 25),
            'суббота': range(25, 30)}


days = ['Понедельник (ОП)',
        'Вторник (Мотор)',
        'Среда (Мотор)',
        'Четверг (ОП)',
        'Пятница (ОП)',
        'Суббота']

days_with_spaces = [f'{day}' for day in days]

time = ['| 09:30-11:05 |', '| 11:20-12:55 |', '| 13:10-14:45 |', '| 15:25-17:00 |', '| 17:15-18:50 |']


def timetable(message):
    message_array = message.split(' ')
    delta = delta_func()

    # запрос в базу данных
    nech = simple_select(conn, cur, select_what=['class_name'], select_from='timetable', where="week = 'неч'")
    ch = simple_select(conn, cur, select_what=['class_name'], select_from='timetable', where="week = 'чет'")

    week_type = {'чет': ch, 'нечет': nech}

    try:
        # расписание
        if len(message_array) == 1 and message_array[0] == '/расписание':
            rasp = ch if (delta // 7) % 2 != 0 else nech
            day = []
            for r in range(0, 30):
                day.append(rasp[r])

            text = rasp_with_time(day, 6)
            return text
        # расписание на день недели
        elif len(message_array) == 1 and message_array[0] != '/р':
            arg = message_array[0][1:].lower()
            day = []
            rasp = ch if (delta // 7) % 2 != 0 else nech
            for r in week_day[arg]:
                day.append(rasp[r])

            text = rasp_with_time(day, 1)
            return text

        elif len(message_array) == 2:
            arg = message_array[1]
            if arg in week_day:

                day = []
                rasp = ch if (delta // 7) % 2 != 0 else nech
                for r in week_day[arg]:
                    day.append(rasp[r])

                text = rasp_with_time(day, 1)
                return text

            elif arg in week_type:
                rasp = week_type[arg]

                day = []
                for r in range(0, 30):
                    day.append(rasp[r])

                text = rasp_with_time(day, 6, nofw=False)
                return text

    except KeyError:
        text = 'Ошибка'
        return text
    except BaseException as e:
        print(e)
        text = 'Ошибка'
        return text


def rasp_with_time(pr, mn, nofw=True):

    if nofw:
        delta = delta_func()
        week_number = (delta // 7) + 1
        week = f'Четная неделя ({week_number})' if (delta // 7) % 2 != 0 else f'Нечетная неделя ({week_number})'

        text = f'{week}\n'
    else:
        text = ''

    for i, item in enumerate(time * mn):
        if i % 5 == 0 and mn > 1:
            text = text + days_with_spaces[i//5] + '\n'
        if pr[i] != None:
            text = text + str(item) + ' ' + pr[i] + '\n'
    return text



def delta_func():
    first_day = date(2021, 8, 30)
    today = date.today()
    delta = (today - first_day).days
    # today = datetime.datetime.today().strftime("%W")
    return delta