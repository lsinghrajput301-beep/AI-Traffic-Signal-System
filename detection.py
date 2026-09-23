from ultralytics import YOLO
import cv2

# YOLO model load
model = YOLO("yolo11n.pt")

# Camera start
cap = cv2.VideoCapture(0)

# Vehicle classes
vehicle_classes = {
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    7: "Truck"
}

print("YOLO model loaded.")
print("Camera started.")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera open nahi ho raha!")
        break

    # Frame size
    height, width = frame.shape[:2]

    # YOLO detection
    results = model(frame, verbose=False)

    # Road counts
    road_a = 0
    road_b = 0
    road_c = 0
    road_d = 0

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            # Sirf vehicles detect karo
            if class_id in vehicle_classes and confidence > 0.40:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Vehicle ka center point
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # 4 roads ke hisaab se count
                if center_x < width // 2 and center_y < height // 2:
                    road_a += 1
                    road_name = "Road A"

                elif center_x >= width // 2 and center_y < height // 2:
                    road_b += 1
                    road_name = "Road B"

                elif center_x < width // 2 and center_y >= height // 2:
                    road_c += 1
                    road_name = "Road C"

                else:
                    road_d += 1
                    road_name = "Road D"

                # Bounding box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # Vehicle name
                vehicle_name = vehicle_classes[class_id]

                cv2.putText(
                    frame,
                    f"{vehicle_name} - {road_name}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

    # --------------------------------
    # Draw road dividing lines
    # --------------------------------

    cv2.line(
        frame,
        (width // 2, 0),
        (width // 2, height),
        (255, 255, 255),
        2
    )

    cv2.line(
        frame,
        (0, height // 2),
        (width, height // 2),
        (255, 255, 255),
        2
    )

    # Road names
    cv2.putText(
        frame,
        "ROAD A",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "ROAD B",
        (width // 2 + 20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "ROAD C",
        (20, height // 2 + 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "ROAD D",
        (width // 2 + 20, height // 2 + 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # --------------------------------
    # Display vehicle counts
    # --------------------------------

    cv2.putText(
        frame,
        f"Road A: {road_a}",
        (20, height - 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Road B: {road_b}",
        (width // 2 + 20, height - 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Road C: {road_c}",
        (20, height - 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Road D: {road_d}",
        (width // 2 + 20, height - 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    # Total vehicles
    total = road_a + road_b + road_c + road_d

    cv2.putText(
        frame,
        f"Total Vehicles: {total}",
        (20, height - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    # Show camera
    cv2.imshow("AI Traffic - Road Vehicle Counting", frame)

    # Q press = exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()