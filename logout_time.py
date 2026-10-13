#!/usr/bin/env python3
"""Calculate expected logout time, early departures, and overtime."""

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
        raise ValueError(
            "Invalid time. Hours must be 00–23 and minutes 00–59."
        ) from exc


def calculate_logout_time(
    login_time: datetime,
    work_time: timedelta = WORK_TIME,
    break_time: timedelta = BREAK_TIME,
) -> datetime:
    """Calculate the expected logout time."""
    return login_time + work_time + break_time


def calculate_time_difference(
    start: datetime, end: datetime
) -> timedelta:
    """Calculate the difference between two times (end - start)."""
    return end - start


def format_timedelta(td: timedelta) -> str:
    """Format a timedelta as HH:MM:SS."""
    total_seconds = int(td.total_seconds())
    sign = "-" if total_seconds < 0 else ""
    total_seconds = abs(total_seconds)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d}"


def calculate_actual_work_time(
    login_time: datetime,
    logout_time: datetime,
    break_time: timedelta = BREAK_TIME,
) -> timedelta:
    """Calculate time worked after deducting the break."""
    elapsed_time = calculate_time_difference(login_time, logout_time)
    work_time = elapsed_time - break_time

    return max(work_time, timedelta(0))


def calculate_work_time_lost(
    actual_work_time: timedelta,
    required_work_time: timedelta = WORK_TIME,
) -> timedelta:
    """Calculate how much required work time remains outstanding."""
    return max(required_work_time - actual_work_time, timedelta(0))


def main() -> None:
    """Run the logout time calculator."""
    login = input("Login time (HH:MM): ").strip()

    try:
        start = parse_time(login)
    except ValueError as exc:
        print(f"Error: {exc}")
        print("Example of valid input: 08:15")
        return

    # Calculate expected logout time.
    expected_logout = calculate_logout_time(start)

    print(f"\nLogin time : {start.strftime(TIME_FORMAT)}")
    print(f"Work time  : {WORK_TIME}")
    print(f"Break      : {BREAK_TIME}")
    print(
        f"Expected logout time: "
        f"{expected_logout.strftime(TIME_FORMAT)}"
    )

    # Feature 1: Check actual logout time.
    early_logout = input(
        "\nAre you logging out early today? (yes/no): "
    ).strip().lower()

    if early_logout in ("yes", "y"):
        while True:
            actual_logout_str = input(
                "Enter your actual logout time (HH:MM): "
            ).strip()

            try:
                actual_logout_time = parse_time(actual_logout_str)
                break
            except ValueError as exc:
                print(f"Error: {exc}")
                print("Please enter time in HH:MM format.")

        # Compare actual logout against expected logout.
        difference = calculate_time_difference(
            expected_logout, actual_logout_time
        )

        if difference.total_seconds() < 0:
            # The actual logout was before the expected logout.
            time_left_early = abs(difference)

            actual_work_time = calculate_actual_work_time(
                start, actual_logout_time
            )
            work_hours_lost = calculate_work_time_lost(actual_work_time)

            hours_lost = int(work_hours_lost.total_seconds() // 3600)
            minutes_lost = int(
                (work_hours_lost.total_seconds() % 3600) // 60
            )

            print(
                f"\nYou left early by: "
                f"{format_timedelta(time_left_early)}"
            )
            print(
                f"Work hours lost: "
                f"{format_timedelta(work_hours_lost)}"
            )
            print(
                f"Today you lost {hours_lost} hours and "
                f"{minutes_lost} minutes, so tomorrow you have to "
                f"work {hours_lost} hours and "
                f"{minutes_lost} minutes extra."
            )

        elif difference.total_seconds() > 0:
            # The actual logout was after the expected logout.
            overtime = difference

            actual_work_time = calculate_actual_work_time(
                start, actual_logout_time
            )
            overtime_work = max(
                actual_work_time - WORK_TIME, timedelta(0)
            )

            print(
                f"\nYou worked overtime by: "
                f"{format_timedelta(overtime)}"
            )
            print(
                f"Overtime work: "
                f"{format_timedelta(overtime_work)}"
            )

        else:
            # The actual logout matches the expected logout.
            print("\nYou logged out exactly at the expected time.")
            print("Overtime work: 00:00:00")

    # Feature 2: Overtime planning.
    overtime_plan = input(
        "\nAre you planning to do overtime today? (yes/no): "
    ).strip().lower()

    if overtime_plan in ("yes", "y"):
        while True:
            planned_logout_str = input(
                "Enter the time you plan to logout (HH:MM): "
            ).strip()

            try:
                planned_logout_time = parse_time(planned_logout_str)
                break
            except ValueError as exc:
                print(f"Error: {exc}")
                print("Please enter time in HH:MM format.")

        # Compare planned logout against expected logout.
        planned_difference = calculate_time_difference(
            expected_logout, planned_logout_time
        )

        if planned_difference.total_seconds() > 0:
            # Planned logout is later: calculate positive overtime.
            planned_overtime = planned_difference

            actual_work_time = calculate_actual_work_time(
                start, planned_logout_time
            )

            print(
                f"\nIf you logout at "
                f"{planned_logout_time.strftime(TIME_FORMAT)}, "
                f"you will accumulate "
                f"{format_timedelta(planned_overtime)} of overtime."
            )
            print(
                f"Your total work time will be: "
                f"{format_timedelta(actual_work_time)}"
            )

        elif planned_difference.total_seconds() < 0:
            # Planned logout is earlier: calculate time left.
            time_left_early = abs(planned_difference)

            actual_work_time = calculate_actual_work_time(
                start, planned_logout_time
            )
            work_hours_lost = calculate_work_time_lost(actual_work_time)

            print(
                f"\nIf you logout at "
                f"{planned_logout_time.strftime(TIME_FORMAT)}, "
                f"you will leave early by "
                f"{format_timedelta(time_left_early)}."
            )
            print(
                f"Your work hours lost would be: "
                f"{format_timedelta(work_hours_lost)}"
            )

        else:
            print(
                f"\nIf you logout at "
                f"{planned_logout_time.strftime(TIME_FORMAT)}, "
                "you will logout exactly at the expected time - "
                "no overtime or undertime."
            )


if __name__ == "__main__":
    main()
