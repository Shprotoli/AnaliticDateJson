from unittest import main, TestCase

from test_task_trajectory.formated import FormatedDateTime


class TestFormatedDateTime(TestCase):
    formated_date_time = FormatedDateTime()

    def test_formate_date(self):
        self.assertEqual(self.formated_date_time.formate_date("2024-10-10"), (2024, 10, 10))

        with self.assertRaises(AssertionError):
            self.formated_date_time.formate_date("2024-13-10")

        with self.assertRaises(AssertionError):
            self.formated_date_time.formate_date("2024-0-10")

        with self.assertRaises(AssertionError):
            self.formated_date_time.formate_date("2024-1-32")

        with self.assertRaises(AssertionError):
            self.formated_date_time.formate_date("2024-1-0")

    def test_formate_time(self):
        self.assertEqual(self.formated_date_time.formate_time("09:55"), (9, 55))
        self.assertEqual(self.formated_date_time.formate_time("9:55"), (9, 55))
        self.assertEqual(self.formated_date_time.formate_time("9:05"), (9, 5))
        self.assertEqual(self.formated_date_time.formate_time("9:5"), (9, 5))
        self.assertEqual(self.formated_date_time.formate_time("10:10"), (10, 10))

if __name__ == "__main__":
    main()