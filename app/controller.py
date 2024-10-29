import threading


class PhilosopherActions:
    """
    Classe com as ações que os filosofos conseguem fazer;
    Tem como função atualizar as mensagens e listas que são apresentadas na interface.

    Está separado para o arquivo 'threads.py' poder dar foco so ao controle das threads
    """
    def __init__(self, n_philosophers):
        self.mutex = threading.Lock()

        self.states = ["F"] * n_philosophers
        self.state_forks = ["L"] * n_philosophers
        self.count_meals = [0] * n_philosophers
        self.n_philosophers = n_philosophers

    def philosophizing(self, philosopher_id):
        with self.mutex:
            self.states[philosopher_id] = "F"

    def eating(self, philosopher_id):
        with self.mutex:
            self.states[philosopher_id] = "C"
            self.count_meals[philosopher_id] += 1

    def require_first_fork(self, philosopher_id):
        with self.mutex:
            self.state_forks[philosopher_id] = "R"

    def require_second_fork(self, philosopher_id):
        with self.mutex:
            self.state_forks[(philosopher_id + 1) % self.n_philosophers] = "R"

    def drop_forks(self, philosopher_id):
        with self.mutex:
            self.state_forks[philosopher_id] = "L"
            self.state_forks[(philosopher_id + 1) % self.n_philosophers] = "L"