from datetime import datetime, timedelta

DAYS_PER_LOAD = 120 #For every run, loads X days
DAYS_PER_UPDATE = 60
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

def Is_Today(date:str):
    return date == datetime.today().strftime(DEFAULT_DATE_FORMAT)

def Get_Extraction_Date_Range(last_date:str):
    last_date = datetime.strptime(last_date, DEFAULT_DATE_FORMAT)
    yesterday = datetime.today() - timedelta(days=1)

    # If the last loaded date was today or yesterday, then load last X days including today
    if last_date >= yesterday:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=DAYS_PER_UPDATE)
    # Else load that date and the next X days
    else:
        start_date = last_date
        end_date = start_date + timedelta(days=DAYS_PER_LOAD)
        if end_date > datetime.today(): end_date = datetime.today()

    return {
        'start_date': start_date.strftime(DEFAULT_DATE_FORMAT), 
        'end_date': end_date.strftime(DEFAULT_DATE_FORMAT)
    }