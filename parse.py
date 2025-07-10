from abc import ABC
from typing import Container
from datetime import datetime

from formated import Formated, FormatedDateTime
from annotations import (
    JsonParseDays,
    ParserDayInfoJson,
    ParseTimeSlotInfoJson
)


class ParserJson(ABC):
    def parse(self, json_date: dict) -> Container:
        ...


class ParserDayInfo(ParserJson):
    DAYS_KEY = 'days'

    def __init__(self, formated: Formated = FormatedDateTime()):
        self.formated = formated

    def parse_day(self, json: dict) -> ParserDayInfoJson:
        """
        Метод `parse_day` обрабатывает исходны JSON,
        полученный от ручки и превращает его в удобный для анализа

        :param json: JSON от ручки
        :return: Generator
            first next: Обработанный JSON (dict)
            second next: JSON (dict), который содержит date-id для удобного поиска за O(1)
        """
        json_date = {}
        json_date_to_id = {}

        for day_info in json[self.DAYS_KEY]:
            id_day, date, start_time, end_time = day_info.values()

            datetime_data = self.formated.formate_date(date)
            datetime_start_time = self.formated.formate_time(start_time)
            datetime_end_time = self.formated.formate_time(end_time)

            json_date[id_day] = (
                datetime(*datetime_data, *datetime_start_time),
                datetime(*datetime_data, *datetime_end_time)
            )
            json_date_to_id[date] = id_day

        yield json_date
        yield json_date_to_id


class ParseTimeSlotInfo(ParserJson):
    TIMESLOT_KEY = 'timeslots'

    def __init__(self, formated: Formated = FormatedDateTime()):
        self.formated = formated

    def get_day(self, day_info: datetime):
        """
        Метод `get_day` просто возвращает информацию о дне (YYYY, MM, D)

        :param day_info: Дата в формате datetime
        :return: tuple
        """
        return (
            day_info.year,
            day_info.month,
            day_info.day
        )

    def parse_slot(self, json: dict, json_parse_days: JsonParseDays) -> ParseTimeSlotInfoJson:
        """
        Метод `parse_slot` обрабатывает переданный `json`, и переделывает его в более удобный для обработки

        :param json:            Переданный JSON
        :param json_parse_days: JSON с уже обработанными данными из класса `ParserDayInfo`
        :return: JSON (dict)
        """
        json_slot = {}

        for slot_info in json[self.TIMESLOT_KEY]:
            id_slot, day_id, start_time, end_time = slot_info.values()

            day_json = json_parse_days[day_id]

            datetime_start_time = self.formated.formate_time(start_time)
            datetime_end_time = self.formated.formate_time(end_time)

            if not json_slot.get(day_id):
                json_slot[day_id] = []
            json_slot[day_id].append(
                (
                    datetime(*self.get_day(day_json[0]), *datetime_start_time),
                    datetime(*self.get_day(day_json[1]), *datetime_end_time)
                )
            )
        return json_slot
