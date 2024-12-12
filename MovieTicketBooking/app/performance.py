import time
from booking_system import BookingSystem, simulate_user


def single_threaded_simulation(booking_system, num_users):
    start_time = time.time()
    for user_id in range(num_users):
        booking_system.random_booking(user_id)
    end_time = time.time()
    return end_time - start_time


def multithreaded_simulation(booking_system, num_users):
    start_time = time.time()
    simulate_user(booking_system, num_users)
    end_time = time.time()
    return end_time - start_time


def benchmark_simulation(booking_system, num_users, num_runs=5):
    single_times = []
    multi_times = []

    for _ in range(num_runs):
        single_times.append(single_threaded_simulation(booking_system, num_users))
        multi_times.append(multithreaded_simulation(booking_system, num_users))

    avg_single_time = sum(single_times) / num_runs
    avg_multi_time = sum(multi_times) / num_runs

    return avg_single_time, avg_multi_time


if __name__ == "__main__":
    num_users = 30
    rows, cols = 10, 10
    show_id = 19

    theater = BookingSystem(rows=rows, cols=cols, show_id=show_id)
    avg_single_time, avg_multi_time = benchmark_simulation(theater, num_users)

    print("\nPerformance Comparison:")
    print(f"Single-threaded simulation average time: {avg_single_time:.2f} seconds")
    print(f"Multithreaded simulation average time: {avg_multi_time:.2f} seconds")

    if avg_multi_time < avg_single_time:
        speedup = avg_single_time / avg_multi_time
        print(
            f"Multithreaded simulation was {speedup:.2f}x faster than single-threaded."
        )
    else:
        print("Multithreaded simulation was slower than single-threaded.")
