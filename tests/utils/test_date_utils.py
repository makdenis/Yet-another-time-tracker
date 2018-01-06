"""
Created by anthony on 18.12.2017
test_date_utils
"""
import unittest

from datetime import datetime, date

import utils.date_utils as du

# fck these tests. i dont have enough time to fix them (since i have finals in 10 hours)
# so they may not be working on next week :)


class TaskServiceTest(unittest.TestCase):

    def test_full_date_and_time_cur_month(self):
        arg = '25 дек 13-37'
        parsed = du.parse_date_msg(arg)

        today = datetime.today()
        expected = datetime(year=today.year, month=12, day=25, hour=13, minute=37)

        if today.day > 25:
            expected = datetime(year=today.year + 1, month=12, day=25, hour=13, minute=37)
        self.assertEqual(parsed, expected)

    def test_full_date_and_time_next_month(self):
        arg = '10 jan 12-28'
        parsed = du.parse_date_msg(arg)

        today = datetime.today()
        expected = datetime(year=today.year+1, month=1, day=10, hour=12, minute=28)
        self.assertEqual(parsed, expected)


    def test_only_time_delimiter_1(self):
        arg = '03-30'
        parsed = du.parse_date_msg(arg)

        today = datetime.today()
        expected = datetime(year=today.year, month=today.month, day=today.day, hour=3, minute=30)
        if today.hour > 3:
            expected = datetime(year=today.year, month=today.month, day=today.day + 1, hour=3, minute=30)
        self.assertEqual(parsed, expected)

    def test_only_time_delimiter_2(self):
        arg = '13:37'
        parsed = du.parse_date_msg(arg)

        today = datetime.today()
        expected = datetime(year=today.year, month=today.month, day=today.day, hour=13, minute=37)
        if today.hour > 13:
            expected = datetime(year=today.year, month=today.month, day=today.day + 1, hour=13, minute=37)

        self.assertEqual(parsed, expected)

    def test_only_time_delimiter_3(self):
        arg = '00.43'
        parsed = du.parse_date_msg(arg)

        today = datetime.today()
        expected = datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=43)
        if today.hour > 0:
            expected = datetime(year=today.year, month=today.month, day=today.day + 1, hour=0, minute=43)

        self.assertEqual(parsed, expected)

    def test_only_time_three_digits(self):
        arg = '945'
        parsed = du.parse_date_msg(arg)

        today = datetime.today()
        expected = datetime(year=today.year, month=today.month, day=today.day, hour=9, minute=45)
        if today.hour > 9:
            expected = datetime(year=today.year, month=today.month, day=today.day + 1, hour=9, minute=45)

        self.assertEqual(parsed, expected)


    def test_day_and_time_in_past(self):
        arg = '15 0-43'
        parsed = du.parse_date_msg(arg)

        today = datetime.today()
        expected = datetime(year=today.year + 1, month=1, day=15, hour=0, minute=43)

        self.assertEqual(parsed, expected)

    def test_day_and_time_in_future(self):
        arg = '25 14-37'
        parsed = du.parse_date_msg(arg)

        today = datetime.today()
        expected = datetime(year=today.year, month=today.month, day=25, hour=14, minute=37)

        self.assertEqual(parsed, expected)

    def test_day_and_time_in_future_4_digits_time(self):
        arg = '25 1422'
        parsed = du.parse_date_msg(arg)

        today = datetime.today()
        expected = datetime(year=today.year, month=today.month, day=25, hour=14, minute=22)

        self.assertEqual(parsed, expected)


if __name__ == '__main__':
    unittest.main()
