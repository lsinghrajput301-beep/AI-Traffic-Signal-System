# traffic_signal.py

def calculate_green_time(vehicles):
    """
    Vehicle count के हिसाब से Green Time तय करता है.
    """

    if vehicles >= 30:
        return 60
    elif vehicles >= 20:
        return 40
    elif vehicles >= 10:
        return 30
    else:
        return 20


def get_traffic_level(vehicles):
    """
    Traffic level बताता है.
    """

    if vehicles >= 30:
        return "VERY HIGH TRAFFIC"
    elif vehicles >= 20:
        return "HIGH TRAFFIC"
    elif vehicles >= 10:
        return "MEDIUM TRAFFIC"
    else:
        return "LOW TRAFFIC"


def select_next_road(traffic):
    """
    सबसे ज्यादा vehicles वाली road चुनता है.
    """

    return max(traffic, key=traffic.get)


def create_signal_status(active_road, roads):
    """
    Active road = GREEN
    बाकी roads = RED
    """

    signal_status = {}

    for road in roads:
        if road == active_road:
            signal_status[road] = "GREEN"
        else:
            signal_status[road] = "RED"

    return signal_status