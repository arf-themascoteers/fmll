def hours_difference(epoch1, epoch2):
    milliseconds_in_an_hour = 3600 * 1000
    difference_in_milliseconds = abs(epoch1 - epoch2)
    difference_in_hours = difference_in_milliseconds / milliseconds_in_an_hour
    return difference_in_hours

epoch1 = 1716854905922
epoch2 = 1717544904428

print(hours_difference(epoch1, epoch2))
