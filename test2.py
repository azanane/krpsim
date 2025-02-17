from itertools import combinations
import numpy as np
import heapq
import random
import copy
import matplotlib.pyplot as plt


class QLearning:
    def __init__(self, stocks, processes, q_table, optimized_processes=["euro"]):
        self.stocks = stocks
        self.current_stocks = copy.copy(stock)
        self.processes = processes
        self.q_table = q_table

        # Hyperparameters
        self.alpha = 0.2
        self.gamma = 0.9
        self.epsilon = 0.5

        # For plotting metrics
        self.all_epochs = []
        self.all_penalties = []

        self.optimized_stock_evo = {}

        self.current_proccesses = []  # This will be our priority queue (min-heap)
        self.optimized_index = [15,16,17,18]
        self.optimized_process_name = optimized_processes
        self.optimized_processes = [process for index, process in enumerate(processes) if index in self.optimized_index]
        self.max_values = {}
        
        for process in self.processes:
            for key, value in process.needs.items():
                value_tmp = self.max_values.get(key)
                if value_tmp == None or value_tmp < value:
                    self.max_values[key] = value

        
        self.state = 0
        self.reward = 0
        self.current_delay = 0
        self.action = 0

        self.not_training = False

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

        # faire un graph de l'evo de l'argent en fonction de l'epoch et du delay
        if self.not_training:
            self.optimized_stock_evo[self.current_delay] = self.stocks["euro"]

    def get_state(self, stocks):
        state = []

        for i, process in enumerate(self.processes):
            # Check if all required items (needs) are available in stock
            can_do_process = True
            for item, required_quantity in process.needs.items():
                # If the required quantity of any item is greater than the stock, the process cannot be done
                if stocks.get(item, 0) < required_quantity:
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

        reward = -1
        # reward -= processTmp.cost * 5 # amoindrir la reward en fonction du cout (pas fou)
        # reward -= processTmp.delay * 1 #amoindrir la reward en fonction du delai (pas fou)

    
        for key, value in processTmp.results.items():
            # Si on a le stock deja au moins 20 fois superieur au resultat alors on achete plus 
            if key not in self.optimized_process_name and self.stocks[key] > self.max_values[key] * 1:
                reward += -30
            # On donne une reward en fonction de la quantité du resultat
            if key in self.optimized_process_name and processTmp in self.optimized_processes:
                reward += 5 * value

        return reward

    def run_process(self, process_index):
        process = copy.copy(self.processes[process_index])
        reward = self.get_reward(process_index)

        if process_index in self.state and process_index != 0:
            for key, value in process.needs.items():
                self.stocks[key] -= value
                self.current_stocks[key] -= value
            process.delay += self.current_delay
            heapq.heappush(self.current_proccesses, process)
            for key, value in process.results.items():
                self.current_stocks[key] += value
            next_state = self.get_state(self.current_stocks)
        else:
            next_state = self.get_state(self.stocks)
        # if next_state == (0,):
        #     reward -= 500
        return next_state, reward

    def update_q_table(self, process_index):
        state_of_current_stock = self.get_state(self.current_stocks)
        next_state, reward = self.run_process(process_index)
        
        old_value = self.q_table[self.state][process_index]
        if type(self.q_table.get(next_state)) != np.ndarray or next_state == self.state or state_of_current_stock == next_state:
            next_max = 0
        else:
            next_max = self.q_table[next_state][np.argmax(self.q_table[next_state])]

        # new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[self.state][process_index] = new_value

        self.state = self.get_state(self.stocks)


    def learning(self):
        stockTmp = copy.copy(self.stocks)
        actions = {}
        actions_history = {}
        self.epochs = 1

        for i in range(1, 10):
            # actions_tmp = copy.copy(actions)
            self.state = self.get_state(self.stocks)
            process_index = -1

            self.current_delay = 0
            self.current_proccesses = []
            self.epochs += 1

            for key in self.stocks:
                if self.max_values.get(key):
                    self.stocks[key] = self.max_values[key] * random.randint(1, 10)
                    print(f"{key}  :  {self.stocks[key]}")

            self.current_stocks = copy.copy(self.stocks)

            print()


            while (self.current_proccesses or self.state != (0,)) and self.current_delay < 1000000:

                if type(self.q_table.get(self.state)) != np.ndarray:
                    self.q_table[self.state] = np.zeros(len(processes))

                # if 15 in self.state or 16 in self.state or 17 in self.state or 18 in self.state:
                # if process_index in [15, 14, 13, 11, 17, 18] and process_index in self.state:
                #     print (self.processes[process_index].name)

                if random.uniform(0, 1) < self.epsilon:
                    process_index = random.randint(0, len(self.processes) - 1) # Explore process space
                else:
                    process_index = np.argmax(self.q_table[self.state]) # Exploit learned values


                # print(f'For state: ${self.state}, better action is ${self.processes[np.argmax(self.q_table[self.state])].name} and action taken is ${self.processes[process_index].name}')
                # if self.processes[process_index].name in ["vente_boite", "vente_tarte_pomme", "vente_tarte_citron", "vente_flan", "rien_faire"] and process_index in self.state:
                #     actions[self.processes[process_index].name] += 1

                # if process_index in self.state:
                #     if actions.get(self.processes[process_index].name) != None:
                #         actions[self.processes[process_index].name] += 1
                #     else:
                #         actions[self.processes[process_index].name] = 1

                if process_index == 0:
                    stateTmp = copy.copy(self.state)
                    while stateTmp == self.state and self.current_proccesses != []:
                        self.update_stock_and_time()
                    # for key in actions:
                    #     if actions_history.get(key):
                    #         actions_history[key].append(actions[key])
                    #     else:
                    #         actions_history[key] = [actions[key]]

                self.update_q_table(process_index)

                self.epochs += 1


            print(f"Episode: {i}, delay: {self.current_delay}, epsilone: {self.epsilon}, euro : {self.stocks['euro']}")
            # for key, value in actions.items():
            #     for key2, value2 in actions_tmp.items():
            #         if key == key2:
            #             print(f'Action: {key}: {value - value2}')
            # for key, value in self.stocks.items():
            #     print(f'stock: {key}: {value}')

            if self.epsilon > 0.2:
                self.epsilon -= 0.025

            # self.stocks = copy.copy(stockTmp)
            # self.current_stocks = copy.copy(stockTmp)
            print("Training finished.\n")



        self.not_training = True

        self.epochs = 1


        self.state = self.get_state(self.stocks)
        process_index = -1

        self.current_delay = 0
        self.current_proccesses = []
        self.epochs += 1
            
        self.stocks = copy.copy(stockTmp)
        self.current_stocks = copy.copy(self.stocks)
        while (self.current_proccesses or self.state != (0,)) and self.current_delay < 10000000:

            if type(self.q_table.get(self.state)) != np.ndarray:
                self.q_table[self.state] = np.zeros(len(processes))
                    
            # if 15 in self.state or 16 in self.state or 17 in self.state or 18 in self.state:
            # if process_index in [15, 14, 13, 11, 17, 18] and process_index in self.state:
            #     print (self.processes[process_index].name)

            if random.uniform(0, 1) < self.epsilon:
                process_index = random.randint(0, len(self.processes) - 1) # Explore process space
            else:
                process_index = np.argmax(self.q_table[self.state]) # Exploit learned values


            # print(f'For state: ${self.state}, better action is ${self.processes[np.argmax(self.q_table[self.state])].name} and action taken is ${self.processes[process_index].name}')
            # if self.processes[process_index].name in ["vente_boite", "vente_tarte_pomme", "vente_tarte_citron", "vente_flan", "rien_faire"] and process_index in self.state:
            #     actions[self.processes[process_index].name] += 1

            if process_index in self.state:
                if actions.get(self.processes[process_index].name) != None:
                    actions[self.processes[process_index].name] += 1
                else:
                    actions[self.processes[process_index].name] = 1

            if process_index == 0:
                stateTmp = copy.copy(self.state)
                while stateTmp == self.state and self.current_proccesses != []:
                    self.update_stock_and_time()
                for key in actions:
                    if actions_history.get(key):
                        actions_history[key].append(actions[key])
                    else:
                        actions_history[key] = [actions[key]]

            self.update_q_table(process_index)

            self.epochs += 1


        for key, value in actions.items():
            print(f'Action: {key}: {value}')
        
        print(self.stocks)


        # Define a color map for different lines
        # print(len(self.q_table))
        # for state, value in self.q_table.items():
        #     print(f'State: {state}, values: {value}')

        x_values = list(self.optimized_stock_evo.keys())
        y_values = list(self.optimized_stock_evo.values())

        # Creating the plot
        plt.plot(x_values, y_values)

        # Adding title and labels
        plt.title('Optimized Stock Evolution')
        plt.xlabel('Time (or other x-axis variable)')
        plt.ylabel('Stock Value')

        # Show the plot
        plt.show()
        # print(self.current_delay)
        
        

class Process:
    def __init__(self, name, needs, results, delay, cost = 0, delay_to_make = 0):
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
processes.append(Process("rien_faire", {}, {}, 50, 0))
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

# do_pate_sablee = 10 + 25 + 0.4 + 0.5 + 300 = 326
# do_pate_feuilletee = 6 + 50 + 1 + 0.2 + 800 = 857
# do_tarte_citron = 857 + 25 + 0.5 + 60 = 968
# do_tarte_pommes = 326 + 9 + 50 = 385
# do_flan = 20 + 40 + 0.4 + 300 =  361
# do_boite = 581 + 337 + 72 = 990
# vente_boite = 99000
# vente_tarte_pomme = 481
# vente_tarte_citron = 1936
# vente_flan = 722
# Pour 10000 => vente_tarte_pomme => 1800 euros
# Pour 10000 => vente_flan => 3626 euros
# Pour 100000 => vente_boite => 47300
# Pour 100000 => vente_tarte_pomme => 18087
# Pour 100000 => vente_flan => 38781






q_table = {}

# for i in range(0, len(processes) + 1):
#     for comb in combinations(range(len(processes)), i):
#         q_table[comb] = np.zeros(len(processes))




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


