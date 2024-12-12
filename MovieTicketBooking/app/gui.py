import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from booking_system import BookingSystem
from db_connection import connect_to_db, close_connection
import admin_gui


class BookingSystemGUI:
    def __init__(self, root, booking_system):
        self.root = root
        self.booking_system = booking_system
        self.root.title("Movie Ticket Booking System")
        self.root.geometry("800x600")

        self.selected_show_id = None
        # self.booking_system = None

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.movie_frame = tk.Frame(self.main_frame)
        self.movie_frame.pack(fill="both", expand=True)

        self.seating_frame = tk.Frame(self.main_frame)

        self.show_movie_selection()

    def show_movie_selection(self):

        tk.Label(
            self.movie_frame, text="Select a Movie and Showtime", font=("Arial", 16)
        ).pack(pady=10)

        connection, cursor = connect_to_db()
        cursor.execute("SELECT id, movie_name, date_time FROM shows;")
        self.shows = cursor.fetchall()
        close_connection(connection, cursor)

        self.show_options = [
            f"{show['movie_name']} - {show['date_time']}" for show in self.shows
        ]

        self.selected_show = tk.StringVar()
        self.dropdown = ttk.Combobox(
            self.movie_frame,
            textvariable=self.selected_show,
            values=self.show_options,
            state="readonly",
        )
        self.dropdown.pack(pady=10)

        proceed_button = tk.Button(
            self.movie_frame,
            text="Proceed",
            command=self.proceed_to_seating,
            font=("Arial", 12),
            bg="blue",
            fg="white",
        )

        proceed_button.pack(pady=20)

        # back_to_admin_button = tk.Button(
        #     self.movie_frame,
        #     text="Back to Admin Panel",
        #     command=self.switch_to_admin_view,
        #     font=("Arial", 12),
        #     bg="red",
        #     fg="white",
        # )
        # back_to_admin_button.pack(pady=10)

        self.refresh_button = tk.Button(
            self.movie_frame,
            text="Refresh",
            command=self.refresh_movie_list,
            font=("Arial", 12),
            bg="yellow",
            fg="black",
        )
        self.refresh_button.pack(pady=10)

    def refresh_movie_list(self):
        self.refresh_button.config(state="disabled")  
        connection, cursor = connect_to_db()
        cursor.execute("SELECT id, movie_name, date_time FROM shows;")
        self.shows = cursor.fetchall()
        close_connection(connection, cursor)

        self.show_options = [
            f"{show['movie_name']} - {show['date_time']}" for show in self.shows
        ]

        self.dropdown["values"] = self.show_options
        self.dropdown.set("")
        self.refresh_button.config(state="normal")  

    def proceed_to_seating(self):
        selected_index = self.dropdown.current()
        if selected_index == -1:
            messagebox.showerror(
                "Selection Error", "Please select a movie and showtime!"
            )
            return

        self.selected_show_id = self.shows[selected_index]["id"]
        self.booking_system = BookingSystem(
            rows=10, cols=10, show_id=self.selected_show_id
        )

        self.movie_frame.pack_forget()
        self.show_seating_layout()

    def show_seating_layout(self):

        self.seating_frame.pack(fill="both", expand=True)

        tk.Label(self.seating_frame, text="Seating Layout", font=("Arial", 16)).grid(
            row=0, column=0, columnspan=self.booking_system.cols, pady=10
        )

        for r in range(self.booking_system.rows):
            for c in range(self.booking_system.cols):
                seat_status = self.booking_system.seats[r][c]
                btn = tk.Button(
                    self.seating_frame,
                    text="O" if seat_status == 0 else "X",
                    width=4,
                    height=2,
                    bg="green" if seat_status == 0 else "red",
                    command=lambda row=r, col=c: self.book_seat(row, col),
                )
                btn.grid(row=r + 1, column=c, padx=5, pady=5)

        back_button = tk.Button(
            self.seating_frame,
            text="Back",
            command=self.return_to_movie_selection,
            font=("Arial", 12),
            bg="grey",
            fg="white",
        )
        back_button.grid(
            row=self.booking_system.rows + 1,
            column=0,
            columnspan=self.booking_system.cols,
            pady=10,
        )

    def return_to_movie_selection(self):

        for widget in self.seating_frame.winfo_children():
            widget.destroy()
        self.seating_frame.pack_forget()
        self.movie_frame.pack(fill="both", expand=True)

    def book_seat(self, row, col):
        user_id = simpledialog.askstring("Enter Name", "Enter your name:")
        if not user_id:
            messagebox.showerror("Booking Failed", "Name is required to book a seat.")
            return

        success = self.booking_system.book_seat(user_id, row + 1, col + 1)
        if success:
            self.update_seats()
        else:
            messagebox.showerror("Booking Failed", "Seat already booked!")

    def update_seats(self):
        """Refresh the seating layout after a booking is made."""
        for widget in self.seating_frame.winfo_children():
            widget.destroy()  

        
        self.show_seating_layout()

    def switch_to_admin_view(self):
        """Switch back to the Admin Panel."""
        self.root.quit()  
        self.root.destroy()  
        admin_gui.start_admin_gui()  


def start_gui():
    root = tk.Tk()
    booking_system = BookingSystem(rows=10, cols=10, show_id=1)  
    app = BookingSystemGUI(root, booking_system)  
    root.mainloop()


if __name__ == "__main__":
    # root = tk.Tk()
    # app = BookingSystemGUI(root)
    # root.mainloop()
    start_gui()
