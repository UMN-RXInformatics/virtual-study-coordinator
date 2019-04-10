from datetime import datetime, timedelta

from hammock import Hammock
import boto3
import json


redcap = Hammock('https://redcap.ahc.umn.edu/api/')


# --- UTILITY METHODS ---
def between(val, low, high):
    try:
        return float(val) >= low and float(val) <= high
    except Exception:
        return False


# --- REDCAP METHODS ---

def get_consents():
    instrument = 'consent'
    consent_responses = redcap.POST(data={
        'token': "enrollment redcap token",
        'content': 'record',
        'instrument': instrument,
        'type': 'flat',
        'format': 'json'
    }).json()

    consents = {item.get('record_id'): item.get('phone_number')
                for item in consent_responses
                if item.get('consent_complete') == '2'}

    return consents


def check_criteria(consents):
    instrument = 'eligibility'
    questionnaire_responses = redcap.POST(data={
        'token': "enrollment redcap token",
        'content': 'record',
        'instrument': instrument,
        'type': 'flat',
        'format': 'json',
        'exportSurveyFields': 'true'
    }).json()

    ids = [i
           for i in questionnaire_responses
           if i.get('record_id') in consents.keys()
           and i.get('is_eligible') == '1'
    ]

    return ids


def create_and_invite(phone_number):
    instrument = 'survey'

    next_id = redcap.POST(data={
        'token': "redcap ema token",
        'content': 'generateNextRecordName'
    }).json()

    data = json.dumps([{'record_id': next_id,
                        'phone_number': phone_number,
                        'invitation_timestamp': datetime.today().strftime("%Y-%m-%d %H:%M:%S")}])

    created = redcap.POST(data={
        'token': "redcap ema token",
        'content': 'record',
        'instrument': instrument,
        'type': 'flat',
        'format': 'json',
        'returnContent': 'ids',
        'data': data
    }).json()

    return created


def main():
    consents = get_consents()

    today = datetime.today()
    duration = timedelta(days=7) # includes current day since the dates start at midnight

    for crit in check_criteria(consents):
        if crit.get('start_date', '') != '':
            start_day = datetime.strptime(crit.get('start_date'), "%Y-%m-%d")
        else:
            continue

        if today > start_day and today < start_day + duration:
            c = create_and_invite(crit.get('phone_number'))
            print("Creating survey for {} at {}. Record {}.".format(
                consents[crit.get('record_id')],
                today.strftime("%Y-%m-%d %H:%M"),
                c[0]
            ))



if __name__ == "__main__":
    main()
