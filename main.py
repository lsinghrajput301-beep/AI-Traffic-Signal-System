import cv2
import os
import threading
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO


class TrafficSignalSystem:

    def __init__(self, root):

        self.root = root

        # ==========================
        # WINDOW
        # ==========================

        self.root.title("AI TRAFFIC SIGNAL SYSTEM")
        self.root.geometry("1100x650")
        self.root.minsize(1000, 600)
        self.root.configure(bg="#101820")

        # ==========================
        # VARIABLES
        # ==========================

        self.camera_running = False
        self.signal_running = False

        self.cap = None

        self.lock = threading.Lock()

        self.road_counts = {
            "Road A": 0,
            "Road B": 0,
            "Road C": 0,
            "Road D": 0
        }

        self.total_vehicles = 0

        self.active_road = "Road A"

        self.current_signal = "RED"

        self.remaining_time = 0

        self.green_time = 10
        self.yellow_time = 3

        # ==========================
        # YOLO MODEL
        # ==========================

        model_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "yolo11n.pt"
        )

        print("Loading YOLO model...")

        try:
            self.model = YOLO(model_path)
            print("YOLO model loaded.")
        except Exception as e:
            messagebox.showerror(
                "YOLO Error",
                f"YOLO model load nahi hua:\n{e}"
            )
            self.root.destroy()
            return

        # COCO vehicle classes
        self.vehicle_classes = {
            2: "Car",
            3: "Motorcycle",
            5: "Bus",
            7: "Truck"
        }

        # Minimum confidence
        self.confidence_threshold = 0.40

        # ==========================
        # TITLE
        # ==========================

        title = tk.Label(
            root,
            text="AI TRAFFIC SIGNAL SYSTEM",
            font=("Arial", 24, "bold"),
            bg="#101820",
            fg="white"
        )

        title.pack(pady=8)

        # ==========================
        # MAIN AREA
        # ==========================

        main_frame = tk.Frame(
            root,
            bg="#101820"
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        # ==========================
        # CAMERA FRAME
        # ==========================

        camera_frame = tk.Frame(
            main_frame,
            bg="#202020",
            bd=2,
            relief="solid"
        )

        camera_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        camera_title = tk.Label(
            camera_frame,
            text="LIVE CAMERA",
            font=("Arial", 18, "bold"),
            bg="#202020",
            fg="white"
        )

        camera_title.pack(pady=5)

        self.camera_label = tk.Label(
            camera_frame,
            text="Camera Not Started",
            font=("Arial", 18),
            bg="black",
            fg="white"
        )

        self.camera_label.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5
        )

        # ==========================
        # RIGHT PANEL
        # ==========================

        right_frame = tk.Frame(
            main_frame,
            bg="#101820",
            width=300
        )

        right_frame.pack(
            side="right",
            fill="y",
            padx=5
        )

        right_frame.pack_propagate(False)

        # ==========================
        # SIGNAL BOX
        # ==========================

        signal_box = tk.Frame(
            right_frame,
            bg="#202020",
            bd=2,
            relief="solid"
        )

        signal_box.pack(
            fill="x",
            pady=3
        )

        tk.Label(
            signal_box,
            text="TRAFFIC SIGNAL",
            font=("Arial", 17, "bold"),
            bg="#202020",
            fg="white"
        ).pack(pady=3)

        self.signal_canvas = tk.Canvas(
            signal_box,
            width=120,
            height=210,
            bg="#202020",
            highlightthickness=0
        )

        self.signal_canvas.pack()

        # RED
        self.red_light = self.signal_canvas.create_oval(
            30, 5, 90, 65,
            fill="gray20",
            outline="white",
            width=2
        )

        # YELLOW
        self.yellow_light = self.signal_canvas.create_oval(
            30, 75, 90, 135,
            fill="gray20",
            outline="white",
            width=2
        )

        # GREEN
        self.green_light = self.signal_canvas.create_oval(
            30, 145, 90, 205,
            fill="gray20",
            outline="white",
            width=2
        )

        self.signal_status_label = tk.Label(
            signal_box,
            text="RED",
            font=("Arial", 20, "bold"),
            bg="#202020",
            fg="red"
        )

        self.signal_status_label.pack(pady=3)

        # ==========================
        # INFORMATION BOX
        # ==========================

        info_box = tk.Frame(
            right_frame,
            bg="#202020",
            bd=2,
            relief="solid"
        )

        info_box.pack(
            fill="x",
            pady=3
        )

        self.active_road_label = tk.Label(
            info_box,
            text="Active Road: Road A",
            font=("Arial", 13, "bold"),
            bg="#202020",
            fg="white"
        )

        self.active_road_label.pack(pady=2)

        self.traffic_level_label = tk.Label(
            info_box,
            text="Traffic Level: LOW",
            font=("Arial", 12),
            bg="#202020",
            fg="white"
        )

        self.traffic_level_label.pack(pady=2)

        self.green_time_label = tk.Label(
            info_box,
            text="Green Time: 10 sec",
            font=("Arial", 12),
            bg="#202020",
            fg="white"
        )

        self.green_time_label.pack(pady=2)

        self.remaining_label = tk.Label(
            info_box,
            text="Remaining: 0 sec",
            font=("Arial", 14, "bold"),
            bg="#202020",
            fg="yellow"
        )

        self.remaining_label.pack(pady=3)

        # ==========================
        # TOTAL VEHICLES
        # ==========================

        total_box = tk.Frame(
            right_frame,
            bg="#202020",
            bd=2,
            relief="solid"
        )

        total_box.pack(
            fill="x",
            pady=3
        )

        self.total_label = tk.Label(
            total_box,
            text="Total Vehicles: 0",
            font=("Arial", 14, "bold"),
            bg="#202020",
            fg="cyan"
        )

        self.total_label.pack(pady=5)

        # ==========================
        # ROAD COUNTS
        # ==========================

        roads_box = tk.Frame(
            right_frame,
            bg="#202020",
            bd=2,
            relief="solid"
        )

        roads_box.pack(
            fill="x",
            pady=3
        )

        tk.Label(
            roads_box,
            text="ROAD VEHICLE COUNT",
            font=("Arial", 13, "bold"),
            bg="#202020",
            fg="white"
        ).pack(pady=2)

        self.road_labels = {}

        for road in [
            "Road A",
            "Road B",
            "Road C",
            "Road D"
        ]:

            label = tk.Label(
                roads_box,
                text=f"{road}: 0",
                font=("Arial", 11),
                bg="#202020",
                fg="white"
            )

            label.pack(pady=1)

            self.road_labels[road] = label

        # ==========================
        # BUTTONS
        # ==========================

        button_box = tk.Frame(
            right_frame,
            bg="#101820"
        )

        button_box.pack(
            fill="x",
            pady=5
        )

        self.camera_button = tk.Button(
            button_box,
            text="START CAMERA",
            font=("Arial", 11, "bold"),
            command=self.start_camera,
            bg="green",
            fg="white",
            width=22
        )

        self.camera_button.pack(pady=2)

        self.signal_button = tk.Button(
            button_box,
            text="START TRAFFIC SIGNAL",
            font=("Arial", 11, "bold"),
            command=self.start_signal,
            bg="blue",
            fg="white",
            width=22
        )

        self.signal_button.pack(pady=2)

        self.stop_button = tk.Button(
            button_box,
            text="STOP",
            font=("Arial", 11, "bold"),
            command=self.stop_system,
            bg="red",
            fg="white",
            width=22
        )

        self.stop_button.pack(pady=2)

        # ==========================
        # START GUI UPDATE
        # ==========================

        self.update_gui()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )

    # =====================================================
    # TRAFFIC LEVEL
    # =====================================================

    def get_traffic_level(self, count):

        if count <= 2:
            return "LOW"

        elif count <= 5:
            return "MEDIUM"

        else:
            return "HIGH"

    # =====================================================
    # AUTOMATIC GREEN TIME
    # =====================================================

    def calculate_green_time(self, count):

        if count <= 2:
            return 10

        elif count <= 5:
            return 20

        elif count <= 10:
            return 30

        else:
            return 45

    # =====================================================
    # SELECT HIGHEST TRAFFIC ROAD
    # =====================================================

    def select_highest_traffic_road(self):

        with self.lock:
            counts = self.road_counts.copy()

        highest_count = max(counts.values())

        # No traffic
        if highest_count == 0:
            return "Road A"

        highest_roads = [
            road
            for road, count in counts.items()
            if count == highest_count
        ]

        # If tie, select first road
        return highest_roads[0]

    # =====================================================
    # SIGNAL DISPLAY
    # =====================================================

    def update_signal_display(self):

        # Turn all lights OFF
        self.signal_canvas.itemconfig(
            self.red_light,
            fill="gray20"
        )

        self.signal_canvas.itemconfig(
            self.yellow_light,
            fill="gray20"
        )

        self.signal_canvas.itemconfig(
            self.green_light,
            fill="gray20"
        )

        # RED
        if self.current_signal == "RED":

            self.signal_canvas.itemconfig(
                self.red_light,
                fill="red"
            )

            self.signal_status_label.config(
                text="RED",
                fg="red"
            )

        # YELLOW
        elif self.current_signal == "YELLOW":

            self.signal_canvas.itemconfig(
                self.yellow_light,
                fill="yellow"
            )

            self.signal_status_label.config(
                text="YELLOW",
                fg="yellow"
            )

        # GREEN
        elif self.current_signal == "GREEN":

            self.signal_canvas.itemconfig(
                self.green_light,
                fill="green"
            )

            self.signal_status_label.config(
                text="GREEN",
                fg="lime"
            )

    # =====================================================
    # GUI UPDATE
    # =====================================================

    def update_gui(self):

        with self.lock:
            counts = self.road_counts.copy()
            total = self.total_vehicles
            active_road = self.active_road
            green_time = self.green_time
            remaining_time = self.remaining_time

        # Total
        self.total_label.config(
            text=f"Total Vehicles: {total}"
        )

        # Road counts
        for road in counts:

            self.road_labels[road].config(
                text=f"{road}: {counts[road]}"
            )

        # Active Road
        self.active_road_label.config(
            text=f"Active Road: {active_road}"
        )

        # Active road traffic
        active_count = counts.get(
            active_road,
            0
        )

        traffic_level = self.get_traffic_level(
            active_count
        )

        self.traffic_level_label.config(
            text=f"Traffic Level: {traffic_level}"
        )

        self.green_time_label.config(
            text=f"Green Time: {green_time} sec"
        )

        self.remaining_label.config(
            text=f"Remaining: {remaining_time} sec"
        )

        self.update_signal_display()

        self.root.after(
            200,
            self.update_gui
        )

    # =====================================================
    # START CAMERA
    # =====================================================

    def start_camera(self):

        if self.camera_running:
            return

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():

            messagebox.showerror(
                "Camera Error",
                "Camera open nahi ho raha hai."
            )

            self.cap = None
            return

        self.camera_running = True

        self.camera_button.config(
            state="disabled"
        )

        print("Camera started.")

        thread = threading.Thread(
            target=self.camera_loop,
            daemon=True
        )

        thread.start()

    # =====================================================
    # CAMERA LOOP
    # =====================================================

    def camera_loop(self):

        while self.camera_running:

            ret, frame = self.cap.read()

            if not ret:

                print(
                    "Camera frame nahi mil raha."
                )

                break

            # Camera size
            frame = cv2.resize(
                frame,
                (760, 500)
            )

            height, width = frame.shape[:2]

            # ==========================
            # YOLO DETECTION
            # ==========================

            try:

                results = self.model(
                    frame,
                    verbose=False
                )

            except Exception as e:

                print(
                    f"YOLO detection error: {e}"
                )

                continue

            # New road counts
            new_counts = {
                "Road A": 0,
                "Road B": 0,
                "Road C": 0,
                "Road D": 0
            }

            total_count = 0

            # ==========================
            # VEHICLE DETECTION
            # ==========================

            for result in results:

                for box in result.boxes:

                    class_id = int(
                        box.cls[0]
                    )

                    # Ignore non-vehicles
                    if class_id not in self.vehicle_classes:
                        continue

                    # Confidence
                    confidence = float(
                        box.conf[0]
                    )

                    if confidence < self.confidence_threshold:
                        continue

                    # Bounding box
                    x1, y1, x2, y2 = map(
                        int,
                        box.xyxy[0]
                    )

                    # Center point
                    center_x = (
                        x1 + x2
                    ) // 2

                    center_y = (
                        y1 + y2
                    ) // 2

                    # ==========================
                    # ROAD SELECTION
                    # ==========================

                    if center_x < width // 2:

                        if center_y < height // 2:
                            road = "Road A"
                        else:
                            road = "Road C"

                    else:

                        if center_y < height // 2:
                            road = "Road B"
                        else:
                            road = "Road D"

                    # Count
                    new_counts[road] += 1
                    total_count += 1

                    vehicle_name = (
                        self.vehicle_classes[
                            class_id
                        ]
                    )

                    # ==========================
                    # DRAW BOX
                    # ==========================

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    # Vehicle label
                    label_text = (
                        f"{vehicle_name} "
                        f"{confidence:.2f}"
                    )

                    cv2.putText(
                        frame,
                        label_text,
                        (
                            x1,
                            max(y1 - 10, 20)
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 255, 0),
                        2
                    )

            # ==========================
            # ROAD DIVIDING LINES
            # ==========================

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

            # ==========================
            # ROAD NAMES
            # ==========================

            cv2.putText(
                frame,
                "ROAD A",
                (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "ROAD B",
                (width // 2 + 15, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "ROAD C",
                (15, height // 2 + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "ROAD D",
                (
                    width // 2 + 15,
                    height // 2 + 30
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            # ==========================
            # TOTAL VEHICLES
            # ==========================

            cv2.putText(
                frame,
                f"Vehicles: {total_count}",
                (15, height - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

            # ==========================
            # SAVE COUNTS
            # ==========================

            with self.lock:

                self.road_counts = new_counts

                self.total_vehicles = total_count

            # ==========================
            # CAMERA IMAGE
            # ==========================

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(rgb)

            # Send image to Tkinter main thread
            self.root.after(
                0,
                self.show_camera,
                image
            )

            time.sleep(0.03)

        print("Camera stopped.")

    # =====================================================
    # SHOW CAMERA
    # =====================================================

    def show_camera(self, image):

        if not self.camera_running:
            return

        photo = ImageTk.PhotoImage(
            image=image
        )

        self.camera_label.config(
            image=photo,
            text=""
        )

        self.camera_label.image = photo

    # =====================================================
    # START SIGNAL
    # =====================================================

    def start_signal(self):

        if self.signal_running:
            return

        self.signal_running = True

        self.signal_button.config(
            state="disabled"
        )

        print(
            "AI Traffic Signal Started."
        )

        thread = threading.Thread(
            target=self.run_signal_cycle,
            daemon=True
        )

        thread.start()

    # =====================================================
    # SIGNAL CYCLE
    # =====================================================

    def run_signal_cycle(self):

        while self.signal_running:

            # ==========================
            # FIND HIGHEST TRAFFIC ROAD
            # ==========================

            road = (
                self.select_highest_traffic_road()
            )

            with self.lock:

                count = self.road_counts[
                    road
                ]

                self.active_road = road

            # ==========================
            # TRAFFIC LEVEL
            # ==========================

            traffic_level = (
                self.get_traffic_level(
                    count
                )
            )

            # ==========================
            # GREEN TIME
            # ==========================

            green_time = (
                self.calculate_green_time(
                    count
                )
            )

            with self.lock:
                self.green_time = green_time

            # ==========================
            # AI DECISION PRINT
            # ==========================

            print()
            print("==========================")
            print("AI TRAFFIC DECISION")
            print(
                f"Road: {road}"
            )
            print(
                f"Vehicles: {count}"
            )
            print(
                f"Traffic: {traffic_level}"
            )
            print(
                f"Green Time: {green_time} sec"
            )
            print("==========================")

            # ==========================
            # GREEN
            # ==========================

            with self.lock:

                self.current_signal = "GREEN"

                self.remaining_time = green_time

            self.root.after(
                0,
                self.update_signal_display
            )

            # Countdown
            for second in range(
                green_time,
                0,
                -1
            ):

                if not self.signal_running:
                    return

                with self.lock:
                    self.remaining_time = second

                time.sleep(1)

            # ==========================
            # YELLOW
            # ==========================

            with self.lock:

                self.current_signal = "YELLOW"

                self.remaining_time = (
                    self.yellow_time
                )

            self.root.after(
                0,
                self.update_signal_display
            )

            for second in range(
                self.yellow_time,
                0,
                -1
            ):

                if not self.signal_running:
                    return

                with self.lock:
                    self.remaining_time = second

                time.sleep(1)

            # ==========================
            # RED
            # ==========================

            with self.lock:

                self.current_signal = "RED"

                self.remaining_time = 0

            self.root.after(
                0,
                self.update_signal_display
            )

            time.sleep(1)

            # Next cycle:
            # AI again checks traffic
            # and selects highest traffic road.

    # =====================================================
    # STOP SYSTEM
    # =====================================================

    def stop_system(self):

        print(
            "Stopping system..."
        )

        self.camera_running = False
        self.signal_running = False

        if self.cap is not None:

            self.cap.release()

            self.cap = None

        with self.lock:

            self.current_signal = "RED"

            self.remaining_time = 0

        self.camera_button.config(
            state="normal"
        )

        self.signal_button.config(
            state="normal"
        )

        self.camera_label.config(
            image="",
            text="Camera Stopped"
        )

        self.camera_label.image = None

        self.update_signal_display()

        print(
            "System stopped."
        )

    # =====================================================
    # CLOSE WINDOW
    # =====================================================

    def close_window(self):

        self.camera_running = False
        self.signal_running = False

        if self.cap is not None:

            self.cap.release()

            self.cap = None

        self.root.destroy()


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = TrafficSignalSystem(
        root
    )

    root.mainloop()