from time import localtime, strftime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def get_sevens(subject_id):
    f = open('data/{}-7s.dat'.format(subject_id))
    lines = f.readlines()
    descriptor = lines[0].split('|')
    end = descriptor # strftime("%Y-%m-%d %H:%M:%S", localtime(int(lines[-2].split('|')[0])/1000))

    return pd.Series(["{} {}".format(descriptor[1], descriptor[2]), end], index=['Event Time', 'End'])


def get_heart(subject_id, interpolate=False):
    if interpolate:
        return pd.read_csv('result/{0}/{0}-heartrate.csv'.format(subject_id),
                           parse_dates=True,
                           index_col=0).resample('1S').interpolate(method='time')
    else:
        return pd.read_csv('result/{0}/{0}-heartrate.csv'.format(subject_id),
                           parse_dates=True,
                           index_col=0)


def get_steps(subject_id, interpolate=False):
    if interpolate:
        return pd.read_csv('result/{0}/{0}-steps.csv'.format(subject_id),
                           parse_dates=True,
                           index_col=0).applymap(lambda x: x if x > 10 else 0).resample('1S').bfill() / 60
    else:
        return pd.read_csv('result/{0}/{0}-steps.csv'.format(subject_id),
                           parse_dates=True,
                           index_col=0)


def get_elevation(subject_id, interpolate=False):
    if interpolate:
        return pd.read_csv('result/{0}/{0}-elevation.csv'.format(subject_id),
                           parse_dates=True,
                           index_col=0).applymap(lambda x: x if x > 2 else 0).resample('1S').bfill() / 60
    else:
        return pd.read_csv('result/{0}/{0}-elevation.csv'.format(subject_id),
                           parse_dates=True,
                           index_col=0)

def get_ema(subject_id):
    return pd.read_csv('result/{0}/{0}-ema.csv'.format(subject_id),
                       parse_dates=True)

def get_exams(subject_id):
    return pd.read_csv('result/{0}/{0}-exams.csv'.format(subject_id),
                       parse_dates=True)


if __name__ == "__main__":
    subjects = [6, 16, 17, 20, 22, 32, 34, 43] # list of subject numbers from study
    interp = True
    active_thresh = 10 / 60
    h_unstressed = []
    us_window_list = []
    h_stressed = []
    s_window_list = []


    for subject in subjects:
        h_df = get_heart(subject, interpolate=True)
        s_df = get_steps(subject, interpolate=True)
        e_df = get_elevation(subject, interpolate=True)
        ema = get_ema(subject)
        exams = get_exams(subject)
        sevens = get_sevens(subject)
        sevens_begin, sevens_end = sevens

        h_df = h_df.rolling(window=60).mean()
        s_df = s_df.rolling(window=600).mean()
        e_df = e_df.rolling(window=600).mean()

        s_active = s_df[s_df.ge(active_thresh)['Steps']] # number of steps per second for 10 steps per min
        s_passive = s_df[s_df.lt(active_thresh)['Steps']]
        h_active = h_df[s_df.ge(active_thresh)['Steps']]
        h_passive = h_df[s_df.lt(active_thresh)['Steps']]
        e_active = e_df[s_df.ge(active_thresh)['Steps']]
        e_passive = e_df[s_df.lt(active_thresh)['Steps']]



        # ADD EMAS TO LIST OF EVENTS
        for idx, record in ema.iterrows():
            if record['EMA Stress'] == 0:
                time = pd.to_datetime(record['EMA Time'], format='%Y-%m-%d %H:%M:%S')
            else:
                time = pd.to_datetime(record['Event Time'], format='%Y-%m-%d %H:%M:%S')

            ema_start = time - pd.to_timedelta(record['Period'])
            window = pd.Timedelta(minutes=10)
            before = window
            after = window
            half_frame = window / 2
            begin = time - before
            end = time + after

            if record['EMA Stress'] == 0:
                curr = ema_start
                while curr + window <= time:
                    frame = h_df[curr:curr + window].reset_index()['HeartRate']
                    if len(frame) == 601 and frame.sum() > 0:
                        h_unstressed.append(frame)
                        r = record.copy()
                        r['Type'] = 'unstressed'
                        r['Subject'] = subject
                        r['Window'] = curr
                        r['Window'] = curr # some sort of bug in pandas makes this necessary
                        us_window_list.append(r)
                    curr += half_frame

            else:
                curr = begin - half_frame
                while curr + window <= end + half_frame:
                    frame = h_df[curr:curr + window].reset_index()['HeartRate']
                    if len(frame) == 601 and frame.sum() > 0:
                        h_stressed.append(frame)
                        r = record.copy()
                        r['Type'] = 'stressed'
                        r['Subject'] = subject
                        r['Window'] = curr
                        r['Window'] = curr # some sort of bug in pandas makes this necessary
                        s_window_list.append(r)
                    curr += half_frame

    # MAIN

    us_windows = pd.concat(us_window_list, axis=1, ignore_index=True).unstack().unstack(level=-1)
    print(us_windows[['Subject', 'Window']])
    h_unstressed = pd.concat(h_unstressed, axis=1, ignore_index=True).T
    all_unstressed = pd.concat([us_windows[['Window', 'Type', 'Subject']], h_unstressed], axis=1)

    s_windows = pd.concat(s_window_list, axis=1, ignore_index=True).unstack().unstack(level=-1)
    h_stressed = pd.concat(h_stressed, axis=1, ignore_index=True).T
    all_stressed = pd.concat([s_windows[['Window', 'Type', 'Subject']], h_stressed], axis=1)

    all_tensor = pd.concat([all_stressed, all_unstressed]).sort_values(by=['Subject', 'Window'])
    # print(all_tensor)
    all_tensor.to_csv('result/tensors.csv', index=False)
