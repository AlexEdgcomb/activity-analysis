from datetime import datetime, date, time

class DateRange:
    def __init__(self, start_date, end_date):
        self.start_date = datetime.strptime(start_date, '%m-%d-%Y')
        self.end_date   = datetime.strptime(end_date, '%m-%d-%Y').replace(hour=23, minute=59, second=59)