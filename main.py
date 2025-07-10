import argparse
from datetime import datetime

from requests import get

from arg_handler import BusyTimeHandler, FreeTimeHandler, CheckTimeHandler, DurationTimeHandler


def math_arg(args):
    match args.mode:
        case "busy":
            assert args.date, argparse.ArgumentTypeError(
                f"При работе в режиме `busy`, требуется передать флаг `--date`!")
            BusyTimeHandler().handler(json_request, args.date)
        case "free":
            assert args.date, (
                argparse.ArgumentTypeError(f"При работе в режиме `free`, требуется передать флаг `--date`!"))
            FreeTimeHandler().handler(json_request, args.date)
        case "check":
            assert args.date and args.time, (
                argparse.ArgumentTypeError(
                    f"При работе в режиме `check`, требуется передать флаг `--date` и `--time`!"))
            CheckTimeHandler().handler(json_request, args.date, args.time)
        case "duration":
            assert args.dur, "При работе в режиме `duration`, требуется передать флаг `--dur`"
            DurationTimeHandler().handler(json_request, args.dur)


def valid_date(date):
    try:
        return str(datetime.strptime(date, "%Y-%m-%d").date())
    except ValueError:
        raise argparse.ArgumentTypeError(f"Неверный формат даты: '{date}'. Ожидается YYYY-MM-DD.")


def valid_duration(duration):
    try:
        hour, minute = duration.split(":")
        request_time_duration = int(minute) + int(hour) * 60

        return request_time_duration
    except ValueError:
        raise argparse.ArgumentTypeError(f"Неверный формат продолжительности: HH:MM")


if __name__ == "__main__":
    json_request = get("https://ofc-test-01.tspb.su/test-task/").json()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mode',
        choices=["busy", "free", "check", "duration"],
        help='Режим поиска'
    )

    parser.add_argument('--date', type=valid_date, help='Аргумент даты, формата year-month-day')
    parser.add_argument('--time', help='Аргумент времени, формата hour:minute hour:minute')
    parser.add_argument('--dur', type=valid_duration, help='Аргумент продолжительности, просто число, например 5')

    args = parser.parse_args()

    math_arg(args)
