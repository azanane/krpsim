from itertools import combinations
import numpy as np
import heapq
import random
import copy


class QLearning:
    def __init__(self, stocks, processes, q_table, optimized_processes=["marelle", "moi"]):
        self.stocks = stocks
        self.processes = processes
        self.q_table = q_table

        # Hyperparameters
        self.alpha = 0.1
        self.gamma = 0.8
        self.epsilon = 0.2

        # For plotting metrics
        self.all_epochs = []
        self.all_penalties = []

        self.current_proccesses = []  # This will be our priority queue (min-heap)
        self.optimized_processes = optimized_processes 


        self.state = 0
        self.reward = 0
        self.current_delay = 10

        self.learning()

    def get_processes_with_smallest_delay(self):
        """Retrieve all processes with the smallest delay."""
        if not self.current_proccesses:
            return []

        # Get the smallest delay
        smallest_delay = self.current_proccesses[0].delay
        processes_with_smallest_delay = []

        # Pop all processes with the smallest delay
        while self.current_proccesses and self.current_proccesses[0].delay == smallest_delay:
            process = heapq.heappop(self.current_proccesses)
            processes_with_smallest_delay.append(process)

        self.current_delay = smallest_delay

        # Return the list of processes with the smallest delay
        return processes_with_smallest_delay

    def update_stock_and_time(self):
        smallest_process = self.get_processes_with_smallest_delay()
        for process in smallest_process:
            for key, value in process.results.items():
                self.stocks[key] += value
        self.state = self.get_state()

    def get_state(self):
        state = []

        for i, process in enumerate(self.processes):
            # Check if all required items (needs) are available in stock
            can_do_process = True
            for item, required_quantity in process.needs.items():
                # If the required quantity of any item is greater than the stock, the process cannot be done
                if self.stocks.get(item, 0) < required_quantity:
                    can_do_process = False
                    break
        
            if can_do_process:
                # If all requirements are met, add the process index to the list
                state.append(i)

        return tuple(state)

    def get_reward(self, process_index): 
        if process_index not in self.state :
            return -100
        elif not self.processes[process_index].results:
            return -100

        reward = 0

        for key, value in self.processes[process_index].needs.items() :
            if key in self.optimized_processes :
                reward -= 10 * value

        for key, value in self.processes[process_index].results.items() :
            if key in self.optimized_processes :
                reward += 10 * value

        return reward 

    def run_process(self, process_index):
        process = copy.copy(self.processes[process_index])
        if process_index in self.state:
            for key, value in process.needs.items():
                stock[key] -= value
            process.delay += self.current_delay
            heapq.heappush(self.current_proccesses, process)
        reward = self.get_reward(process_index)

        next_state = self.get_state()

        return next_state, reward

    def learning(self):
        for i in range(1, 1000):
            self.state = (0,) # or random state

            self.epochs, self.reward = 0, 0
            available_proccess = self.get_state()
            self.state = tuple(available_proccess)


            while self.current_proccesses or available_proccess:
                if not available_proccess:
                    self.update_stock_and_time()

                if random.uniform(0, 1) < self.epsilon:
                    process_index = random.randint(0, len(self.processes) - 1) # Explore process space
                else:
                    process_index = np.argmax(self.q_table[self.state]) # Exploit learned values

                next_state, reward = self.run_process(process_index)
        
                old_value = self.q_table[self.state][process_index]
                next_max = np.argmax(self.q_table[next_state])
        
                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                self.q_table[self.state][process_index] = new_value


                self.state = next_state
                available_proccess = next_state
                self.epochs += 1
        
            if i % 100 == 0:
                # clear_output(wait=True)
                print(f"Episode: {i}")

            print("Training finished.\n")
        
        

class Process:
    def __init__(self, name, needs, results, delay):
        self.name = name
        self.needs = needs  # Using a set to represent needs (hashable items)
        self.results = results  # Using a set to represent results (hashable items)
        self.delay = delay

    def __lt__(self, other):
        # Compare based on the delay
        return self.delay < other.delay

stock = {
    "bonbon": 10,
    "moi": 1,
    "marelle": 0
}

processes = []
processes.append(Process("manger", {"bonbon": 1}, {}, 10))
processes.append(Process("jouer_a_la_marelle", {"bonbon": 5, "moi": 1}, {"moi": 1, "marelle": 1}, 20))
processes.append(Process("parier_avec_un_copain", {"bonbon": 2, "moi": 1}, {"moi": 1, "bonbon": 3}, 10))
processes.append(Process("parier_avec_un_autre_copain", {"bonbon": 2, "moi": 1}, {"moi": 1, "bonbon": 1}, 10))
processes.append(Process("se_battre_dans_la_cours", {"moi": 1}, {"moi": 1, "bonbon": 1}, 50))

q_table = {}

for i in range(0, len(processes) + 1):
    for comb in combinations(range(len(processes)), i):
        q_table[comb] = np.zeros(len(processes))
    


qlearn = QLearning(stock, processes, q_table)


# env.step(process):
#   update_stock(process)
#   current_process[current_time + process.time].append(process)
#   next_state = calculate_state(stock)
#   reward = get_reward(process, stock)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#


# print(len(states))
# print(states)


