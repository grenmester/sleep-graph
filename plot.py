"""A convenient script to parse sleep times and plot statistics."""

import datetime as dt
import json
import os
import re
from collections import defaultdict

import click
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


def extract_sleep_data(json_file, org_file):
    """Extract sleep data from org file into JSON."""
    regex = r"  - (?:sleep|nap) 1?\d:[0-5]\d [ap]m - 1?\d:[0-5]\d [ap]m"
    with open(org_file, "r", encoding="utf8") as source:
        lines = source.readlines()
        date = ""
        data = defaultdict(list)
        for line in lines:
            # Date information
            if line.startswith("*"):
                date = line.strip("*").strip()
            # Sleep information
            elif date != "" and re.match(regex, line):
                split = line.split()
                sleep_type = split[1]
                start_time = split[2]
                start_period = split[3]
                end_time = split[5]
                end_period = split[6]
                start = dt.datetime.strptime(
                    f"{date} {start_time} {start_period}", "%b %d, %Y %I:%M %p"
                )
                end = dt.datetime.strptime(
                    f"{date} {end_time} {end_period}", "%b %d, %Y %I:%M %p"
                )
                # Takes care of cases where the end time is the next day
                if end < start:
                    end += dt.timedelta(days=1)
                data[sleep_type].append(
                    {
                        "start": start.strftime("%m/%d/%Y %H:%M"),
                        "end": end.strftime("%m/%d/%Y %H:%M"),
                    }
                )
        with open(json_file, "w", encoding="utf8") as output:
            json.dump(data, output)


@click.command()
@click.argument("json-file", type=click.Path())
@click.option(
    "-d",
    "--output-dir",
    default="output",
    type=click.Path(),
    help="Path to output directory.",
)
@click.option(
    "-o",
    "--org-file",
    default="",
    type=click.Path(),
    help="Path to org file with sleep data. If this option is "
    "provided, a JSON file with the name `JSON_FILE' will be "
    "generated and used. If this option is not provided, data will "
    "be read from `JSON_FILE'.",
)
def gen_plots(json_file, output_dir, org_file):
    """
    Given a JSON file containing sleep data, generate plots analyzing the data.
    The JSON file can be generated from an org file.
    """
    if org_file:
        extract_sleep_data(json_file, org_file)

    starts = {}
    ends = {}

    # Used to compute the mean number of sleep hours.
    first_day = dt.datetime(dt.MAXYEAR, 12, 31)
    last_day = dt.datetime(dt.MINYEAR, 1, 1)
    total_seconds = 0

    with open(json_file, "r", encoding="utf8") as data:
        # Load data and convert to datetime objects
        data = json.load(data)
        for k, v in data.items():
            starts[k] = []
            ends[k] = []
            for interval in v:
                start = dt.datetime.strptime(interval["start"], "%m/%d/%Y %H:%M")
                end = dt.datetime.strptime(interval["end"], "%m/%d/%Y %H:%M")
                assert start < end, "End time is earlier than start time"
                first_day = min(first_day, start)
                last_day = max(last_day, end)
                total_seconds += (end - start).seconds
                # Break up intervals so each interval is in one day
                while start.date() < end.date():
                    temp_end = dt.datetime(start.year, start.month, start.day, 23, 59)
                    starts[k].append(start)
                    ends[k].append(temp_end)
                    start -= dt.timedelta(
                        days=-1, hours=start.hour, minutes=start.minute
                    )
                starts[k].append(start)
                ends[k].append(end)

    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.8)

    for k in starts:
        mpl_starts = mdates.date2num(starts[k])
        mpl_ends = mdates.date2num(ends[k])
        start_times = mpl_starts % 1  # Extract time
        start_days = mpl_starts - start_times
        durations = mpl_ends - mpl_starts
        start_times += 1  # So we have a valid date

        ax.bar(
            start_days, durations, align="edge", bottom=start_times, width=0.9, zorder=3
        )

    padding = dt.timedelta(days=1)
    plt.xlim(first_day - padding, last_day + padding)
    plt.ylim(2, 1)
    plt.xlabel("Date")
    plt.ylabel("Time")
    plt.title("Sleep Times")

    ax.grid(linewidth=0.1, which="minor", zorder=0)
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d/%y"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_tick_params(rotation=30)
    ax.yaxis_date()
    ax.yaxis.set_major_formatter(mdates.DateFormatter("%I:%M %p"))
    ax.yaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.yaxis.set_minor_locator(mdates.HourLocator())

    num_days = (last_day - first_day).days
    total_minutes = round(total_seconds / (60 * num_days))
    mean_hours = total_minutes // 60
    mean_minutes = total_minutes % 60
    stats = f"Mean\nSleep Time:\n{mean_hours}h {mean_minutes}min"
    ax.text(1.15, 0.6, stats, horizontalalignment="center", transform=ax.transAxes)

    ax.legend(starts.keys(), bbox_to_anchor=(1.15, 0.5), loc="center")
    plt.savefig(os.path.join(output_dir, "graph.png"), bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    gen_plots()
