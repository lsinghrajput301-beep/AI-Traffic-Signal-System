from traffic_signal import calculate_green_time

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

print("\n--- Automatic Signal Timing ---")

for road, vehicles in traffic.items():
    green_time = calculate_green_time(vehicles)

    print(
        road,
        "->",
        vehicles,
        "vehicles -> GREEN",
        green_time,
        "seconds"
    )
