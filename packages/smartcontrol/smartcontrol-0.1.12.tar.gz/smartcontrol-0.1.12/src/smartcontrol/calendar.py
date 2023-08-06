from enum import Enum
import typing
from typing import Coroutine, Generator
import time, datetime


class Details(Enum):
    HOURS = 1


class Language(Enum):
    FR = 1
    EN = 2


def get_tommorrow():
    return datetime.date.today() + datetime.timedelta(days=1)


def date_range_day(
    start_date: datetime.datetime, end_date: datetime.datetime, step: int = 1
) -> Generator:
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def numbers_days_between(
    start: datetime.datetime, end: datetime.datetime, week_day: int
) -> int:
    num_weeks, remainder = divmod((end - start).days, 7)
    if (week_day - start.weekday()) % 7 <= remainder:
        return num_weeks + 1
    else:
        return num_weeks


def delta_time_from_now(hour, date=None):
    def add_date_to_hour(hour, date):
        hour = datetime.strptime(hour, "%H:%M:%S.%f")
        target = hour.replace(year=date.year, month=date.month, day=date.day)

        return target

    def format_in_milisec(format):
        if len(re.findall(r"\d{1,2}:\d{1,2}:\d{1,2}", format)) < 1:
            return format + ":00.00"
        if len(re.findall(r"\.[0-9]+$", format)) < 1:
            return format + ".00"
        return format

    def is_contain_date(format):
        return len(re.findall(r"[0-9]{1,2}/[0-9]{1,2}/[0-9]+", format)) > 0

    now = time.time()
    hour = format_in_milisec(hour)
    if is_contain_date(hour):

        date_time_obj = datetime.strptime(hour, "%d/%m/%Y %H:%M:%S.%f")
        target = date_time_obj.timestamp()

    else:
        if type(date) == str:
            date = datetime.strptime(date, "%d/%m/%Y")

        date_time_obj = add_date_to_hour(hour, date)

        target = date_time_obj.timestamp()

    return target - now


def get_slots(
    amount: int,
    step: int = 1,
    start: datetime.datetime or typing.List[datetime.datetime] = get_tommorrow(),
    end: datetime.datetime or typing.List[datetime.datetime] = None,
    details: Details = None,
    language: Language = Language.FR,
) -> str:

    days = []
    if end:
        functional_days = (
            (end - start).days
            - numbers_days_between(start, end, 5)
            - numbers_days_between(start, end, 6)
        )
    else:
        end = start + datetime.timedelta(amount)
        end2 = end + datetime.timedelta(2 * numbers_days_between(start, end, 5))
        end = end + datetime.timedelta(2 * numbers_days_between(start, end2, 5))
        for date in date_range_day(start, end):
            if date.weekday() not in (5, 6):
                days.append(date)
    addition = ""
    if details is not None:
        if details == Details.HOURS:
            addition = " de 10:00 à 12:00 et de 14:00 à 17:00"
        else:
            addition = ""
    slots = "Le " + days[0].strftime("%d/%m") + addition
    for i in range(1, len(days) - 1):
        slots += ", le " + days[i].strftime("%d/%m") + addition
    if (n := len(days)) > 1:
        slots += ", et le " + days[n - 1].strftime("%d/%m") + addition
    return slots
