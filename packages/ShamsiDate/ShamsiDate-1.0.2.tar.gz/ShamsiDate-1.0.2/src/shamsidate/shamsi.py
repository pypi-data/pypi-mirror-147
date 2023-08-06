#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert Shamsi (Jalali) to Gregorian date and vice versa

@author: Samic (samic.org)

Created on 2022-04-19
Based on code written on 30 Mar 2003 (in ASP) and on 2 Jan 2009 (in Delphi)

"""

import sys
import datetime
import calendar
import argparse
import json


# Number of days per month (except for leap years)
G_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
S_DAYS = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]

MONTH_NAMES_FAEN = ["Farvardin", "Ordibehesht", "Khordad", "Tir", "Mordad",
                    "Shahrivar", "Mehr", "Aban", "Azar", "Dey", "Bahman", "Esfand"]
MONTH_NAMES_FA = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
"مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
MONTH_NAMES_ABBR_FAEN = ["Far", "Ord", "Kho", "Tir", "Mor", "Sha",
                         "Meh", "Aba", "Aza", "Dey", "Bah", "Esf"]
WEEKDAY_NAMES_FAEN = ["Doshanbe", "Seshanbe", "Chaharshanbe",
                      "Panjshanbe", "Jome", "Shanbe", "Yekshanbe"]
WEEKDAY_NAMES_FA = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]
WEEKDAY_NAMES_ABBR_EN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def g_is_leap(g_year):
    """Return True for leap years, False for non-leap years."""
    return g_year % 4 == 0 and (g_year % 100 != 0 or g_year % 400 == 0)


def s_is_leap(s_year):
    """Return True for Shamsi leap years, False for non-leap years."""
    return s_year % 33 in [1, 5, 9, 13, 17, 22, 26, 30]


def weekday(g_year, g_month, g_day):
    """Return weekday (0-6 for Mon-Sun) for year, month"""
    return datetime.date(g_year, g_month, g_day).weekday()


def date_valid(year, month, day, cal='gregorian'):
    """Check to see if date (year, month, day) is valid"""
    result = True
    if month < 1 or month > 12 or day < 1:
        result = False
    if cal == "shamsi":
        if year < 1 or year > 9999:
            result = False
        days_left = S_DAYS[month-1]
        if month == 12 and s_is_leap(year):
            days_left = 30
        if day > days_left:
            result = False
    else:
        if year < 622 or year > 9999:
            result = False

        if day > calendar.monthrange(year, month)[1]:
            result = False

    return result


def gregorian_to_shamsi(g_year, g_month, g_day):
    """Convert a Gregorian date to Shamsi"""
    if not date_valid(g_year, g_month, g_day, 'gregorian'):
        return -1, -1, -1

    date1 = datetime.datetime(622, 3, 21)
    date2 = datetime.datetime(g_year, g_month, g_day)
    total_days = abs((date2 - date1).days)
    s_year = 1  # 0622-03-21 --> 1/1/1
    s_month = 0
    s_day = 1
    while total_days > 0:
        s_month += 1
        if s_month == 13:
            s_year += 1
            s_month = 1

        days_left = S_DAYS[s_month-1]
        if s_month == 12 and s_is_leap(s_year):
            days_left = 30
        total_days -= days_left

    if total_days == 0:
        s_month += 1
        if s_month == 13:
            s_year += 1
            s_month = 1
    else:
        s_day = days_left + total_days + 1

    return s_year, s_month, s_day


def shamsi_to_gregorian(s_year, s_month, s_day):
    """Convert a Shamsi date to Gregorian"""
    if not date_valid(s_year, s_month, s_day, 'shamsi'):
        return -1, -1, -1

    base_date = datetime.datetime(621, 3, 21)
    year = 0  # 0621-03-21 --> 0/1/1
    month = 1
    total_days = 30

    while True:
        month += 1
        if month == 13:
            year += 1
            month = 1
        days_left = S_DAYS[month-1]

        if month == 12 and s_is_leap(year):
            days_left = 30

        total_days += days_left

        if month == s_month and year == s_year:
            break

    total_days = total_days - days_left + s_day
    result = base_date + datetime.timedelta(days=total_days)

    return result.year, result.month, result.day


def print_shamsi_to_gregorian(*d, json_output=False):
    """print formatted date"""
    r = shamsi_to_gregorian(*d)
    if r[0] == -1:
        print('Invalid date. \nRun "shamsi -h" to see the help page.')
        sys.exit(0)
    if not json_output:
        print(f'{r[0]}-{r[1]}-{r[2]}')
    else:
        j = {"year":r[0],
             "month":r[1],
             "day":r[2],
             "weekday":weekday(*d),
             "weekday_name":WEEKDAY_NAMES_ABBR_EN[weekday(*d)],
             "month_name_abbr":calendar.month_abbr[r[1]],
             "month_name":calendar.month_name[r[1]]
             }
        print(json.dumps(j, indent=4))


def print_gregorian_to_shamsi(*d, json_output=False):
    """print formatted date"""
    r = gregorian_to_shamsi(*d)
    if r[0] == -1:
        print('Invalid date. \nRun "shamsi -h" to see the help page.')
        sys.exit(0)
    if not json_output:
        print(f'{r[0]}-{r[1]}-{r[2]}')
    else:
        j = {"year":r[0],
             "month":r[1],
             "day":r[2],
             "weekday":weekday(*d),
             "weekday_name":WEEKDAY_NAMES_ABBR_EN[weekday(*d)],
             "weekday_name_faen":WEEKDAY_NAMES_FAEN[weekday(*d)],
             "weekday_name_fa":WEEKDAY_NAMES_FA[weekday(*d)],
             "month_name_abbr":MONTH_NAMES_ABBR_FAEN[r[1]-1],
             "month_name_faen":MONTH_NAMES_FAEN[r[1]-1],
             "month_name_fa":MONTH_NAMES_FA[r[1]-1]
             }
        print(json.dumps(j, indent=4))


def custom_format(form, date):
    """
    use a user-provided format to process input date
    example: shamsi -f 'dd/M/YYYY' -s 16/1/1350
    year has to 4 digits but day and month can be 1 digit
    """
    form = form.upper()
    if form.find('YYYY') == -1 or form.find('M') == -1 or form.find('D') == -1:
        print('Invalid format. \nRun "shamsi -h" to see the help page.')
        sys.exit(0)

    year_pos = form.index('YYYY')
    year = int(date[year_pos:][:4])

    month_pos = form.find('MM')
    if month_pos >= 0:
        month = int(date[month_pos:][:2])
    else:
        month_pos = form.index('M')
        month = int(date[month_pos:][:1])

    day_pos = form.find('DD')
    if day_pos >= 0:
        day = int(date[day_pos:][:2])
    else:
        month_pos = form.index('D')
        day = int(date[month_pos:][:1])

    return year, month, day


def main(argv=None):
    parser = argparse.ArgumentParser(prog='shamsi',
                description='Convert Shamsi (Jalali) to Gregorian date and vice versa',
                epilog="By Samic (samic.org)")
    parser.add_argument("date", help="a date to convert (format: YYYY-MM-DD)", nargs='?')
    parser.add_argument("-s", "--shamsi", help="convert a Shamsi (Jalali) date", action="store_true")
    parser.add_argument("-g", "--gregorian", help="convert a Gregorian date", action="store_true")
    parser.add_argument("-f", "--format", help="define date format (ex: -f 'dd/M/YYYY' -s 16/1/1350)")
    parser.add_argument("-j", "--json", help="give JSON output", action="store_true")
    args = parser.parse_args(argv)

    if not args.date:
        n = datetime.datetime.now()
        print_gregorian_to_shamsi(n.year, n.month, n.day, json_output=args.json)
    else:
        if args.format:
            d = custom_format(args.format, args.date)
        else:
            try:
                d = args.date.split('-')
                d = [int(_) for _ in d]
            except:
                print('Invalid date. \nRun "shamsi -h" to see the help page.')
                sys.exit(0)

        if len(d) != 3:
            print('Invalid date. \nRun "shamsi -h" to see the help page.')
            sys.exit(0)

        if args.shamsi:
            print_shamsi_to_gregorian(*d, json_output=args.json)

        elif args.gregorian:
            print_gregorian_to_shamsi(*d, json_output=args.json)

        else:
            if d[0] < 1600:
                print_shamsi_to_gregorian(*d, json_output=args.json)
            else:
                print_gregorian_to_shamsi(*d, json_output=args.json)




if __name__ == '__main__':
    main()



# Tests:

def test_gregorian_to_shamsi():
    """test function for pytest"""
    assert gregorian_to_shamsi(2000, 1, 1) == (1378, 10, 11)
    assert gregorian_to_shamsi(1500, 9, 14) == (879, 6, 23)
    assert gregorian_to_shamsi(2050, 2, 28) == (1428, 12, 10)
    assert gregorian_to_shamsi(1956, 2, 29) == (1334, 12, 9)
    assert gregorian_to_shamsi(2015, 12, 31) == (1394, 10, 10)
    assert gregorian_to_shamsi(2036, 2, 29) == (1414, 12, 10)
    assert gregorian_to_shamsi(700, 8, 8) == (79, 5, 17)
    assert gregorian_to_shamsi(1489, 11, 18) == (868, 8, 27)
    assert gregorian_to_shamsi(2021, 3, 21) == (1400, 1, 1)
    assert gregorian_to_shamsi(1986, 4, 2) == (1365, 1, 13)
    assert gregorian_to_shamsi(1873, 3, 20) == (1251, 12, 30)
    assert gregorian_to_shamsi(3021, 11, 14) == (2400, 8, 23)
    assert gregorian_to_shamsi(1988, 5, 4) == (1367, 2, 14)
    assert gregorian_to_shamsi(2122, 1, 31) == (1500, 11, 11)
    assert gregorian_to_shamsi(2017, 3, 20) == (1395, 12, 30)
    assert gregorian_to_shamsi(2000, 1, 1) == (1378, 10, 11)
    assert gregorian_to_shamsi(2017, 10, 19) == (1396, 7, 27)
    assert gregorian_to_shamsi(2019, 2, 18) == (1397, 11, 29)
    assert gregorian_to_shamsi(1990, 9, 23) == (1369, 7, 1)
    assert gregorian_to_shamsi(1990, 9, 23) == (1369, 7, 1)
    assert gregorian_to_shamsi(2013, 9, 16) == (1392, 6, 25)
    assert gregorian_to_shamsi(2018, 3, 20) == (1396, 12, 29)
    assert gregorian_to_shamsi(2021, 2, 11) == (1399, 11, 23)
    assert gregorian_to_shamsi(2021, 7, 16) == (1400, 4, 25)


def test_shamsi_to_gregorian():
    """test function for pytest"""
    assert shamsi_to_gregorian(1400, 1, 1) == (2021, 3, 21)
    assert shamsi_to_gregorian(1365, 1, 13) == (1986, 4, 2)
    assert shamsi_to_gregorian(1251, 12, 30) == (1873, 3, 20)
    assert shamsi_to_gregorian(2400, 8, 23) == (3021, 11, 14)
    assert shamsi_to_gregorian(1378, 10, 11) == (2000, 1, 1)
    assert shamsi_to_gregorian(879, 6, 23) == (1500, 9, 14)
    assert shamsi_to_gregorian(1428, 12, 10) == (2050, 2, 28)
    assert shamsi_to_gregorian(1334, 12, 9) == (1956, 2, 29)
    assert shamsi_to_gregorian(1394, 10, 10) == (2015, 12, 31)
    assert shamsi_to_gregorian(1414, 12, 10) == (2036, 2, 29)
    assert shamsi_to_gregorian(79, 5, 17) == (700, 8, 8)
    assert shamsi_to_gregorian(868, 8, 27) == (1489, 11, 18)
    assert shamsi_to_gregorian(1367, 2, 14) == (1988, 5, 4)
    assert shamsi_to_gregorian(1369, 7, 1) == (1990, 9, 23)
    assert shamsi_to_gregorian(1395, 3, 21) == (2016, 6, 10)
    assert shamsi_to_gregorian(1395, 12, 9) == (2017, 2, 27)
    assert shamsi_to_gregorian(1395, 12, 30) == (2017, 3, 20)
    assert shamsi_to_gregorian(1396, 1, 1) == (2017, 3, 21)
    assert shamsi_to_gregorian(1400, 6, 31) == (2021, 9, 22)
    assert shamsi_to_gregorian(1396, 7, 27) == (2017, 10, 19)
    assert shamsi_to_gregorian(1397, 11, 29) == (2019, 2, 18)
    assert shamsi_to_gregorian(1399, 11, 23) == (2021, 2, 11)
    assert shamsi_to_gregorian(1400, 4, 25) == (2021, 7, 16)
    assert shamsi_to_gregorian(1400, 12, 20) == (2022, 3, 11)


def test_s_is_leap():
    """test function for pytest"""
    s_is_leap(1358) == True
    s_is_leap(1366) == True
    s_is_leap(1370) == True
    s_is_leap(1387) == True
    s_is_leap(1395) == True
    s_is_leap(1399) == True
    s_is_leap(1403) == True
    s_is_leap(1367) == False
    s_is_leap(1396) == False
    s_is_leap(1397) == False
    s_is_leap(1398) == False
    s_is_leap(1400) == False


def test_main(capsys):
    """test function for pytest"""
    main(["1400-12-20"])
    captured = capsys.readouterr()
    assert captured.out == "2022-3-11\n"

    main(["-s", "1400-12-20"])
    captured = capsys.readouterr()
    assert captured.out == "2022-3-11\n"

    main(["2022-3-11"])
    captured = capsys.readouterr()
    assert captured.out == "1400-12-20\n"

    main(["-g", "2022-3-11"])
    captured = capsys.readouterr()
    assert captured.out == "1400-12-20\n"

    main(["-f", "dd/M/YYYY", "-s", "16/1/1350"])
    captured = capsys.readouterr()
    assert captured.out == "1971-4-5\n"

    main([])
    captured = capsys.readouterr()
    main(["-s", captured.out.strip()])
    captured = capsys.readouterr()
    d=datetime.datetime.today()
    assert captured.out == f"{d.year}-{d.month}-{d.day}\n"
