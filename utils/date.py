import pytz

from datetime import datetime

def convert_utc_to_brt(utc_time_str):
    utc_timezone = pytz.utc
    brt_timezone = pytz.timezone('America/Sao_Paulo')

    utc_time = datetime.strptime(utc_time_str, '%Y-%m-%d %H:%M:%S')
    utc_time = utc_timezone.localize(utc_time)
    brt_time = utc_time.astimezone(brt_timezone)
    
    return brt_time.strftime('%d/%m/%Y %H:%M:%S')
