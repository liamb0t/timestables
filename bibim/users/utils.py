import datetime

def date_member_since(date_joined):
    join_date = date_joined.date()
    today = datetime.date.today()

    delta = today - join_date
    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = delta.days 

    if years > 0:
        time_string = f"Member for {years}, {months} months"
    elif years == 0 and months > 0:
        time_string = f"Member for {months} months"
    elif days <= 1:
        time_string = "Member since today"
    else:
        time_string = f"Member for {days} days"

    return time_string