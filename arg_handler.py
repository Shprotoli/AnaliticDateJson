from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from annotations import JsonNoParseDate
from parse import ParseTimeSlotInfo, ParserDayInfo


def generate_json_date(json):
    parse_days = ParserDayInfo().parse_day(json)
    json_date = next(parse_days)
    json_date_to_id = next(parse_days)

    parse_slot = ParseTimeSlotInfo().parse_slot(json, json_date)

    return json_date_to_id, parse_slot


def generate_json_day(json):
    parse_days = ParserDayInfo().parse_day(json)
    json_date = next(parse_days)
    json_date_to_id = next(parse_days)

    return json_date_to_id, json_date


class ArgumentHandler(ABC):
    @abstractmethod
    def handler(self, *args):
        ...


class BusyTimeHandler(ArgumentHandler):
    """
    Класс для обработки режима работы `busy` (Найти все занятые промежутки для указанной даты)
    """
    def handler(self, json: JsonNoParseDate, date_find: str):
        json_date_to_id, parse_slot = generate_json_date(json)

        if date_find in json_date_to_id:
            print(f"Все занятые промежутки для {date_find}")

            id_date = json_date_to_id[date_find]
            for start, end in parse_slot[id_date]:
                start_date, start_time = start.date(), start.time()
                end_date, end_time = end.date(), end.time()

                print(
                    f"Начало:\t {start_date} {start_time}\n"
                    f"Конец:\t {end_date} {end_time}\n"
                )
        else:
            print(f"Для даты {date_find}, просмотр не доступен")


class FreeTimeHandler(ArgumentHandler):
    """
    Класс для обработки режима работы `free` (Найти свободное время для заданной даты)
    """
    def handler(self, json: JsonNoParseDate, date_find: str):
        json_date_to_id, json_date = generate_json_day(json)
        _, parse_slot = generate_json_date(json)

        if date_find in json_date_to_id:
            id_date = json_date_to_id[date_find]

            start_day, end_day = json_date[id_date]
            start_time = start_day

            print(f"Свободное время для {date_find}:")

            sorted_parse_slot = sorted(parse_slot[id_date], key=lambda x: x[0])
            for start_slot, end_slot in sorted_parse_slot:
                if start_time < start_slot:
                    print(f"С:\t{start_time.time()}\nДо:\t{start_slot.time()}\n")
                start_time = end_slot
            print(f"С:\t{start_time.time()}\nДо:\t{end_day.time()}")
        else:
            print(f"Для даты {date_find}, просмотр не доступен")


class CheckTimeHandler(ArgumentHandler):
    """
    Класс для обработки режима работы `check` (Вывести доступен ли заданный промежуток времени для заданной даты)
    """
    def handler(self, json: JsonNoParseDate, date_find: str, time_find: str):
        json_date_to_id, json_date = generate_json_day(json)
        _, parse_slot = generate_json_date(json)

        if date_find in json_date_to_id:
            id_date = json_date_to_id[date_find]

            start_day, end_day = json_date[id_date]

            find_start = datetime.strptime(f"{date_find} {time_find.split()[0]}", "%Y-%m-%d %H:%M")
            find_end = datetime.strptime(f"{date_find} {time_find.split()[1]}", "%Y-%m-%d %H:%M")

            if start_day > find_start:
                print("Начальное время не может быть меньше, чем начальное время в графике")
                return

            if end_day < find_end:
                print("Конечное время не может быть больше, чем конечное время в графике")
                return

            for slot_start, slot_end in parse_slot[id_date]:
                if not (find_end <= slot_start or find_start >= slot_end):
                    print("Время занято.")
                    return
            print(f"Время: {find_start.time()} - {find_end.time()}\nДля даты: {find_end.date()}, свободно!")

        else:
            print(f"Для даты {date_find}, просмотр не доступен")


class DurationTimeHandler(ArgumentHandler):
    """
    Класс для обработки режима работы `free` (Найти свободное время для заданной даты)
    """
    def handler(self, json: JsonNoParseDate, duration: int):
        json_date_to_id, json_date = generate_json_day(json)
        _, parse_slot = generate_json_date(json)

        for day_id in json_date.keys():
            if day_id in parse_slot:
                start_day, end_day = json_date[day_id]
                start_time = start_day

                sorted_parse_slot = sorted(parse_slot[day_id], key=lambda x: x[0])

                print(f"Дата: {json_date[day_id][0].date()}")
                for start_slot, end_slot in sorted_parse_slot:
                    time_duration = start_slot - start_time

                    if start_time < start_slot and time_duration.seconds // 60 >= duration:
                        print(f"С:\t{start_time.time()}\nДо:\t{start_slot.time()}\n")
                    start_time = end_slot