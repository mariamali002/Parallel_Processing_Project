import threading
import random
import time
from db_connection import connect_to_db, close_connection


# class to mange the movie theater ticket booking system
class BookingSystem:
    def __init__(self, rows, cols, show_id):

        self.rows = rows
        self.cols = cols
        self.show_id = show_id
        self.seats = self.fetch_seating_layout()
        self.lock = threading.Lock()

    def fetch_seating_layout(self):
        connection, cursor = connect_to_db()
        cursor.execute(
            "Select row_num, col_num, status from seats where show_id = %s ORDER BY row_num, col_num; ",
            (self.show_id,),
        )

        layout = cursor.fetchall()
        close_connection(connection, cursor)
        seating = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for seat in layout:
            row, col, status = seat["row_num"], seat["col_num"], seat["status"]
            seating[row - 1][col - 1] = status

        return seating

    def display_seats(self):

        for row in self.seats:
            print(" ".join(map(str, row)))
        print("\n")

    def book_seat(self, user_id, row, col):
        with self.lock:
            if self.seats[row - 1][col - 1] == 1:
                print(
                    f"User {user_id} failed to book seat ({row}, {col}). Already booked."
                )
                return False

            connection, cursor = connect_to_db()
            try:
                cursor.execute(
                    "update seats set status = 1 where show_id = %s and row_num = %s and col_num = %s and status = 0;",
                    (self.show_id, row, col),
                )
                if cursor.rowcount == 0:
                    print(
                        f"User {user_id} failed to book seat ({row}, {col}). Another user booked it."
                    )
                    return False

                cursor.execute(
                    "insert into bookings (show_id, user_name, seat_row, seat_col) values (%s, %s,%s,%s);",
                    (self.show_id, f"User-{user_id}", row, col),
                )

                connection.commit()

                self.seats[row - 1][col - 1] = 1
                print(f"User {user_id} successfully booked seat ({row},{col}.)")
                return True

            except Exception as e:
                print("Error during booking:", e)
                connection.rollback()
                return False

            finally:
                close_connection(connection, cursor)

    def random_booking(self, user_id):
        while True:
            with self.lock:
                if all(all(seat == 1 for seat in row) for row in self.seats):
                    print(f"User {user_id}: Theater fully booked. No seat available.")
                    break

            row = random.randint(1, self.rows)
            col = random.randint(1, self.cols)

            if self.book_seat(user_id, row, col):
                break


def simulate_user(booking_system, num_users):
    threads = []
    for user_id in range(num_users):
        thread = threading.Thread(target=booking_system.random_booking, args=(user_id,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


# if __name__ == "__main__":

#     theater = BookingSystem(rows=10, cols=10, show_id=1)
#     print("Intial Seating Layout:")
#     theater.display_seats()

#     simulate_user(theater, num_users=50)

#     print("final Seating Layout:")
#     theater.display_seats()
