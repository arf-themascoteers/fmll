from datetime import datetime

dt_string = "2024-05-27 11:00:00"
dt_object = datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')
epoch = int(dt_object.timestamp())*1000
print(epoch)

dt_string = "2024-08-14 11:00:00"
dt_object = datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')
epoch = int(dt_object.timestamp())*1000
print(epoch)