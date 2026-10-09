#!/usr/bin/env python3
"""Calculate the expected logout time from a login time."""

import re
from datetime import datetime, timedelta


WORK_TIME = timedelta(hours=7, minutes=48)
BREAK_TIME = timedelta(minutes=30)
TIME_FORMAT = "%H:%M"


def parse_time(time_str: str) -> datetime:
    """Parse a time string in strict HH:MM format."""
    if not re.fullmatch(r"\d{2}:\d{2}", time_str):
        raise ValueError("Time must be in HH:MM format.")

    try:
        return datetime.strptime(time_str, TIME_FORMAT)
    except ValueError as exc:
        raise ValueError("Invalid time. Hours must be 00–23 and minutes 00–59.") from exc


def calculate_logout_time(
    login_time: datetime,
    work_time: timedelta = WORK_TIME,
    break_time: timedelta = BREAK_TIME,
) -> datetime:
    """Calculate the expected logout time."""
    return login_time + work_time + break_time


def main() -> None:
    """Run the logout time calculator."""
    login = input("Login time (HH:MM): ").strip()

    try:
        start = parse_time(login)
    except ValueError as exc:
        print(f"Error: {exc}")
        print("Example of valid input: 08:15")
        return

    logout = calculate_logout_time(start)

    print(f"\nLogin time : {start.strftime(TIME_FORMAT)}")
    print(f"Work time  : {WORK_TIME}")
    print(f"Break      : {BREAK_TIME}")
    print(f"Logout time: {logout.strftime(TIME_FORMAT)}")


if __name__ == "__main__":
    main()
