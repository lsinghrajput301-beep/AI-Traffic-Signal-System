import cv2
import time
from ultralytics import YOLO

from traffic_signal import (
    calculate_green_time,
    get_traffic_status
)


# =========================================================
# YOLO MODEL
# =========================================================

model = YOLO("yolo11n.pt")


# =========================================================
# VEHICLE CLASSES
# =========================================================

VEHICLE_CLASSES = {
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    7: "Truck"
}


# =========================================================
# VEHICLE COUNT
# =========================================================

vehicle_count = {
    "Car": 0,
    "Motorcycle": 0,
    "Bus": 0,
    "Truck": 0
}


# =========================================================
# TRACKING
# =========================================================

counted_ids = set()
previous_positions = {}


# =========================================================
# SIGNAL SETTINGS
# =========================================================

signal_state = "RED"

signal_start_time = time.time()

green_time = 20
yellow_time = 5
red_time = 5


# =========================================================
# UPDATE TRAFFIC SIGNAL
# =========================================================

def update_signal(total):

    global signal_state
    global signal_start_time
    global green_time

    # Vehicle count के हिसाब से green time
    green_time = calculate_green_time(total)

    current_time = time.time()

    elapsed = current_time - signal_start_time

    # RED → GREEN
    if signal_state == "RED":

        if elapsed >= red_time:

            signal_state = "GREEN"
            signal_start_time = current_time

    # GREEN → YELLOW
    elif signal_state == "GREEN":

        if elapsed >= green_time:

            signal_state = "YELLOW"
            signal_start_time = current_time

    # YELLOW → RED
    elif signal_state == "YELLOW":

        if elapsed >= yellow_time:

            signal_state = "RED"
            signal_start_time = current_time


# =========================================================
# DRAW TRAFFIC LIGHT
# =========================================================

