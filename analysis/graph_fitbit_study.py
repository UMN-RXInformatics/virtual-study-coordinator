import json
import pathlib
import pickle

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from hammock import Hammock
redcap = Hammock('https://redcap.ahc.umn.edu/api/')
config = {
    "redcap_fitbit_key": "enrollment key here",
    "redcap_fitbit_survey_key": "ema key here"
}


def get_sevens(subject_id):
    f = open('data/{}-7s.dat'.format(subject_id))
    descriptor = f.readline().split('|')

    return pd.to_datetime(
        "{} {}".format(descriptor[1], descriptor[2]),
        format='%Y-%m-%d %H:%M:%S')


def get_heart(subject_id):
    f = open('data/{}-fitbit.dat'.format(subject_id))
    j = json.loads(f.read())

    times = [
        [
            pd.to_datetime(
                h['activities-heart'][0]['dateTime'] + ' ' + t['time'],
                format='%Y-%m-%d %H:%M:%S')
            for t in h.get('activities-heart-intraday')['dataset']]
        for h in j if h.get('activities-heart-intraday')
    ]

    values = [
        [
            t['value']
            for t in h.get('activities-heart-intraday')['dataset']]
        for h in j if h.get('activities-heart-intraday')
    ]

    frames = []

    for n, v in enumerate(times):
        frames.append(
            pd.DataFrame(values[n], columns=['HeartRate'], index=times[n]))

    return pd.concat(frames)


def get_steps(subject_id):
    f = open('data/{}-fitbit.dat'.format(subject_id))
    j = json.loads(f.read())

    times = [
        [
            pd.to_datetime(
                h['activities-steps'][0]['dateTime'] + ' ' + t['time'],
                format='%Y-%m-%d %H:%M:%S')
            for t in h.get('activities-steps-intraday')['dataset']]
        for h in j if h.get('activities-steps-intraday')
    ]

    values = [
        [
            t['value']
            for t in h.get('activities-steps-intraday')['dataset']]
        for h in j if h.get('activities-steps-intraday')
    ]

    frames = []

    for n, v in enumerate(times):
        frames.append(
            pd.DataFrame(values[n], columns=['Steps'], index=times[n]))

    return pd.concat(frames)

def get_elevation(subject_id):
    f = open('data/{}-fitbit.dat'.format(subject_id))
    j = json.loads(f.read())

    times = [
        [
            pd.to_datetime(
                h['activities-elevation'][0]['dateTime'] + ' ' + t['time'],
                format='%Y-%m-%d %H:%M:%S')
            for t in h.get('activities-elevation-intraday')['dataset']]
        for h in j if h.get('activities-elevation-intraday')
    ]

    values = [
        [
            t['value']
            for t in h.get('activities-elevation-intraday')['dataset']]
        for h in j if h.get('activities-elevation-intraday')
    ]

    frames = []

    for n, v in enumerate(times):
        frames.append(
            pd.DataFrame(values[n], columns=['Elevation'], index=times[n]))

    return pd.concat(frames)


