import threading
import queue
import random
import time


def producer(shared_queue: queue.Queue, lock, run_event):
    while run_event.is_set():
        with lock:
            if not shared_queue.full():
                item = random.randint(1, 100)
                shared_queue.put(item)
                print(f"Produced: {item}")
        time.sleep(0.1)  # Produce every 0.1 seconds


def consumer(shared_queue: queue.Queue, lock, run_event):
    nums = ""
    while run_event.is_set():
        with lock:
            if not shared_queue.empty():
                item = shared_queue.get()
                print(f"Consumed: {item}")
        time.sleep(0.15)  # Consume every 0.15 seconds


def main():
    # Shared resources
    shared_queue = queue.Queue(maxsize=10)
    lock = threading.Lock()
    run_event = threading.Event()
    run_event.set()  # Set the event to start threads

    # Create threads
    producer_thread = threading.Thread(
        target=producer,
        args=(shared_queue, lock, run_event)
    )
    consumer_thread = threading.Thread(
        target=consumer,
        args=(shared_queue, lock, run_event)
    )

    # Start threads
    producer_thread.start()
    consumer_thread.start()

    # Run for 10 seconds
    time.sleep(10)
    run_event.clear()  # Stop threads gracefully


    # Wait for threads to finish
    producer_thread.join()
    consumer_thread.join()

    print("Program terminated after 10 seconds.")


if __name__ == "__main__":
    main()

