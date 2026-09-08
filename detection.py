import cv2

def detect_vehicles():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera open nahi ho raha")
        return

    print("Camera started... Press Q to exit")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("AI Traffic Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_vehicles()
