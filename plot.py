import click
import datetime as dt
import json
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import os


def extract_sleep_data(json_file, org_file):
    '''Extract sleep data from org file into JSON.'''
    with open(org_file, 'r') as source:
        lines = source.readlines()
        date = ''
        data = {'sleep': [], 'nap': []}
        for line in lines:
            # Date information
            if line.startswith('*'):
                date = line.strip('*').strip()
            # Sleep information
            elif ('  - sleep' in line or '  - nap' in line) and date is not '':
                split = line.split()
                sleep_type = split[1]
                start_time = split[2]
                start_period = split[3]
                end_time = split[5]
                end_period = split[6]
                start = dt.datetime.strptime(
                    f'{date} {start_time} {start_period}', '%b %d, %Y %I:%M %p')
                end = dt.datetime.strptime(
                    f'{date} {end_time} {end_period}', '%b %d, %Y %I:%M %p')
                # Takes care of cases where the end time is the next day
                if end < start:
                    end += dt.timedelta(days=1)
                data[sleep_type].append({
                    'start': start.strftime('%m/%d/%Y %H:%M'),
                    'end': end.strftime('%m/%d/%Y %H:%M')
                })
        with open(json_file, 'w') as output:
            json.dump(data, output)


@click.command()
@click.argument('json-file', type=click.Path())
@click.option('-d', '--output-dir', default='output', type=click.Path(),
              help='Path to output directory.')
@click.option('-o', '--org-file', default='', type=click.Path(),
              help='Path to org file with sleep data. If this option is '
              'provided, a JSON file with the name `JSON_FILE\' will be '
              'generated and used. If this option is not provided, data will '
              'be read from `JSON_FILE\'.')
def gen_plots(json_file, output_dir, org_file):
    '''
    Given a JSON file containing sleep data, generate plots analyzing the data.
    The JSON file can be generated from an org file.
    '''
    if org_file:
        extract_sleep_data(json_file, org_file)

    starts = {}
    ends = {}

    with open(json_file, 'r') as data:
        # Load data and convert to datetime objects
        data = json.load(data)
        for k, v in data.items():
            starts[k] = []
            ends[k] = []
            for interval in v:
                start = dt.datetime.strptime(
                    interval['start'], '%m/%d/%Y %H:%M')
                end = dt.datetime.strptime(interval['end'], '%m/%d/%Y %H:%M')
                assert start < end, 'End time is earlier than start time'
                # Break up intervals so each interval is in one day
                while start.day < end.day:
                    temp_end = dt.datetime(
                        start.year, start.month, start.day, 23, 59)
                    starts[k].append(start)
                    ends[k].append(temp_end)
                    start -= dt.timedelta(days=-1, hours=start.hour,
                                          minutes=start.minute)
                starts[k].append(start)
                ends[k].append(end)

    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots()

    for k in starts.keys():
        mpl_starts = mdates.date2num(starts[k])
        mpl_ends = mdates.date2num(ends[k])
        start_times = mpl_starts % 1  # Extract time
        start_days = mpl_starts - start_times
        durations = mpl_ends - mpl_starts
        start_times += 1  # So we have a valid date

        ax.bar(start_days, durations, bottom=start_times, zorder=3)

    plt.xlabel('Date')
    plt.ylabel('Time')
    plt.title('Sleep Times')
    ax.grid(which='minor', zorder=0)
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_tick_params(rotation=30)
    ax.yaxis_date()
    ax.yaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
    ax.yaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.yaxis.set_minor_locator(mdates.HourLocator())
    plt.legend(starts.keys())
    plt.savefig(os.path.join(output_dir, 'graph.png'))
    plt.show()


if __name__ == '__main__':
    gen_plots()