def draw_traffic_light(frame, remaining_time):

    height, width = frame.shape[:2]

    # Traffic light की position
    box_x = width - 170
    box_y = 35

    box_width = 135
    box_height = 330

    # Background box
    cv2.rectangle(
        frame,
        (box_x, box_y),
        (box_x + box_width, box_y + box_height),
        (25, 25, 25),
        -1
    )

    # Border
    cv2.rectangle(
        frame,
        (box_x, box_y),
        (box_x + box_width, box_y + box_height),
        (180, 180, 180),
        2
    )

    # -----------------------------------------------------
    # RED
    # -----------------------------------------------------

    if signal_state == "RED":
        red_color = (0, 0, 255)
    else:
        red_color = (60, 60, 60)

    cv2.circle(
        frame,
        (box_x + 67, box_y + 60),
        35,
        red_color,
        -1
    )

    # -----------------------------------------------------
    # YELLOW
    # -----------------------------------------------------

    if signal_state == "YELLOW":
        yellow_color = (0, 255, 255)
    else:
        yellow_color = (60, 60, 60)

    cv2.circle(
        frame,
        (box_x + 67, box_y + 160),
        35,
        yellow_color,
        -1
    )

    # -----------------------------------------------------
    # GREEN
    # -----------------------------------------------------

    if signal_state == "GREEN":
        green_color = (0, 255, 0)
    else:
        green_color = (60, 60, 60)

    cv2.circle(
        frame,
        (box_x + 67, box_y + 260),
        35,
        green_color,
        -1
    )

    # -----------------------------------------------------
    # SIGNAL STATUS
    # -----------------------------------------------------

    status_y = box_y + box_height + 40

    cv2.putText(
        frame,
        signal_state,
        (box_x - 5, status_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # -----------------------------------------------------
    # TIMER
    # -----------------------------------------------------

    cv2.putText(
        frame,
        f"{int(remaining_time)} sec",
        (box_x + 10, status_y + 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )


# =========================================================
# DRAW INFORMATION PANEL
# =========================================================

def draw_info_panel(frame, total, traffic_status):

    # Left side dark transparent-style panel
    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (10, 10),
        (340, 275),
        (20, 20, 20),
        -1
    )

    # Blend
    frame[:] = cv2.addWeighted(
        overlay,
        0.75,
        frame,
        0.25,
        0
    )

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    cv2.putText(
        frame,
        "AI TRAFFIC SYSTEM",
        (25, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2
    )

    # -----------------------------------------------------
    # VEHICLE COUNTS
    # -----------------------------------------------------

    y = 75

    for vehicle, count in vehicle_count.items():

        cv2.putText(
            frame,
            f"{vehicle}: {count}",
            (25, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        y += 32

    # -----------------------------------------------------
    # TOTAL
    # -----------------------------------------------------

    cv2.putText(
        frame,
        f"TOTAL VEHICLES: {total}",
        (25, 215),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 255),
        2
    )

    # -----------------------------------------------------
    # GREEN TIME
    # -----------------------------------------------------

    cv2.putText(
        frame,
        f"GREEN TIME: {green_time} sec",
        (25, 245),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    # -----------------------------------------------------
    # TRAFFIC STATUS
    # -----------------------------------------------------

    cv2.putText(
        frame,
        traffic_status,
        (25, 275),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2
    )


# =========================================================
# CAMERA
# =========================================================

def open_camera():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print("कैमरा खुल नहीं रहा है।")
        return

    print("=" * 55)
    print("           AI TRAFFIC SIGNAL SYSTEM")
    print("=" * 55)
    print()
    print("Camera        : ON")
    print("YOLO          : ON")
    print("Vehicle Count : ON")
    print("Tracking      : ON")
    print("Signal        : SIMULATION")
    print()
    print("Q दबाकर system बंद करें।")
    print()

    while True:

        # =================================================
        # READ CAMERA
        # =================================================

        ret, frame = cap.read()

        if not ret:

            print("कैमरे से वीडियो नहीं मिल रहा है।")
            break

        height, width = frame.shape[:2]

        # =================================================
        # COUNTING LINE
        # =================================================

        line_y = int(height * 0.60)

        # =================================================
        # YOLO TRACKING
        # =================================================

        results = model.track(
            frame,
            persist=True,
            verbose=False
        )

        # =================================================
        # PROCESS DETECTIONS
        # =================================================

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                # -----------------------------------------
                # CLASS
                # -----------------------------------------

                class_id = int(box.cls[0])

                if class_id not in VEHICLE_CLASSES:
                    continue

                # -----------------------------------------
                # CONFIDENCE
                # -----------------------------------------

                confidence = float(box.conf[0])

                if confidence < 0.50:
                    continue

                # -----------------------------------------
                # TRACK ID
                # -----------------------------------------

                if box.id is None:
                    continue

                track_id = int(box.id[0])

                # -----------------------------------------
                # BOUNDING BOX
                # -----------------------------------------

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                # -----------------------------------------
                # CENTER
                # -----------------------------------------

                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                vehicle_name = VEHICLE_CLASSES[class_id]

                # -----------------------------------------
                # DRAW BOX
                # -----------------------------------------

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # -----------------------------------------
                # CENTER POINT
                # -----------------------------------------

                cv2.circle(
                    frame,
                    (center_x, center_y),
                    5,
                    (255, 0, 0),
                    -1
                )

                # -----------------------------------------
                # LABEL
                # -----------------------------------------

                label = (
                    f"{vehicle_name} "
                    f"ID:{track_id} "
                    f"{confidence:.2f}"
                )

                cv2.putText(
                    frame,
                    label,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

                # =================================================
                # COUNT VEHICLE WHEN IT CROSSES LINE
                # =================================================

                if track_id in previous_positions:

                    previous_y = previous_positions[track_id]

                    crossed_down = (
                        previous_y < line_y
                        and center_y >= line_y
                    )

                    crossed_up = (
                        previous_y > line_y
                        and center_y <= line_y
                    )

                    if crossed_down or crossed_up:

                        if track_id not in counted_ids:

                            vehicle_count[
                                vehicle_name
                            ] += 1

                            counted_ids.add(track_id)

                            direction = (
                                "IN"
                                if crossed_down
                                else "OUT"
                            )

                            print(
                                f"{vehicle_name} | "
                                f"ID: {track_id} | "
                                f"{direction}"
                            )

                # Save current position
                previous_positions[track_id] = center_y

        # =================================================
        # TOTAL VEHICLES
        # =================================================

        total = sum(
            vehicle_count.values()
        )

        # =================================================
        # TRAFFIC STATUS
        # =================================================

        traffic_status = get_traffic_status(total)

        # =================================================
        # UPDATE SIGNAL
        # =================================================

        update_signal(total)

        # =================================================
        # CALCULATE REMAINING TIME
        # =================================================

        elapsed = (
            time.time()
            - signal_start_time
        )

        if signal_state == "GREEN":

            remaining_time = green_time - elapsed

        elif signal_state == "YELLOW":

            remaining_time = yellow_time - elapsed

        else:

            remaining_time = red_time - elapsed

        if remaining_time < 0:
            remaining_time = 0

        # =================================================
        # COUNTING LINE
        # =================================================

        cv2.line(
            frame,
            (0, line_y),
            (width, line_y),
            (0, 0, 255),
            3
        )

        # Counting line label
        cv2.rectangle(
            frame,
            (15, line_y - 38),
            (190, line_y - 8),
            (20, 20, 20),
            -1
        )

        cv2.putText(
            frame,
            "COUNTING LINE",
            (25, line_y - 17),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 0, 255),
            2
        )

        # =================================================
        # INFO PANEL
        # =================================================

        draw_info_panel(
            frame,
            total,
            traffic_status
        )

        # =================================================
        # TRAFFIC LIGHT
        # =================================================

        draw_traffic_light(
            frame,
            remaining_time
        )

        # =================================================
        # BOTTOM INFORMATION
        # =================================================

        cv2.rectangle(
            frame,
            (0, height - 40),
            (width, height),
            (20, 20, 20),
            -1
        )

        cv2.putText(
            frame,
            "AI Vehicle Detection  |  Automatic Signal Simulation  |  Press Q to Exit",
            (15, height - 13),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )

        # =================================================
        # SHOW WINDOW
        # =================================================

        cv2.imshow(
            "AI Traffic Signal System",
            frame
        )

        # =================================================
        # EXIT
        # =================================================

        if cv2.waitKey(1) & 0xFF == ord("q"):

            break

    # =====================================================
    # RELEASE CAMERA
    # =====================================================

    cap.release()

    cv2.destroyAllWindows()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    open_camera()