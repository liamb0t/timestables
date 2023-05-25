import datetime

def post_timestamp(date_posted):
    now = datetime.datetime.utcnow()
    time_diff = now - date_posted

    print(now, date_posted, time_diff)
    
    MINUTE = 60
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR
    WEEK = 7 * DAY
    MONTH = 30 * DAY
    YEAR = 365 * DAY

    # determine the closest time interval
    if time_diff.total_seconds() < MINUTE:
        time_since = 'Just now'
    elif MINUTE <= time_diff.total_seconds() < HOUR:
        time_since = f'{int(time_diff.total_seconds() / MINUTE)} m'
    elif HOUR <= time_diff.total_seconds() < DAY:
        time_since = f'{int(time_diff.total_seconds() / HOUR)} h'
    elif DAY <= time_diff.total_seconds() < WEEK:
        time_since = f'{int(time_diff.total_seconds() / DAY)} d'
    elif WEEK <= time_diff.total_seconds() < MONTH:
        time_since = f'{int(time_diff.total_seconds() / WEEK)} w'
    elif MONTH <= time_diff.total_seconds() < YEAR:
        time_since = f'{int(time_diff.total_seconds() / MONTH)} m'
    else:
        time_since = f'{int(time_diff.total_seconds() / YEAR)} y'
    return time_since


   