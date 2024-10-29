import sys
import threading
import time
from PyQt5.QtWidgets import QApplication

from app.interface import PhilosopherTableWindow
from app.controller import PhilosopherActions
from app.threads import philosopher_thread

N_PHILOSOPHERS = 5
PHILOSOPHERS_THREADS = []

stop_event = threading.Event()

def update_states(window):
    while True:
        time.sleep(1)
        window.update_signal.update.emit()

def start_philosophers(philosopher_actions, window, forks, n_philosophers):
    for i in range(n_philosophers):
        t = threading.Thread(target=philosopher_thread, args=(philosopher_actions, window, stop_event, i, forks, n_philosophers))
        t.daemon = True
        PHILOSOPHERS_THREADS.append(t)
        t.start()
    return PHILOSOPHERS_THREADS

def stop_philosophers():
    stop_event.set()
    for t in PHILOSOPHERS_THREADS:
        t.join()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    forks = [threading.Semaphore(1) for _ in range(N_PHILOSOPHERS)]

    philosopher_actions = PhilosopherActions(N_PHILOSOPHERS)

    window = PhilosopherTableWindow(philosopher_actions, lambda: stop_philosophers())

    start_philosophers(philosopher_actions, window, forks, N_PHILOSOPHERS)

    sys.exit(app.exec_())

