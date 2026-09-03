def calculate_green_time(vehicles):
    if vehicles >= 30:
        return 60
    elif vehicles >= 20:
        return 40
    elif vehicles >= 10:
        return 30
    else:
        return 20