def get_stressors(subject_id):
    print(subject_id)
    q_r = redcap.POST(data={
        'token': config['redcap_fitbit_key'],
        'content': 'record',
        'instrument': 'eligibility',
        'type': 'flat',
        'format': 'json',
        'exportSurveyFields': 'true',
        'records': [subject_id]
    }).json()[0]

    exam_times = [
        pd.to_datetime(q_r['exam_{}'.format(i)], format='%Y-%m-%d %H:%M')
        for i in range(1, 8) if q_r.get('exam_{}'.format(i))
    ]

    exam_values = [
        float(q_r['exam_stress_{}'.format(i)])
        for i in range(1, 8) if q_r.get('exam_{}'.format(i))
    ]

    ema = redcap.POST(data={
        'token': config['redcap_fitbit_survey_key'],
        'content': 'record',
        'instrument': 'survey',
        'type': 'flat',
        'format': 'json',
        'exportSurveyFields': 'true',
        'filterLogic': '[phone_number] = "{}"'.format(q_r['phone_number'])
    }).json()

    all_times = [
        (s['stress_happened'], pd.to_datetime(s['survey_timestamp'], format='%Y-%m-%d %H:%M:%S'))
        for s in ema if s['stress_happened'] == '1' or s['stress_happened'] == '0'
    ]

    stress_times = [
        pd.to_datetime(s['survey_timestamp'], format='%Y-%m-%d %H:%M:%S')
        for s in ema if s['stress_happened'] == '1'
    ]

    widths = [
        max((all_times[all_times.index(t)-1][1] - t[1]).total_seconds()/60/60/24, -4.4/24.0)
        for t in all_times if t[0] == '1'
    ]

    self_stress = [
        pd.to_datetime(s['stress_time'], format='%Y-%m-%d %H:%M')
        for s in ema if s['stress_happened'] == '1'
    ]

    stress_values = [
        float(s['stress_magnitude'])
        for s in ema if s['stress_happened'] == '1'
    ]

    stress_types = [
        s['stress_type']
        for s in ema if s['stress_happened'] == '1'
    ]

    return self_stress, {'stress': widths, 'exam': [2.5/24.0]*len(exam_times)}, pd.DataFrame({'EMA Stress': stress_values, 'Stress Type': stress_types}, index=stress_times), pd.DataFrame(exam_values, columns=['Exam'], index=exam_times)


if __name__ == "__main__":
    subjects = [58] # list of subject numbers from study
    for subject in subjects:
        fig, ax = plt.subplots()

        h_df = get_heart(subject)
        s_df = get_steps(subject)
        e_df = get_elevation(subject)
        self_stress, widths, stressors, exams = get_stressors(subject)

        ax.bar(stressors.index, stressors['EMA Stress'], widths['stress'], alpha=.5, align='edge')
        ax.bar(exams.index, exams['Exam'], widths['exam'], alpha=.5, align='edge')
        ax.plot(s_df.index, s_df.rolling(window=5).mean()['Steps'], color='g', alpha=.7)
        ax.plot(e_df.index, e_df.rolling(window=5).mean()['Elevation'] * 5, color='k', alpha=.7)
        h_df.rolling(window=60).mean().plot(ax=ax, color='r', secondary_y=True)
        for d in self_stress:
            ax.axvline(d, ls='--', color='b')
        try:
            ax.axvline(get_sevens(subject), ls='-.', color='m')
        except Exception as e:
            pass

        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_minor_locator(mdates.HourLocator())

        study_days = pd.PeriodIndex(h_df.index.to_period('D'))
        study_days = study_days.groupby(study_days)

        pathlib.Path('result/{}'.format(subject)).mkdir(parents=True, exist_ok=True)
        fig.savefig('result/{}/{}-full.png'.format(subject, subject),
                    transparent=False, dpi=300, bbox_inches="tight")
        # plt.clf()
        # pickle.dump(fig, open('result/{}/{}.pickle'.format(subject, subject), 'wb'))

        # for n, day in enumerate(study_days):
        #     ax.set_xlim(day.start_time, day.end_time)

        #     fig.savefig('result/{}/{}-{}.png'.format(subject, subject, n),
        #                 transparent=False, dpi=300, bbox_inches="tight")


        # e_df.to_csv('result/{}/{}-elevation.csv'.format(subject, subject))
        # s_df.to_csv('result/{}/{}-steps.csv'.format(subject, subject))
        # h_df.to_csv('result/{}/{}-heartrate.csv'.format(subject, subject))
        # stressors.to_csv('result/{}/{}-stressors.csv'.format(subject, subject))
        # exams.to_csv('result/{}/{}-exams.csv'.format(subject, subject))

        plt.show()
        # print(j[0]['activities-heart-intraday']['dataset'])
