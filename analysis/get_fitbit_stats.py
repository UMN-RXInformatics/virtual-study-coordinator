from time import localtime, strftime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import glob

def get_sevens(subject_id):
    f = open('data/{}-7s.dat'.format(subject_id))
    lines = f.readlines()
    descriptor = lines[0].split('|')
    end = descriptor # strftime("%Y-%m-%d %H:%M:%S", localtime(int(lines[-2].split('|')[0])/1000))

    return pd.Series(["{} {}".format(descriptor[1], descriptor[2]), end], index=['Event Time', 'End'])

def get_vf(subject_id):
    # 46-2018-04-02_20-41-19_Animals-vf
    poss = glob.glob('data/{}-*_A-vf.wav'.format(subject_id))
    res = poss[0].split('/')[1]
    return pd.Series(["{} {}".format(res[3:13], res[14:22].replace('-',':'))], index=['Event Time'])

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
    subject = 52 # subject number from study
    interp = True
    active_thresh = 10 / 60
    window_before = 10
    window_after = 10

    if interp:
        h_df = get_heart(subject, interpolate=True)
        s_df = get_steps(subject, interpolate=True)
        e_df = get_elevation(subject, interpolate=True)
        ema = get_ema(subject)
        exams = get_exams(subject)
        try:
            sevens = get_sevens(subject)
            sevens_begin, sevens_end = sevens
        except Exception as e:
            sevens = None

        try:
            vf = get_vf(subject)
            vf_begin = vf[0]
        except Exception as e:
            vf = None

        h_df = h_df.rolling(window=60).mean()
        s_df = s_df.rolling(window=600).mean()
        e_df = e_df.rolling(window=600).mean()

        s_active = s_df[s_df.ge(active_thresh)['Steps']] # number of steps per second for 10 steps per min
        s_passive = s_df[s_df.lt(active_thresh)['Steps']]
        h_active = h_df[s_df.ge(active_thresh)['Steps']]
        h_passive = h_df[s_df.lt(active_thresh)['Steps']]
        e_active = e_df[s_df.ge(active_thresh)['Steps']]
        e_passive = e_df[s_df.lt(active_thresh)['Steps']]

    else:
        h_df = get_heart(subject)
        s_df = get_steps(subject)
        e_df = get_elevation(subject)
        ema = get_ema(subject)
        exams = get_exams(subject)
        sevens = get_sevens(subject)
        sevens_begin, sevens_end = sevens

        s_active = s_df.copy()
        s_passive = s_df.copy()
        h_active = h_df.copy()
        h_passive = h_df.copy()
        e_active = e_df.copy()
        e_passive = e_df.copy()

    baseline = []
    h_stats = []
    s_stats = []
    e_stats = []
    ema_list = []

    # ADD EMAS TO LIST OF EVENTS
    for idx, record in ema.iterrows():
        if record['EMA Stress'] == 0:
            time = pd.to_datetime(record['EMA Time'], format='%Y-%m-%d %H:%M:%S')
        else:
            time = pd.to_datetime(record['Event Time'], format='%Y-%m-%d %H:%M:%S')
        ema_start = time - pd.to_timedelta(record['Period'])
        before = pd.Timedelta(minutes=window_before)
        after = pd.Timedelta(minutes=window_after)
        begin = time - before
        end = time + after

        if record['EMA Stress'] == 0:
            baseline.append(h_passive[ema_start:time])
        else:
            h_stats.append(h_passive[begin:time].describe())
            record['Window'] = 'Before'
            ema_list.append(record.copy())

            h_stats.append(h_passive[time:end].describe())
            record['Window'] = 'After'
            ema_list.append(record.copy())

            h_stats.append(h_passive[begin:end].describe())
            record['Window'] = 'Combined'
            ema_list.append(record.copy())

    # ADD EXAMS TO LIST OF EVENTS
    exams.rename(columns={'Unnamed: 0': 'Event Time', 'Exam': 'EMA Stress'}, inplace=True)
    for idx, record in exams.iterrows():
        time = pd.to_datetime(record['Event Time'], format='%Y-%m-%d %H:%M:%S')
        before = pd.Timedelta(minutes=window_before)
        after = pd.Timedelta(minutes=window_after)
        begin = time - before
        end = time + after

        record['Number'] = 1
        record['Stress Type'] = -1

        h_stats.append(h_passive[begin:time].describe())
        record['Window'] = 'Before'
        ema_list.append(record.copy())

        h_stats.append(h_passive[time:end].describe())
        record['Window'] = 'After'
        ema_list.append(record.copy())

        h_stats.append(h_passive[begin:end].describe())
        record['Window'] = 'Combined'
        ema_list.append(record.copy())

    # ADD SEVENS TASK TO LIST OF EVENTS
    if sevens is not None:
        time = pd.to_datetime(sevens_begin, format='%Y-%m-%d %H:%M:%S')
        begin = pd.to_datetime(sevens_begin, format='%Y-%m-%d %H:%M:%S')
        end = begin + pd.Timedelta(minutes=2)
        print(begin, end)
        sevens['Number'] = 1
        sevens['Stress Type'] = -7
        sevens['EMA Stress'] = 1

        h_stats.append(h_passive[begin:time].describe())
        sevens['Window'] = 'Before'
        ema_list.append(sevens.copy())

        h_stats.append(h_passive[time:end].describe())
        sevens['Window'] = 'After'
        ema_list.append(sevens.copy())

        h_stats.append(h_passive[begin:end].describe())
        sevens['Window'] = 'Combined'
        ema_list.append(sevens.copy())

    # ADD VF TASK TO LIST OF EVENTS
    if vf is not None:
        time = pd.to_datetime(vf_begin, format='%Y-%m-%d %H:%M:%S')
        begin = pd.to_datetime(vf_begin, format='%Y-%m-%d %H:%M:%S')
        end = begin + pd.Timedelta(minutes=3)
        print(begin, end)
        vf['Number'] = 1
        vf['Stress Type'] = -8
        vf['EMA Stress'] = 1

        h_stats.append(h_passive[begin:time].describe())
        vf['Window'] = 'Before'
        ema_list.append(vf.copy())

        h_stats.append(h_passive[time:end].describe())
        vf['Window'] = 'After'
        ema_list.append(vf.copy())

        h_stats.append(h_passive[begin:end].describe())
        vf['Window'] = 'Combined'
        ema_list.append(vf.copy())


    # CALCULATE BASELINE FROM PASSIVE HEARTRATE EMA
    baseline = pd.concat(baseline)
    print(baseline.describe())
    baseline = baseline.mean().mean()

    # ASSEMBLE HEARTRATE STATS
    h_ema = pd.concat(h_stats,
                      axis=1,
                      ignore_index=True).unstack().unstack(level=-1)

    # ASSOCIATE HEARTRATES WITH STRESS EVENTS
    emas = pd.concat(ema_list, axis=1, ignore_index=True).unstack().unstack(level=-1)

    # ASSEMBLE FINAL DATAFRAME FOR CSV OUTPUT
    out = pd.concat(
        [emas[['EMA Stress', 'Event Time', 'Number', 'Stress Type', 'Window']],
         h_ema], axis=1).sort_values(by='Event Time')

    out['Baseline'] = baseline
    out.to_csv('result/{0}/{0}-ema-stats.csv'.format(subject),
               index=False)
