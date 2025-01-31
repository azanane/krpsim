from itertools import combinations
import numpy as np
import heapq
import random
import copy
import matplotlib.pyplot as plt


class QLearning:
    def __init__(self, stocks, processes, q_table, optimized_processes=["euro"]):
        self.stocks = stocks
        self.processes = processes
        self.q_table = q_table

        # Hyperparameters
        self.alpha = 0.4
        self.gamma = 0.9
        self.epsilon = 1

        # For plotting metrics
        self.all_epochs = []
        self.all_penalties = []

        self.current_proccesses = []  # This will be our priority queue (min-heap)
        self.optimized_index = [15, 16, 17, 18]
        self.optimized_process_needs = []
        self.optimized_process_name = ['euro']
        self.optimized_processes = [process for index, process in enumerate(processes) if index in self.optimized_index]
        for process in self.optimized_processes:
            for key, value in process.needs.items():
                self.optimized_process_needs.append(key)
        
        self.state = 0
        self.reward = 0
        self.current_delay = 10
        self.action = 0

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
        if process_index not in self.state:
            return -100
        elif self.processes[process_index].needs and not self.processes[process_index].results:
            return -100


        processTmp = self.processes[process_index]

        # reward = processTmp.cost / 100 * -1
        reward = processTmp.delay * -1
        # reward = 0

        if processTmp in self.optimized_processes:
            for key, value in processTmp.results.items():
                if key in self.optimized_process_name:
                    reward = 5 * (value - processTmp.cost)

        return reward

    def run_process(self, process_index):
        process = copy.copy(self.processes[process_index])
        reward = self.get_reward(process_index)

        if process_index in self.state and process_index != 0:
            for key, value in process.needs.items():
                self.stocks[key] -= value
            process.delay += self.current_delay
            heapq.heappush(self.current_proccesses, process)

        next_state = self.get_state()
        self.action += 1

        return next_state, reward

    def update_q_table(self, process_index):
        next_state, reward = self.run_process(process_index)
        
        old_value = self.q_table[self.state][process_index]
        next_max = np.argmax(self.q_table[next_state])

        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[self.state][process_index] = new_value

        self.state = next_state


    def learning(self):
        stockTmp = copy.copy(self.stocks)
        actions = {
            'vente_boite' : 0,
            'vente_tarte_pomme' : 0,
            'vente_tarte_citron' : 0,
            'vente_flan' : 0,
        }
        actions_history = {
            'vente_boite' : [],
            'vente_tarte_pomme' : [],
            'vente_tarte_citron' : [],
            'vente_flan' : [],
        }
        self.epochs = 1

        for i in range(1, 20):
            self.state = self.get_state()
            process_index = -1

            self.current_delay = 0
            self.current_proccesses = []
            self.epochs += 1

            while (self.current_proccesses or self.state != (0,)) and self.epochs % 300000 != 0:
                # if 15 in self.state or 16 in self.state or 17 in self.state or 18 in self.state:
                # if process_index in [15, 14, 13, 11, 17, 18] and process_index in self.state:
                #     print (self.processes[process_index].name)
              
                if random.uniform(0, 1) < self.epsilon:
                    process_index = random.randint(0, len(self.processes) - 1) # Explore process space
                else:
                    process_index = np.argmax(self.q_table[self.state]) # Exploit learned values
                

                # print(f'For state: ${self.state}, better action is ${self.processes[np.argmax(self.q_table[self.state])].name} and action taken is ${self.processes[process_index].name}')
                if self.processes[process_index].name in ["vente_boite", "vente_tarte_pomme", "vente_tarte_citron", "vente_flan"]:
                    actions[self.processes[process_index].name] += 1

                if process_index == 0:
                    stateTmp = copy.copy(self.state)
                    while stateTmp == self.state and self.current_proccesses != []:
                        self.update_stock_and_time()
                    for key in actions:
                        if actions_history[key]:
                            actions_history[key].append(actions[key] + actions_history[key][-1])
                        else:
                            actions_history[key].append(actions[key])
                        actions[key] = 0

                self.update_q_table(process_index)

                self.epochs += 1

            self.stocks = copy.copy(stockTmp)
            if self.epsilon > 0.2:
                self.epsilon -= 0.05
            # if i % 100 == 0:
                # clear_output(wait=True)
            print(f"Episode: {i}, delay: {self.current_delay}, epsilone: {self.epsilon}")
            

            print("Training finished.\n")
        # Define a color map for different lines
        colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']

        plt.figure(figsize=(10, 5))

        for (action, history), color in zip(actions_history.items(), colors):
            plt.plot(history, marker='o', linestyle='-', color=color, linewidth=2, markersize=6, label=action.replace("_", " ").title())

        # Labels, title, legend
        plt.xlabel("Time (Updates)")
        plt.ylabel("Sales Count")
        plt.title("Sales History Over Time")
        plt.legend()
        plt.grid(True)

        # Show the plot
        plt.show()
        print(self.current_delay)
        
        

