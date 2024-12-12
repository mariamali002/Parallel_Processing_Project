import tkinter as tk
from tkinter import messagebox
import threading
from booking_system import BookingSystem
from gui import BookingSystemGUI


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parallel Movie Ticket Booking System")
        self.root.geometry("400x200")
        self.shared_booking_system = BookingSystem(rows=10, cols=10, show_id=1)

        tk.Label(self.root, text="Enter Number of Threads:", font=("Arial", 14)).pack(
            pady=20
        )

        self.thread_count_var = tk.StringVar()
        tk.Entry(
            self.root, textvariable=self.thread_count_var, font=("Arial", 14)
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Start",
            font=("Arial", 14),
            bg="blue",
            fg="white",
            command=self.start_threads,
        ).pack(pady=20)

    def start_threads(self):
        try:
            num_threads = int(self.thread_count_var.get())
            if num_threads <= 0:
                raise ValueError("Number of threads must be greater than 0")

            # Launch multiple windows using Toplevel instead of Tk in separate threads
            for _ in range(num_threads):
                thread = threading.Thread(target=self.launch_gui)
                thread.daemon = (
                    True  # Allow threads to exit when the main program exits
                )
                thread.start()

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def launch_gui(self):
        
        top_window = tk.Toplevel(self.root)
        app = BookingSystemGUI(top_window, booking_system=self.shared_booking_system)
        


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
