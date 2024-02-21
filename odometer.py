import speedtest
import pytz
import datetime
import time
import csv
from typing import Iterable, Any

OUTPUT_FILE: str = ""

EST = pytz.timezone("US/Eastern")

INTERVAL_MINUTES = 15
INTERVAL_SECONDS = INTERVAL_MINUTES * 60


def sleep():
    time.sleep(INTERVAL_SECONDS)


def current_time() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc).astimezone(EST)


def time_string(date: datetime.datetime) -> str:
    return date.strftime('%x %X')


def column_date(date: datetime.datetime) -> float:
    return date.timestamp() * 1000.0


def write_to_csv(row: Iterable[Any], mode='a'):
    with open(OUTPUT_FILE, mode, newline='') as file:
        writer = csv.writer(
            file,
            delimiter=','
        )
        writer.writerow(row)
        file.close()


def mbps(bits: float) -> float:
    return bits / 1_000_000.0


def main():
    global OUTPUT_FILE

    file_name = current_time().strftime("%m_%d_%Y____%H_%M_%S")
    OUTPUT_FILE = f"/Users/matthewshoemaker/odometer/{file_name}.csv"
    print(f"\nCreated output file: {OUTPUT_FILE}\n")
    write_to_csv(['Time', "Download (Mbps)", "Upload (Mbps)"], "w+")

    while True:
        try:
            print(f"{time_string(current_time())}: Starting speed test....")
            st = speedtest.Speedtest()
            download_speed = mbps(st.download())
            upload_speed = mbps(st.upload())
            write_to_csv([time_string(current_time()), download_speed, upload_speed])

            print(f"    Download Speed: \t{str(round(download_speed, 2))} Mbps")
            print(f"      Upload Speed: \t{str(round(upload_speed, 2))} Mbps")
        except Exception as e:
            print(f"Speed test failed!")
            print(e)

        print(f"\nWaiting {INTERVAL_MINUTES} minutes before checking again...\n")

        sleep()


if __name__ == '__main__':
    main()
