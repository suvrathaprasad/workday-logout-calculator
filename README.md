# Workday Logout Time Calculator

A lightweight Python command-line utility that calculates your expected logout time based on your login time, daily working hours, and break duration.

## Features

- Accepts login time in strict `HH:MM` format.
- Calculates the expected logout time automatically.
- Accounts for 7 hours and 48 minutes of working time and a 30-minute break by default.
- Validates user input and displays helpful error messages.
- Supports custom working hours and break durations through its calculation function.
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

Enter your login time when prompted, using the `HH:MM` format.

### Example

```text
Login time (HH:MM): 08:15

Login time : 08:15
Work time  : 7:48:00
Break      : 0:30:00
Logout time: 16:33
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
