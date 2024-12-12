import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import connect_to_db, close_connection
import gui


class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel")
        self.root.geometry("800x600")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.show_admin_options()

    def show_admin_options(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Admin Panel", font=("Arial", 20)).pack(pady=20)

        tk.Button(
            self.main_frame,
            text="Add New Movie",
            command=self.add_movie_screen,
            font=("Arial", 14),
            bg="blue",
            fg="white",
            width=20,
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Reset Seat Status",
            command=self.reset_seats_screen,
            font=("Arial", 14),
            bg="orange",
            fg="white",
            width=20,
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="View Bookings",
            command=self.view_bookings_screen,
            font=("Arial", 14),
            bg="green",
            fg="white",
            width=20,
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Delete Movie",
            command=self.delete_movie_screen,
            font=("Arial", 14),
            bg="red",
            fg="white",
            width=20,
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Back to User View",
            command=self.switch_to_user_view,
            font=("Arial", 14),
            bg="red",
            fg="white",
            width=20,
        ).pack(pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def add_movie_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Add New Movie", font=("Arial", 16)).pack(
            pady=20
        )

        tk.Label(self.main_frame, text="Movie Name").pack(pady=5)
        self.movie_name_entry = tk.Entry(self.main_frame, width=30)
        self.movie_name_entry.pack(pady=5)

        tk.Label(self.main_frame, text="showtime (yyyy-MM-DD HH:MM:SS)").pack(pady=5)
        self.showtime_entry = tk.Entry(self.main_frame, width=30)
        self.showtime_entry.pack(pady=5)

        tk.Button(
            self.main_frame,
            text="Add Movie",
            command=self.add_movie_to_db,
            font=("Arial", 12),
            bg="blue",
            fg="white",
        ).pack(pady=20)

        tk.Button(
            self.main_frame,
            text="Back",
            command=self.show_admin_options,
            font=("Arial", 12),
            bg="grey",
            fg="white",
        ).pack(pady=10)

    def add_movie_to_db(self):
        movie_name = self.movie_name_entry.get()
        showtime = self.showtime_entry.get()

        if not movie_name or not showtime:
            messagebox.showerror("Input Error", "Please fill in all fields")
            return

        try:
            connection, cursor = connect_to_db()
            cursor.execute(
                "INSERT INTO shows (movie_name,date_time) VALUES (%s, %s);",
                (movie_name, showtime),
            )

            show_id = cursor.lastrowid

            cursor.execute(
                """
            INSERT INTO seats (show_id, row_num, col_num, status)
            SELECT %s AS show_id, r AS row_num, c AS col_num, 0 AS status
            FROM (SELECT 1 AS r UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION 
                         SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) row_numbers,
                 (SELECT 1 AS c UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION 
                         SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) col_numbers
            ORDER BY row_num, col_num;
            """,
                (show_id,),
            )

            connection.commit()
            close_connection(connection, cursor)
            messagebox.showinfo("Success", "Movie added successfully.")
            self.show_admin_options()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def reset_seats_screen(self):

        self.clear_frame()

        tk.Label(self.main_frame, text="Reset Seat Status", font=("Arial", 16)).pack(
            pady=20
        )

        tk.Label(self.main_frame, text="Select Movie and Showtime").pack(pady=5)
        connection, cursor = connect_to_db()
        cursor.execute("SELECT id, movie_name, date_time FROM shows;")
        self.shows = cursor.fetchall()
        close_connection(connection, cursor)

        self.show_options = [
            f"{show['movie_name']} - {show['date_time']}" for show in self.shows
        ]

        self.selected_show = tk.StringVar()
        self.dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.selected_show,
            values=self.show_options,
            state="readonly",
        )
        self.dropdown.pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Reset Seats",
            command=self.reset_seats_in_db,
            font=("Arial", 12),
            bg="orange",
            fg="white",
        ).pack(pady=20)

        tk.Button(
            self.main_frame,
            text="Back",
            command=self.show_admin_options,
            font=("Arial", 12),
            bg="grey",
            fg="white",
        ).pack(pady=10)

    def reset_seats_in_db(self):
        selected_index = self.dropdown.current()
        if selected_index == -1:
            messagebox.showerror("Selection Error", "Please select a movie!")
            return

        show_id = self.shows[selected_index]["id"]

        try:
            connection, cursor = connect_to_db()
            cursor.execute(
                "UPDATE seats SET status = 0 WHERE show_id = %s;", (show_id,)
            )

            cursor.execute("DELETE FROM bookings WHERE show_id = %s;", (show_id,))

            connection.commit()
            close_connection(connection, cursor)
            messagebox.showinfo("Success", "Seats reset successfully.")
            self.show_admin_options()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def view_bookings_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="View Bookings", font=("Arial", 16)).pack(
            pady=20
        )

        tk.Label(self.main_frame, text="Select Movie and Showtime").pack(pady=5)
        connection, cursor = connect_to_db()
        cursor.execute("SELECT id, movie_name, date_time FROM shows;")
        self.shows = cursor.fetchall()
        close_connection(connection, cursor)

        self.show_options = [
            f"{show['movie_name']} - {show['date_time']}" for show in self.shows
        ]

        self.selected_show = tk.StringVar()
        self.dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.selected_show,
            values=self.show_options,
            state="readonly",
        )

        self.dropdown.pack(pady=10)

        tk.Button(
            self.main_frame,
            text="View Bookings",
            command=self.view_bookings_in_db,
            font=("Arial", 12),
            bg="green",
            fg="white",
        ).pack(pady=20)

        tk.Button(
            self.main_frame,
            text="Back",
            command=self.show_admin_options,
            font=("Arial", 12),
            bg="grey",
            fg="white",
        ).pack(pady=10)

    def view_bookings_in_db(self):

        selected_index = self.dropdown.current()
        if selected_index == -1:
            messagebox.showerror("Selection Error", "Please select a movie!")
            return

        show_id = self.shows[selected_index]["id"]

        try:
            connection, cursor = connect_to_db()
            cursor.execute("SELECT * FROM bookings WHERE show_id = %s;", (show_id,))
            bookings = cursor.fetchall()
            close_connection(connection, cursor)

            if not bookings:
                messagebox.showinfo("No Bookings", "No bookings found for this show.")
                return

            bookings_window = tk.Toplevel(self.root)
            bookings_window.title("Bookings")
            bookings_window.geometry("600x400")

            canvas = tk.Canvas(bookings_window)
            scroll_y = tk.Scrollbar(
                bookings_window, orient="vertical", command=canvas.yview
            )
            frame = tk.Frame(canvas)

            frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
            )

            canvas.create_window((0, 0), window=frame, anchor="nw")
            canvas.configure(yscrollcommand=scroll_y.set)

            canvas.pack(side="left", fill="both", expand=True)
            scroll_y.pack(side="right", fill="y")

            for idx, booking in enumerate(bookings, start=1):
                tk.Label(
                    frame,
                    text=f"{idx}. User: {booking['user_name']}, Row: {booking['seat_row']}, Col: {booking['seat_col']}",
                    font=("Arial", 12),
                ).pack(pady=5)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def delete_movie_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Delete Movie", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.main_frame, text="Select a Movie").pack(pady=5)
        connection, cursor = connect_to_db()
        cursor.execute("SELECT id, movie_name, date_time FROM shows;")
        self.shows = cursor.fetchall()
        close_connection(connection, cursor)

        self.show_options = [
            f"{show['movie_name']} - {show['date_time']}" for show in self.shows
        ]

        self.selected_show = tk.StringVar()
        self.dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.selected_show,
            values=self.show_options,
            state="readonly",
        )
        self.dropdown.pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Delete Movie",
            command=self.delete_movie_from_db,
            font=("Arial", 12),
            bg="red",
            fg="white",
        ).pack(pady=20)

        tk.Button(
            self.main_frame,
            text="Back",
            command=self.show_admin_options,
            font=("Arial", 12),
            bg="grey",
            fg="white",
        ).pack(pady=10)

    def delete_movie_from_db(self):
        selected_index = self.dropdown.current()
        if selected_index == -1:
            messagebox.showerror("Selection Error", "Please select a movie!")
            return
        show_id = self.shows[selected_index]["id"]

        confirmation = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the movie: {self.show_options[selected_index]}?\nThis will also delete all associated bookings and seats.",
        )
        if not confirmation:
            return

        try:
            connection, cursor = connect_to_db()
            cursor.execute("DELETE FROM bookings WHERE show_id = %s;", (show_id,))
            cursor.execute("DELETE FROM seats WHERE show_id = %s;", (show_id,))
            cursor.execute("DELETE FROM shows WHERE id = %s;", (show_id,))
            connection.commit()
            close_connection(connection, cursor)

            messagebox.showinfo("Success", "Movie deleted successfully.")
            self.show_admin_options()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def switch_to_user_view(self):
        self.root.destroy()
        gui.start_gui()


def start_admin_gui():
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()


if __name__ == "__main__":
    start_admin_gui()
#     # root = tk.Tk()
#     # app = AdminGUI(root)
#     # root.mainloop()
