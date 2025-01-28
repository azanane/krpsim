from itertools import combinations
import numpy as np
import heapq
import random


# class Stock:
#     def __init__(self, name="", quantity=0):
#         self.name = name
#         self.quantity = quantity


class Process:
    def __init__(self, name, needs, results, delay):
        self.name = name
        self.needs = needs  # Using a set to represent needs (hashable items)
        self.results = results  # Using a set to represent results (hashable items)
        self.delay = delay

# heapq.heappush(self.heap, (process.delay, process))
def get_processes_with_smallest_delay(current_proccesses):
    """Retrieve all processes with the smallest delay."""
    if not current_proccesses:
        return []

    # Get the smallest delay
    smallest_delay = current_proccesses[0][0]
    processes_with_smallest_delay = []

    # Pop all processes with the smallest delay
    while current_proccesses and current_proccesses[0][0] == smallest_delay:
        _, process = heapq.heappop(current_proccesses)
        processes_with_smallest_delay.append(process)

    # Return the list of processes with the smallest delay
    return current_proccesses, processes_with_smallest_delay, smallest_delay


def can_be_done(stock, processes):
    processable_indices = []

    for i, process in enumerate(processes):
        # Check if all required items (needs) are available in stock
        can_do_process = True
        for item, required_quantity in process.needs.items():
            # If the required quantity of any item is greater than the stock, the process cannot be done
            if stock.get(item, 0) < required_quantity:
                can_do_process = False
                break
        
        if can_do_process:
            # If all requirements are met, add the process index to the list
            processable_indices.append(i)

    return processable_indices

def update_stock_and_time(current_processes, stock):
    current_proccesses, smallest_process, delay = get_processes_with_smallest_delay(current_processes)
    for process in smallest_process.results:
        for result in process.needs:
            stock[result[0]] += result[1]
    return current_proccesses, stock, delay

    

def run_process(state, current_processes, process, stock, current_delay):
    if process in state:
        for result in process.reuslts:
            stock[result[0]] -= result[1]
    # reward = get_reward(state, process)


    

stock = {
    "euros": 1000,
    "pomme": 0,
    "tarte": 0
}

processes = []
processes.append(Process("make_pomme", {"euros": 100}, {"pomme": 50}, 10))
processes.append(Process("make_tarte", {"pomme": 100}, {"tarte": 1}, 5))
processes.append(Process("make_euro", {"tarte": 1}, {"euros": 200}, 20))

q_table = {}

for i in range(1, len(processes) + 1):
    for comb in combinations(range(len(processes)), i):
        q_table[comb] = np.zeros(len(processes))


# # Hyperparameters
alpha = 0.1
gamma = 0.8
epsilon = 0.1

# # For plotting metrics
all_epochs = []
all_penalties = []

current_proccesses = []  # This will be our priority queue (min-heap)
    





for i in range(1, 1000):
    state = (0,) # or random state

    epochs, reward, = 0, 0, 0
    available_proccess = can_be_done(stock, processes)
    current_delay = 0

    while current_proccesses or available_proccess:
        if not available_proccess:
            current_proccesses, stock, current_delay = update_stock_and_time(current_proccesses, stock)
          

        state = tuple(can_be_done(stock, processes))
        if random.uniform(0, 1) < epsilon:
            process = processes[random.randint(len(processes))] # Explore process space
        else:
            process = np.argmax(q_table[state]) # Exploit learned values

        next_state, reward = env.step(process)
        
        old_value = q_table[state][index of process]
        next_max = np.argmax(q_table[next_state])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, process] = new_value


        state = next_state
  epochs += 1
        
    if i % 100 == 0:
        clear_output(wait=True)
        print(f"Episode: {i}")

print("Training finished.\n")




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


