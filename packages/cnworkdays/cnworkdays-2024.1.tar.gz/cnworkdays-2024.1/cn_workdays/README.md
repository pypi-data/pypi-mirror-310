# cnworkdays

A Python tool for managing Chinese public holidays and compensatory working days. This tool helps you accurately calculate working days while accounting for China's unique holiday schedule.

## Features

- **Holiday Announcement Parser**: parse official holiday announcements from the General Office of the State Council to generate data for annual public holidays and compensatory working days in China.

- **Working Day Calculator**: calculate dates before or after a specified number of working days, taking into account official public holidays and compensatory working days in China.

## Installation

```bash
pip install cnworkdays
```

## Usage

`cnworkdays` provides two main commands: `holiparse` and `workcalc`.

### Holiday Announcement Parser

Launch the web application for parsing holiday announcements:

```shell
cnworkdays holiparse

✨ Running marimo app Holiday Announcement Parser
🔗 URL: http://127.0.0.1:8080
```

By default, the application runs at <http://127.0.0.1:8080>. To customize the host and port:

```shell
cnworkdays holiparse --host 0.0.0.0 --port 9000

✨ Running marimo app Holiday Announcement Parser
🔗 URL: http://0.0.0.0:9000
```

### Working Day Calculator

Launch the web application for calculating working days:

```shell
cnworkdays workcalc

✨ Running marimo app Working Day Calculator
🔗 URL: http://127.0.0.1:8080
```

By default, the application runs at <http://127.0.0.1:8080>. To customize the host and port:

```bash
cnworkdays workcalc --host 0.0.0.0 --port 9000

✨ Running marimo app Working Day Calculator
🔗 URL: http://0.0.0.0:9000
```

## Changelog

### 2024.1

Release date: 2024-11-14

- Enhance browser application with more descriptive page titles for better user experience.
- Fix the issue that `workcalc` gets stuck when negative days are provided.

### 2024.0

Release date: 2024-11-13

- Launch `cnworkdays` CLI with two main commands:

  - `holiparse`: generate data for annual public holidays and compensatory working days based on notifications from the General Office of the State Council.
  - `workcalc`: calculate the date after or before a specified number of working days, accounting for official public holidays and compensatory working days in China.

- Add support for date calculations spanning from January 1, 2018, to December 31, 2024
