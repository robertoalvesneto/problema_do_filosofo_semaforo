import time

from app.controller import PhilosopherActions

def philosopher_thread(actions: PhilosopherActions, window, stop_event, philosopher_id, forks, n_philosophers):
    while not stop_event.is_set():
        actions.philosophizing(philosopher_id)
        time.sleep(1)

        fork_esq = forks[philosopher_id]
        fork_dir = forks[(philosopher_id + 1) % n_philosophers]

        first_fork, second_fork = None, None
        if philosopher_id % 2 == 0:
            first_fork, second_fork = fork_esq, fork_dir
        else:
            first_fork, second_fork = fork_dir, fork_esq

        first_fork.acquire()
        actions.require_first_fork(philosopher_id)
        window.update_signal.update.emit()

        second_fork.acquire()
        actions.require_second_fork(philosopher_id)
        actions.eating(philosopher_id)
        window.update_signal.update.emit()

        time.sleep(2)

        first_fork.release()
        second_fork.release()

        actions.philosophizing(philosopher_id)
        actions.drop_forks(philosopher_id)
        window.update_signal.update.emit()