class Process:
    def __init__(self, name, needs, results, delay, cost = 0):
        self.name = name
        self.needs = needs  # Using a set to represent needs (hashable items)
        self.results = results  # Using a set to represent results (hashable items)
        self.delay = delay
        self.cost = cost

    def __lt__(self, other):
        # Compare based on the delay
        return self.delay < other.delay

stock = {
    "four": 10,
    "euro": 10000,
    "pomme": 0,
    "citron": 0,
    "oeuf": 0,
    "farine": 0,
    "beurre": 0,
    "lait": 0,
    "jaune_oeuf": 0,
    "blanc_oeuf": 0,
    "pate_sablee": 0,
    "pate_feuilletee": 0,
    "tarte_citron": 0,
    "tarte_pomme": 0,
    "flan": 0,
    "boite": 0
}

processes = []
processes.append(Process("rien_faire", {}, {}, 100, 0))
processes.append(Process("buy_pomme", {"euro": 100}, {"pomme": 700}, 200, 100))
processes.append(Process("buy_citron", {"euro": 100}, {"citron": 400}, 200, 100))
processes.append(Process("buy_oeuf", {"euro": 100}, {"oeuf": 100}, 200, 100))
processes.append(Process("buy_farine", {"euro": 100}, {"farine": 800}, 200, 100))
processes.append(Process("buy_beurre", {"euro": 100}, {"beurre": 2000}, 200, 100))
processes.append(Process("buy_lait", {"euro": 100}, {"lait": 2000}, 200, 100))

processes.append(Process("separation_oeuf", {"oeuf": 1}, {"jaune_oeuf": 1, "blanc_oeuf": 1}, 2, 1))
processes.append(Process("reunion_oeuf", {"jaune_oeuf": 1, "blanc_oeuf": 1}, {"oeuf": 1}, 1, 1))
processes.append(Process("do_pate_sablee", {"oeuf": 5, "farine": 100, "beurre": 4, "lait": 5}, {"pate_sablee": 300, "blanc_oeuf": 3}, 300, 17.95)) #12,5 + 5 + 0.2 + 0.25
processes.append(Process("do_pate_feuilletee", {"oeuf": 3, "farine": 200, "beurre": 10, "lait": 2}, {"pate_feuilletee": 100}, 800, 28.6)) # 3 + 25 + 0.5 + 0. 1
processes.append(Process("do_tarte_citron", {"pate_feuilletee": 100, "citron": 50, "blanc_oeuf": 5, "four": 1}, {"tarte_citron": 5, "four": 1}, 60, 46.1)) # 28.6 + 12.5 + 5
processes.append(Process("do_tarte_pomme", {"pate_sablee": 100, "pomme": 30, "four": 1}, {"tarte_pomme": 8, "four": 1}, 50, 10.3)) # 6 + 4.3 
processes.append(Process("do_flan", {"jaune_oeuf": 10, "lait": 4, "four": 1}, {"flan": 5, "four": 1}, 300, 10.2)) # 10 + 0.2 
processes.append(Process("do_boite", {"tarte_citron": 3, "tarte_pomme": 7, "flan": 1, "euro": 30}, {"boite": 1}, 1, 47)) # 36 + 9 + 2
processes.append(Process("vente_boite", {"boite": 100}, {"euro": 55000}, 30, 7700))
processes.append(Process("vente_tarte_pomme", {"tarte_pomme": 10}, {"euro": 100}, 30, 13))
processes.append(Process("vente_tarte_citron", {"tarte_citron": 10}, {"euro": 200}, 30, 120))
processes.append(Process("vente_flan", {"flan": 10}, {"euro": 300}, 30, 20))




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


