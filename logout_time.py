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


def calculate_time_difference(start: datetime, end: datetime) -> timedelta:
    """Calculate the difference between two times (end - start)."""
    return end - start


def format_timedelta(td: timedelta) -> str:
    """Format a timedelta as HH:MM:SS."""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def main() -> None:
    """Run the logout time calculator."""
    login = input("Login time (HH:MM): ").strip()

    try:
        start = parse_time(login)
    except ValueError as exc:
        print(f"Error: {exc}")
        print("Example of valid input: 08:15")
        return

    # Calculate expected logout time
    expected_logout = calculate_logout_time(start)

    print(f"\nLogin time : {start.strftime(TIME_FORMAT)}")
    print(f"Work time  : {WORK_TIME}")
    print(f"Break      : {BREAK_TIME}")
    print(f"Expected logout time: {expected_logout.strftime(TIME_FORMAT)}")

    # Feature 1: Check for early logout
    early_logout = input("\nAre you logging out early today? (yes/no): ").strip().lower()
    if early_logout in ['yes', 'y']:
        while True:
            early_time_str = input("Enter your actual logout time (HH:MM): ").strip()
            try:
                early_logout_time = parse_time(early_time_str)
                break
            except ValueError as exc:
                print(f"Error: {exc}")
                print("Please enter time in HH:MM format.")

        # Calculate time difference
        time_left_early = calculate_time_difference(expected_logout, early_logout_time)

        if time_left_early.total_seconds() > 0:
            # User left early
            print(f"\nYou left early by: {format_timedelta(time_left_early)}")

            # Calculate work hours lost (assuming break is still taken)
            actual_time_at_work = calculate_time_difference(start, early_logout_time)
            actual_work_time = actual_time_at_work - BREAK_TIME
            if actual_work_time.total_seconds() < 0:
                actual_work_time = timedelta(0)  # Can't have negative work time

            work_hours_lost = WORK_TIME - actual_work_time
            if work_hours_lost.total_seconds() < 0:
                work_hours_lost = timedelta(0)  # Can't lose negative time

            hours_lost = int(work_hours_lost.total_seconds() // 3600)
            minutes_lost = int((work_hours_lost.total_seconds() % 3600) // 60)

            print(f"Work hours lost: {format_timedelta(work_hours_lost)}")
            print(f"Today you lost {hours_lost} hours and {minutes_lost} minutes, so tomorrow you have to work {hours_lost} hours and {minutes_lost} minutes extra.")
        else:
            # User left late (overtime)
            overtime = calculate_time_difference(early_logout_time, expected_logout)
            print(f"\nYou worked overtime by: {format_timedelta(overtime)}")

            # Calculate actual work time including overtime
            actual_time_at_work = calculate_time_difference(start, early_logout_time)
            actual_work_time = actual_time_at_work - BREAK_TIME
            if actual_work_time.total_seconds() < 0:
                actual_work_time = timedelta(0)

            overtime_work = actual_work_time - WORK_TIME
            if overtime_work.total_seconds() < 0:
                overtime_work = timedelta(0)

            print(f"Overtime work: {format_timedelta(overtime_work)}")

    # Feature 2: Overtime planning
    overtime_plan = input("\nAre you planning to do overtime today? (yes/no): ").strip().lower()
    if overtime_plan in ['yes', 'y']:
        while True:
            planned_logout_str = input("Enter the time you plan to logout (HH:MM): ").strip()
            try:
                planned_logout_time = parse_time(planned_logout_str)
                break
            except ValueError as exc:
                print(f"Error: {exc}")
                print("Please enter time in HH:MM format.")

        # Calculate overtime based on planned logout time
        if planned_logout_time > expected_logout:
            planned_overtime = calculate_time_difference(planned_logout_time, expected_logout)
            print(f"\nIf you logout at {planned_logout_time.strftime(TIME_FORMAT)}, you will accumulate {format_timedelta(planned_overtime)} of overtime.")

            # Calculate actual work time with planned logout
            actual_time_at_work = calculate_time_difference(start, planned_logout_time)
            actual_work_time = actual_time_at_work - BREAK_TIME
            if actual_work_time.total_seconds() < 0:
                actual_work_time = timedelta(0)

            print(f"Your total work time will be: {format_timedelta(actual_work_time)}")
        elif planned_logout_time < expected_logout:
            time_left_early = calculate_time_difference(expected_logout, planned_logout_time)
            print(f"\nIf you logout at {planned_logout_time.strftime(TIME_FORMAT)}, you will leave early by {format_timedelta(time_left_early)}.")

            # Calculate actual work time
            actual_time_at_work = calculate_time_difference(start, planned_logout_time)
            actual_work_time = actual_time_at_work - BREAK_TIME
            if actual_work_time.total_seconds() < 0:
                actual_work_time = timedelta(0)

            work_hours_lost = WORK_TIME - actual_work_time
            if work_hours_lost.total_seconds() < 0:
                work_hours_lost = timedelta(0)

            print(f"Your work hours lost would be: {format_timedelta(work_hours_lost)}")
        else:
            print(f"\nIf you logout at {planned_logout_time.strftime(TIME_FORMAT)}, you will logout exactly at the expected time - no overtime or undertime.")


if __name__ == "__main__":
    main()
