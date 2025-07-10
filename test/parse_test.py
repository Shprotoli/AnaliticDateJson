from unittest import main, TestCase
from datetime import datetime

from test_task_trajectory.parse import ParserDayInfo, ParseTimeSlotInfo


class TestParserDayInfo(TestCase):
    json = {
        "days": [
            {"id": 1, "date": "2024-10-10", "start": "09:00", "end": "18:00"},
            {"id": 2, "date": "2024-10-11", "start": "08:00", "end": "17:00"}
        ],
        "timeslots": [
            {"id": 1, "day_id": 1, "start": "11:00", "end": "12:00"},
            {"id": 2, "day_id": 1, "start": "12:00", "end": "13:00"},
            {"id": 3, "day_id": 2, "start": "09:30", "end": "16:00"}
        ]
    }

    @classmethod
    def setUpClass(cls):
        cls.parser_day_info = ParserDayInfo()

    def test_parse_day_return(self):
        generator_parse_day_info = self.parser_day_info.parse_day(self.json)

        self.assertEqual(next(generator_parse_day_info), {
            1: (datetime(2024, 10, 10, 9, 0), datetime(2024, 10, 10, 18, 0)),
            2: (datetime(2024, 10, 11, 8, 0), datetime(2024, 10, 11, 17, 0))
        })
        self.assertEqual(next(generator_parse_day_info), {
            '2024-10-10': 1,
            '2024-10-11': 2
        })


class TestParseTimeSlotInfo(TestCase):
    json = {
        "days": [
            {"id": 1, "date": "2024-10-10", "start": "09:00", "end": "18:00"},
            {"id": 2, "date": "2024-10-11", "start": "08:00", "end": "17:00"}
        ],
        "timeslots": [
            {"id": 1, "day_id": 1, "start": "11:00", "end": "12:00"},
            {"id": 2, "day_id": 1, "start": "12:00", "end": "13:00"},
            {"id": 3, "day_id": 2, "start": "09:30", "end": "16:00"}
        ]
    }

    @classmethod
    def setUpClass(cls):
        cls.parser_timeslot_info = ParseTimeSlotInfo()

        parser_day_info = ParserDayInfo()
        cls.json_parse_days = next(parser_day_info.parse_day(cls.json))

    def test_parse_timeslots_return(self):
        self.assertEqual(self.parser_timeslot_info.parse_slot(self.json, self.json_parse_days), {
            1: [
                (datetime(2024, 10, 10, 11, 0), datetime(2024, 10, 10, 12, 0)),
                (datetime(2024, 10, 10, 12, 0), datetime(2024, 10, 10, 13, 0))
            ],
            2: [
                (datetime(2024, 10, 11, 9, 30), datetime(2024, 10, 11, 16, 0))
            ]
        }
)


if __name__ == "__main__":
    main()
