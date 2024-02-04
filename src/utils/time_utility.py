""" This module contains utility functions to work with time and date. """
from datetime import datetime


def calculate_time_between_string_hours(start_hour, end_hour):
    """Calculate the time between two string hours in seconds."""
    validate_hour(start_hour, "start_hour")
    validate_hour(end_hour, "end_hour")

    start_hour = datetime.strptime(start_hour, "%H:%M:%S")
    end_hour = datetime.strptime(end_hour, "%H:%M:%S")
    return (end_hour - start_hour).seconds


def check_date_order(start_date, end_date):
    """Check if the start date is greater than the end date."""
    validate_date(start_date, "start_date")
    validate_date(end_date, "end_date")
    return start_date > end_date


def check_hour_order(start_hour, end_hour):
    """Check if the start hour is greater than the end hour."""
    validate_hour(start_hour, "start_hour")
    validate_hour(end_hour, "end_hour")
    start_hour = datetime.strptime(start_hour, "%H:%M:%S")
    end_hour = datetime.strptime(end_hour, "%H:%M:%S")
    return start_hour > end_hour


def validate_date(date_text, field_name):
    """Validate if the date is in the correct format."""
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError(
            f"Incorrect date format for {field_name}, should be YYYY-MM-DD")


def validate_hour(hour_text, field_name):
    """Validate if the hour is in the correct format."""
    try:
        datetime.strptime(hour_text, '%H:%M:%S')
    except ValueError:
        raise ValueError(
            f"Incorrect hour format for {field_name}, should be H:M:S")


def convert_to_date(date_text):
    """Convert a string to a date."""
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError as exc:
        raise ValueError(
            'Incorrect date format, should be YYYY-MM-DD') from exc


def convert_to_hour(hour_text):
    """Convert a string to a hour."""
    try:
        return datetime.strptime(hour_text, '%H:%M:%S')
    except ValueError as exc:
        raise ValueError('Incorrect hour format, should be H:M:S') from exc


def get_months_in_period(period):
    """Get the number of months in a period."""
    if period == "mensual":
        return 1
    elif period == "bimestral":
        return 2
    elif period == "trimestral":
        return 3
    elif period == "semestral":
        return 6
