from datetime import datetime, timedelta

today = datetime.today()
yesterday = today - timedelta(days=1)

formatted_date = yesterday.strftime("%d/%m/%Y")

FROM = formatted_date
TO = formatted_date
