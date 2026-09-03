print("AI Traffic Signal System")

road_A = int(input("Road A par vehicles: "))
road_B = int(input("Road B par vehicles: "))
road_C = int(input("Road C par vehicles: "))
road_D = int(input("Road D par vehicles: "))

traffic = {
    "Road A": road_A,
    "Road B": road_B,
    "Road C": road_C,
    "Road D": road_D
}

for road, vehicles in traffic.items():

    if vehicles >= 30:
        green_time = 60
    elif vehicles >= 20:
        green_time = 40
    elif vehicles >= 10:
        green_time = 30
    else:
        green_time = 20

    print(road, "-> GREEN", green_time, "seconds")
