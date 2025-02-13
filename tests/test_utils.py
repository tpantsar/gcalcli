from datetime import datetime, timedelta

import pytest
import pytz
from dateutil.tz import UTC, tzutc

from gcalcli.utils import (
    days_since_epoch,
    get_time_from_str,
    get_timedelta_from_str,
    get_times_from_duration,
    localize_datetime,
    set_locale,
)


def test_get_time_from_str():
    assert get_time_from_str('7am tomorrow')


def test_get_time_from_str_non_dayfirst_locale():
    TIMEZONE = 'Europe/Helsinki'
    when = '2025-01-26 11:00'

    # Convert UTC datetime to local datetime
    local_timezone = pytz.timezone(TIMEZONE)

    # Localize the expected datetime to the specified timezone
    expected = local_timezone.localize(datetime(2025, 1, 26, 11, 0))
    result = get_time_from_str(when).astimezone(local_timezone)
    # logger.info(result)

    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_time_from_str_valid_fuzzy_parse_next_week():
    when = 'next Friday at 6pm'
    current_year = datetime.now().year

    result = get_time_from_str(when)
    # logger.info(result)
    assert result.year == current_year, f'Expected {current_year}, but got {result.year}'
    assert result.weekday() == 4, f'Expected Friday, but got {result.strftime("%A")}'
    assert result.hour == 18, f'Expected 18:00, but got {result.strftime("%H:%M")}'


def test_get_time_from_str_valid_fuzzy_parse_today():
    when = 'Today at 3pm'

    current_year = datetime.now().year

    result = get_time_from_str(when)
    # logger.info(result)
    assert result.year == current_year, f'Expected {current_year}, but got {result.year}'
    assert result.weekday() == datetime.now().weekday(), (
        f'Expected today, but got {result.strftime("%A")}'
    )
    assert result.hour == 15, f'Expected 15:00, but got {result.strftime("%H:%M")}'


def test_get_time_from_str_invalid_date():
    when = 'invalid date string'
    with pytest.raises(ValueError, match='Date and time is invalid'):
        get_time_from_str(when)


def test_get_time_from_str_invalid_date_emptystring():
    when = ''
    with pytest.raises(ValueError, match='Date and time is invalid'):
        get_time_from_str(when)


def test_get_time_from_str_dayfirst_locale():
    TIMEZONE = 'Europe/Helsinki'
    when = '04-10-2024 18:00'

    # Convert UTC datetime to local datetime
    local_timezone = pytz.timezone(TIMEZONE)

    expected = local_timezone.localize(datetime(2024, 10, 4, 18, 0))
    result = get_time_from_str(when).astimezone(local_timezone)

    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_time_from_str_dayfirst_locale_leading_zeroes():
    TIMEZONE = 'Europe/Helsinki'
    when = '04.09.2024 18:00'

    # Convert UTC datetime to local datetime
    local_timezone = pytz.timezone(TIMEZONE)

    expected = local_timezone.localize(datetime(2024, 9, 4, 18, 0))
    result = get_time_from_str(when).astimezone(local_timezone)

    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_time_from_str_dayfirst_locale_non_leading_zeroes():
    TIMEZONE = 'Europe/Helsinki'
    when = '4.5.2024 9:00'

    # Convert UTC datetime to local datetime
    local_timezone = pytz.timezone(TIMEZONE)

    expected = local_timezone.localize(datetime(2024, 5, 4, 9, 0))
    result = get_time_from_str(when).astimezone(local_timezone)

    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_parsed_timedelta_from_str():
    assert get_timedelta_from_str('3.5h') == timedelta(hours=3, minutes=30)
    assert get_timedelta_from_str('1') == timedelta(minutes=1)
    assert get_timedelta_from_str('1m') == timedelta(minutes=1)
    assert get_timedelta_from_str('0.5h') == timedelta(minutes=30)
    assert get_timedelta_from_str('1h') == timedelta(hours=1)
    assert get_timedelta_from_str('1h1m') == timedelta(hours=1, minutes=1)
    assert get_timedelta_from_str('1:10') == timedelta(hours=1, minutes=10)
    assert get_timedelta_from_str('2d:1h:3m') == timedelta(days=2, hours=1, minutes=3)
    assert get_timedelta_from_str('2d 1h 3m 10s') == timedelta(
        days=2, hours=1, minutes=3, seconds=10
    )
    assert get_timedelta_from_str('2 days 1 hour 2 minutes 40 seconds') == timedelta(
        days=2, hours=1, minutes=2, seconds=40
    )
    with pytest.raises(ValueError) as ve:
        get_timedelta_from_str('junk')
    assert str(ve.value) == 'Duration is invalid: junk'


def test_get_times_from_duration():
    begin_1970 = '1970-01-01'
    begin_1970_midnight = begin_1970 + 'T00:00:00+00:00'
    two_hrs_later = begin_1970 + 'T02:00:00+00:00'
    next_day = '1970-01-02'
    assert (begin_1970_midnight, two_hrs_later) == get_times_from_duration(
        begin_1970_midnight, duration=120
    )

    assert (begin_1970_midnight, two_hrs_later) == get_times_from_duration(
        begin_1970_midnight, duration='2h'
    )

    assert (begin_1970_midnight, two_hrs_later) == get_times_from_duration(
        begin_1970_midnight, duration='120m'
    )

    assert (begin_1970, next_day) == get_times_from_duration(
        begin_1970_midnight, duration=1, allday=True
    )

    with pytest.raises(ValueError):
        get_times_from_duration('this is not a date')

    with pytest.raises(ValueError):
        get_times_from_duration(begin_1970_midnight, duration='not a duration')

    with pytest.raises(ValueError):
        get_times_from_duration(
            begin_1970_midnight, duration='not a duraction', allday=True
        )


def test_days_since_epoch():
    assert days_since_epoch(datetime(1970, 1, 1, 0, tzinfo=UTC)) == 0
    assert days_since_epoch(datetime(1970, 12, 31)) == 364


def test_set_locale():
    with pytest.raises(ValueError):
        set_locale('not_a_real_locale')


def test_localize_datetime(PatchedGCalI):
    dt = localize_datetime(datetime.now())
    assert dt.tzinfo is not None

    dt = datetime.now(tzutc())
    dt = localize_datetime(dt)
    assert dt.tzinfo is not None
