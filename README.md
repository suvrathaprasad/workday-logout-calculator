# Workday Logout Time Calculator

A lightweight Python command-line utility that calculates your expected logout time based on your login time, daily working hours, and break duration.

## Features

- Accepts login time in strict `HH:MM` format.
- Calculates the expected logout time automatically.
- Accounts for 7 hours and 48 minutes of working time and a 30-minute break by default.
- Validates user input and displays helpful error messages.
- Supports custom working hours and break durations through its calculation function.
- Early logout detection - calculates time lost and suggests makeup time for next day
- Overtime planning - input planned logout time to see accumulated overtime
- Includes automated unit tests using Python's built-in `unittest` framework.
- Requires no third-party dependencies.

## Requirements

- Python 3.8 or later

## Project Structure

```text
workday-logout-calculator/
├── logout_time.py
├── test_logout_time.py
├── README.md
├── .gitignore
└── LICENSE
```

## Usage

Run the script from your terminal:

```bash
python3 logout_time.py
```

You will be prompted for:
1. Your login time (HH:MM format)
2. Whether you're logging out early today (yes/no)
3. If yes, your actual logout time
4. Whether you're planning to do overtime today (yes/no)
5. If yes, your planned logout time

### Example

```text
Login time (HH:MM): 08:15

Login time : 08:15
Work time  : 7:48:00
Break      : 0:30:00
Expected logout time: 16:33

Are you logging out early today? (yes/no): no

Are you planning to do overtime today? (yes/no): yes
Enter the time you plan to logout (HH:MM): 17:30

If you logout at 17:30, you will accumulate 00:42:00 of overtime.
Your total work time will be: 08:12:00
```

### Invalid Input

The script validates the input and displays an error message for invalid times.

For example:

```text
Login time (HH:MM): 25:00
Error: Invalid time. Hours must be 00–23 and minutes 00–59.
Example of valid input: 08:15
```

Accepted input must follow the strict `HH:MM` format, such as `08:15` or `16:45`.

## Configuration

The default working hours and break duration are defined at the top of `logout_time.py`:

```python
WORK_TIME = timedelta(hours=7, minutes=48)
BREAK_TIME = timedelta(minutes=30)
```

Modify these values to match your work schedule.

The `calculate_logout_time()` function also accepts custom working hours and break durations, allowing the calculation to be reused in other Python programs.


## Testing

The project includes automated tests for input validation and logout-time calculations.

Run the tests from the repository's root directory:

```bash
python3 -m unittest -v
```

The tests use Python's built-in `unittest` framework, so no additional packages are required.

## Limitations

- The calculator assumes a fixed working duration and break duration.
- It does not account for holidays, overtime rules, or flexible work schedules.
- The displayed logout time represents a clock time; the script does not display the date when a shift ends after midnight.

## License

This project is distributed under the MIT License. See the `LICENSE` file for details.
