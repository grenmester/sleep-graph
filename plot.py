import datetime as dt
import json


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
