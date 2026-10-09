import unittest
from datetime import datetime, timedelta

from logout_time import (
    calculate_logout_time,
    parse_time,
)


class TestLogoutTime(unittest.TestCase):

    def test_parse_valid_time(self):
        result = parse_time("08:15")
        self.assertEqual(result.hour, 8)
        self.assertEqual(result.minute, 15)

    def test_parse_invalid_time(self):
        for value in ("8:15", "25:00", "08:75", "abc", ""):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_time(value)

    def test_calculate_logout_time(self):
        login = parse_time("08:15")
        result = calculate_logout_time(login)
        self.assertEqual(result.strftime("%H:%M"), "16:33")

    def test_custom_work_and_break_times(self):
        login = parse_time("09:00")
        result = calculate_logout_time(
            login,
            work_time=timedelta(hours=8),
            break_time=timedelta(minutes=45),
        )
        self.assertEqual(result.strftime("%H:%M"), "17:45")


if __name__ == "__main__":
    unittest.main()
