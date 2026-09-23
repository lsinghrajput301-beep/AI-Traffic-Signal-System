import tkinter as tk


class TrafficSignalGUI:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("AI Traffic Signal System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#101820")

        # ==============================
        # TITLE
        # ==============================

        title = tk.Label(
            self.root,
            text="AI TRAFFIC SIGNAL SYSTEM",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#101820"
        )

        title.pack(pady=20)

        # ==============================
        # MAIN FRAME
        # ==============================

        main_frame = tk.Frame(
            self.root,
            bg="#101820"
        )

        main_frame.pack()

        # ==============================
        # SIGNAL BOX
        # ==============================

        signal_box = tk.Frame(
            main_frame,
            bg="#202020",
            bd=3,
            relief="ridge",
            width=300,
            height=500
        )

        signal_box.grid(
            row=0,
            column=0,
            padx=20
        )

        tk.Label(
            signal_box,
            text="TRAFFIC SIGNAL",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#202020"
        ).pack(pady=20)

        # ==============================
        # SIGNAL CANVAS
        # ==============================

        self.canvas = tk.Canvas(
            signal_box,
            width=220,
            height=400,
            bg="black",
            highlightthickness=0
        )

        self.canvas.pack(pady=10)

        # RED

        self.red_light = self.canvas.create_oval(
            60, 20,
            160, 120,
            fill="gray"
        )

        # YELLOW

        self.yellow_light = self.canvas.create_oval(
            60, 150,
            160, 250,
            fill="gray"
        )

        # GREEN

        self.green_light = self.canvas.create_oval(
            60, 280,
            160, 380,
            fill="gray"
        )

        # ==============================
        # INFORMATION BOX
        # ==============================

        info_box = tk.Frame(
            main_frame,
            bg="#202020",
            bd=3,
            relief="ridge",
            width=500,
            height=500
        )

        info_box.grid(
            row=0,
            column=1,
            padx=20
        )

        tk.Label(
            info_box,
            text="ROAD-WISE TRAFFIC",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#202020"
        ).pack(pady=20)

        # ==============================
        # ROAD LABELS
        # ==============================

        self.road_a = tk.Label(
            info_box,
            text="Road A : 0",
            font=("Arial", 18, "bold"),
            fg="red",
            bg="#202020"
        )

        self.road_a.pack(pady=5)

        self.road_b = tk.Label(
            info_box,
            text="Road B : 0",
            font=("Arial", 18, "bold"),
            fg="blue",
            bg="#202020"
        )

        self.road_b.pack(pady=5)

        self.road_c = tk.Label(
            info_box,
            text="Road C : 0",
            font=("Arial", 18, "bold"),
            fg="orange",
            bg="#202020"
        )

        self.road_c.pack(pady=5)

        self.road_d = tk.Label(
            info_box,
            text="Road D : 0",
            font=("Arial", 18, "bold"),
            fg="green",
            bg="#202020"
        )

        self.road_d.pack(pady=5)

        # ==============================
        # ACTIVE ROAD
        # ==============================

        self.active_label = tk.Label(
            info_box,
            text="ACTIVE ROAD : Road A",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#202020"
        )

        self.active_label.pack(pady=25)

        # ==============================
        # TRAFFIC
        # ==============================

        self.traffic_label = tk.Label(
            info_box,
            text="TRAFFIC : LOW",
            font=("Arial", 20, "bold"),
            fg="yellow",
            bg="#202020"
        )

        self.traffic_label.pack(pady=8)

        # ==============================
        # GREEN TIME
        # ==============================

        self.green_time_label = tk.Label(
            info_box,
            text="GREEN TIME : 15 sec",
            font=("Arial", 20, "bold"),
            fg="lime",
            bg="#202020"
        )

        self.green_time_label.pack(pady=8)

        # ==============================
        # REMAINING
        # ==============================

        self.remaining_label = tk.Label(
            info_box,
            text="REMAINING : 15 sec",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#202020"
        )

        self.remaining_label.pack(pady=8)

        # ==============================
        # STATUS
        # ==============================

        self.status_label = tk.Label(
            self.root,
            text="RED",
            font=("Arial", 30, "bold"),
            fg="red",
            bg="#101820"
        )

        self.status_label.pack(pady=20)

    # ==================================
    # UPDATE SIGNAL
    # ==================================

    def update_signal(
        self,
        signal,
        active_road,
        traffic_level,
        green_time,
        remaining,
        road_counts
    ):

        # Turn OFF all lights

        self.canvas.itemconfig(
            self.red_light,
            fill="gray"
        )

        self.canvas.itemconfig(
            self.yellow_light,
            fill="gray"
        )

        self.canvas.itemconfig(
            self.green_light,
            fill="gray"
        )

        # ==============================
        # RED
        # ==============================

        if signal == "RED":

            self.canvas.itemconfig(
                self.red_light,
                fill="red"
            )

            self.status_label.config(
                text="RED",
                fg="red"
            )

        # ==============================
        # YELLOW
        # ==============================

        elif signal == "YELLOW":

            self.canvas.itemconfig(
                self.yellow_light,
                fill="yellow"
            )

            self.status_label.config(
                text="YELLOW",
                fg="yellow"
            )

        # ==============================
        # GREEN
        # ==============================

        elif signal == "GREEN":

            self.canvas.itemconfig(
                self.green_light,
                fill="green"
            )

            self.status_label.config(
                text="GREEN",
                fg="lime"
            )

        # ==============================
        # ROAD COUNTS
        # ==============================

        self.road_a.config(
            text=f"Road A : {road_counts['Road A']}"
        )

        self.road_b.config(
            text=f"Road B : {road_counts['Road B']}"
        )

        self.road_c.config(
            text=f"Road C : {road_counts['Road C']}"
        )

        self.road_d.config(
            text=f"Road D : {road_counts['Road D']}"
        )

        # ==============================
        # OTHER INFORMATION
        # ==============================

        self.active_label.config(
            text=f"ACTIVE ROAD : {active_road}"
        )

        self.traffic_label.config(
            text=f"TRAFFIC : {traffic_level}"
        )

        self.green_time_label.config(
            text=f"GREEN TIME : {green_time} sec"
        )

        self.remaining_label.config(
            text=f"REMAINING : {remaining} sec"
        )