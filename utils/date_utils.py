"""
Created by anthony on 07.12.2017
date_utils
"""
from datetime import datetime, timedelta, date
from random import randrange
from time import strftime, gmtime, time
import time


def random_date(start, end):
    """
    This function will return a random datetime between two datetime objects.
    https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def parse_date_msg(basedate):
    data_len = None
    if list == type(basedate):
        data_len = len(basedate)

    else:
        basedate = basedate.split()
        data_len = len(basedate)

    parsed = None
    if 0 == data_len or basedate is None:
        raise ValueError('Empty data provided!')

    elif 1 == data_len:
        # parse for time only. get nearest date with this time
        t = basedate[0]

        t_hour, t_minutes = recognize_time(t)

        date_line = f'{date.today().day} {date.today().month} {date.today().year} {t_hour}:{t_minutes}'
        parsed = datetime.strptime(date_line, "%d %m %Y %H:%M")
        if parsed < datetime.now():
            date_line = f'{date.today().day + 1} {date.today().month} {date.today().year} {t_hour}:{t_minutes}'

        parsed = datetime.strptime(date_line, "%d %m %Y %H:%M")
        return parsed

    elif 2 == data_len:
        # parse for day and time within current month
        day = int(basedate[0])
        t = basedate[1]

        if 1 <= day <= 31:

            t_hour, t_minutes = recognize_time(t)

            date_line = f'{day} {date.today().month} {date.today().year} {t_hour}:{t_minutes}'
            parsed = datetime.strptime(date_line, "%d %m %Y %H:%M")

            if parsed < datetime.now():
                try:
                    date_line = f'{day} {date.today().month + 1} {date.today().year} {t_hour}:{t_minutes}'
                    parsed = datetime.strptime(date_line, "%d %m %Y %H:%M")

                except ValueError:
                    date_line = f'{day} {1} {date.today().year + 1} {t_hour}:{t_minutes}'
                    parsed = datetime.strptime(date_line, "%d %m %Y %H:%M")
            return parsed

        else:
            raise ValueError(f'Could not recognize day in: {basedate}')

    elif 3 == data_len:
        # parse for the whole date
        day = int(basedate[0])
        month = basedate[1]
        t = basedate[2]

        months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
        month_eng = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        month_prefix = month[0: 3]  # декабрь ->дек, дек -> дек
        if month_prefix in months or month_prefix in month_eng:
            month_ordinal = None
            if month_prefix in months:
                month_ordinal = str(months.index(month_prefix) + 1)

            elif month_prefix in month_eng:
                month_ordinal = str(month_eng.index(month_prefix) + 1)

            else:
                raise ValueError(f'Could not recognize month in: {basedate}')

            if len(month_ordinal) < 2:
                month_ordinal = '0' + month_ordinal

            if 1 <= day <= 31:

                t_hour, t_minutes = recognize_time(t)

                date_line = f'{day} {month_ordinal} {date.today().year} {t_hour}:{t_minutes}'
                parsed = datetime.strptime(date_line, "%d %m %Y %H:%M")
                if parsed < datetime.now():
                    try:
                        date_line = f'{day} {date.today().month + 1} {date.today().year} {t_hour}:{t_minutes}'
                        parsed = datetime.strptime(date_line, "%d %m %Y %H:%M")

                    except ValueError:
                        date_line = f'{day} {1} {date.today().year + 1} {t_hour}:{t_minutes}'
                        parsed = datetime.strptime(date_line, "%d %m %Y %H:%M")

                    if parsed < datetime.now():
                        date_line = f'{day} {date.today().month} {date.today().year + 1} {t_hour}:{t_minutes}'

                parsed = datetime.strptime(date_line, "%d %m %Y %H:%M")
                return parsed

        else:
            raise ValueError(f'Could not recognize month in: {basedate}')

    else:
        raise ValueError('Too much data provided')


def recognize_time(time_string):
    if '-' in time_string or '.' in time_string or ':' in time_string:
        time_string = time_string.replace('-', ':').replace('.', ':')
        hour = time_string[:time_string.index(':')]
        if 1 == len(hour):
            hour += '0'

        minutes = time_string[time_string.index(':') + 1:]
        return hour, minutes

    elif 3 == len(time_string):
        hour = '0' + time_string[0]
        minutes = time_string[1:]
        return hour, minutes

    elif 4 == len(time_string):
        hour = time_string[:2]
        minutes = time_string[2:]
        return hour, minutes

    else:
        raise ValueError(f'Could not recognize time in: {time_string}')


def current_time():
    return strftime("%H:%M %d-%m-%Y", gmtime())


# decorator from lecture
def add_timestamp(func):
    def inner_func(text_arg):
        ret = func(f'{text_arg} ...sent on {current_time()}')
        return ret

    return inner_func


def log_duration(func):
    def inner_func(*args):
        start_time = time()
        ret = func(args)

        print(f'execution time: {time() - start_time} seconds')
        return ret

    return inner_func


def seconds_between_tasks(task1, task2):
    return (task1.get_next_remind_date() - task2.get_next_remind_date()).total_seconds()


def readable_datetime(datetime_to_parse):
    if datetime_to_parse is None:
        return '-'

    else:
        # from_zone = tz.tzutc()
        # utc = datetime_to_parse.replace(tzinfo=from_zone)
        # to_zone = tz.tzlocal()
        # local = utc.astimezone(to_zone)
        formatted = datetime.strftime(datetime_to_parse, "%d %b %H:%M")
        return formatted
