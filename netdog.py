import subprocess
import time
import datetime
import csv
from typing import Iterable, Any
import pytz


IP_ADDRESS = "8.8.8.8"
INTERVAL_SECONDS = 3

DOWNTIME_COUNTER = 0

OUTPUT_FILE: str = ""
EPOCH = datetime.datetime.utcfromtimestamp(0)

MAX_RETRIES = 2
RETRY_INTERVAL = .1

EST = pytz.timezone("US/Eastern")


def sleep():
    time.sleep(INTERVAL_SECONDS)


def current_time() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc).astimezone(EST)


def time_string(date: datetime.datetime) -> str:
    return date.strftime('%x %X')


def column_date(date: datetime.datetime) -> float:
    return date.timestamp() * 1000.0


def report_outage(
        start: datetime,
        end: datetime
):
    down_time_delta: datetime.timedelta = end - start
    down_time_seconds = down_time_delta.total_seconds()
    down_time_minutes = down_time_seconds / 60.0

    if down_time_seconds < 60:
        print()
        print()
        print()
        print()
        print(f"Outage lasted {down_time_seconds} seconds")
        print()
        print()
        print()
        print()

    else:
        print()
        print()
        print()
        print()
        print(f"Outage lasted {down_time_minutes} minutes")
        print()
        print()
        print()
        print()

    write_to_csv([time_string(start), time_string(end), down_time_seconds, down_time_minutes])


def internet_is_connected() -> bool:
    retries = 1
    succeeded = False
    try:
        subprocess.check_output(["ping", "-c", "1", IP_ADDRESS])
        succeeded = True
    except subprocess.CalledProcessError:
        while retries < MAX_RETRIES and not succeeded:
            time.sleep(RETRY_INTERVAL)
            succeeded = test_connection()
            retries = retries + 1

    return succeeded


def test_connection() -> bool:
    try:
        subprocess.check_output(["ping", "-c", "1", IP_ADDRESS])
        return True
    except subprocess.CalledProcessError:
        return False


def write_to_csv(row: Iterable[Any], mode='a'):
    with open(OUTPUT_FILE, mode, newline='') as file:
        writer = csv.writer(
            file,
            delimiter=','
        )
        writer.writerow(row)
        file.close()


def main():
    global OUTPUT_FILE

    file_name = current_time().strftime("%m_%d_%Y____%H_%M_%S")
    OUTPUT_FILE = f"/Users/matthewshoemaker/outages/{file_name}.csv"
    print(f"Created output file: {OUTPUT_FILE}")
    write_to_csv(['Start Time', "End Time", "Total Seconds", "Total Minutes"], "w+")

    while True:
        if not internet_is_connected():
            start_time = current_time()
            print(f"{time_string(start_time)} :: INTERNET DOWN")
            sleep()
            while not internet_is_connected():
                now = time_string(current_time())
                print(f"{now} :: INTERNET DOWN")
                sleep()

            end_time = current_time()
            report_outage(start_time, end_time)

        else:
            print(f"{time_string(current_time())} -- Internet is connected! :)")

        sleep()


if __name__ == '__main__':
    main()
