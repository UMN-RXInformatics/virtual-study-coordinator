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


def num(s):
    try:
        return float(s)
    except ValueError:
        return 0.0

def get_stressors(subject_id):
    q_r = redcap.POST(data={
        'token': config['redcap_fitbit_key'],
        'content': 'record',
        'instrument': 'eligibility',
        'type': 'flat',
        'format': 'json',
        'exportSurveyFields': 'true',
        'records': [subject_id]
    }).json()[0]

    ema = redcap.POST(data={
        'token': config['redcap_fitbit_survey_key'],
        'content': 'record',
        'instrument': 'survey',
        'type': 'flat',
        'format': 'json',
        'exportSurveyFields': 'true',
        'filterLogic': '[phone_number] = "{}"'.format(q_r['phone_number'])
    }).json()

    time = [
        pd.to_datetime(s['survey_timestamp'], format='%Y-%m-%d %H:%M:%S')
        for s in ema if s['stress_happened'] == '1' or s['stress_happened'] == '0'
    ]

    begin_time = [
        min(abs(t - time[time.index(t)-1]), pd.Timedelta('4 hours 24 minutes')) for t in time
    ]

    self_time = [
        pd.to_datetime(s['stress_time'], format='%Y-%m-%d %H:%M')
        for s in ema if s['stress_happened'] == '1' or s['stress_happened'] == '0'
    ]

    stress_value = [
        num(s['stress_magnitude'])
        for s in ema if s['stress_happened'] == '1' or s['stress_happened'] == '0'
    ]

    stress_type = [
        s['stress_type']
        for s in ema if s['stress_happened'] == '1' or s['stress_happened'] == '0'
    ]

    stress_number = [
        s['stress_number']
        for s in ema if s['stress_happened'] == '1' or s['stress_happened'] == '0'
    ]


    ema_df = pd.DataFrame({
        'Period': begin_time,
        'EMA Time': time,
        'Event Time': self_time,
        'Number': stress_number,
        'EMA Stress': stress_value,
        'Stress Type': stress_type})

    ema_df.to_csv('result/{0}/{0}-ema.csv'.format(subject_id), index=False)

if __name__ == "__main__":
    for x in [46, 52, 54, 56, 57, 58, 60, 61, 62, 64, 69, 71]:
        get_stressors(x)
