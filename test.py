import datetime

time = '22:43'
current = datetime.datetime.now()
current_time=current.strftime("%H:%M")
if(time <= current_time):
  print('Done')