import datetime

def datetime_to_describe(time_strp):
    y,m,d,h,min = [int(i) for i in time_strp.split("-")]
    time = datetime.datetime(y,m,d,h,min)
    # weekday_id = datetime.datetime.today().weekday()
    # day_of_week_list = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
    # weekday = day_of_week_list[weekday_id]
    return time.strftime('%Y年%m月%d日 %H時%M分')