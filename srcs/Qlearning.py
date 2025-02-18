import copy
import random
import numpy as np
import heapq
import matplotlib.pyplot as plt

class QLearning:
    def __init__(self, stocks, processes, optimized_stock=["euro"], delay = 1000):
        self.stocks = stocks
        self.current_stocks = copy.copy(stocks)
        self.processes = processes
        self.q_table = {}

        # Hyperparameters
        self.alpha = 0.4
        self.gamma = 0.9
        self.epsilon = 0.1

        # For plotting metrics
        self.all_epochs = []
        self.all_penalties = []

        self.optimized_stock_evo = {}

        self.current_proccesses = []  # This will be our priority queue (min-heap)
        self.optimized_stock_name = optimized_stock
        self.optimized_processes = []
        for stock_name in self.optimized_stock_name:
            for process in processes:
                if stock_name in process.results:
                    self.optimized_processes.append(process)

        self.max_values = {}
        
        for process in self.processes:
            for key, value in process.needs.items():
                value_tmp = self.max_values.get(key)
                if value_tmp == None or value_tmp < value:
                    self.max_values[key] = value

        self.actions = {}
        self.actions_history = []

        
        self.state = 0
        self.reward = 0
        self.current_delay = 0
        self.delay = delay

        self.not_training = False

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
            self.optimized_stock_evo[self.current_delay] = self.stocks[self.optimized_stock_name[0]]

    def get_state(self, stocks):
        state = []

        for key, value in stocks.items():
            state.append(value)

        return tuple(state)


    # def get_state(self, stocks):
    #     state = []
        
    #     for key, value in stocks.items():
    #         min_need = self.max_values.get(key, 0) # default 0
        
    #         # Categorize dynamically based on min_need
    #         if value or min_need == 0:
    #             category = 0  # No stock
    #         elif value <= min_need:
    #             category = 1  # Bare minimum available
    #         elif value <= min_need * 2:
    #             category = 2  # Sufficient stock
    #         elif value <= min_need * 5:
    #             category = 3  # Well-stocked
    #         else:
    #             category = 4  # Excess stock

    #         state.append(category)

    #     return tuple(state)

    def is_doable(self, stocks, proccess_index):

        for item, required_quantity in self.processes[proccess_index].needs.items():
            # If the required quantity of any item is greater than the stock, the process cannot be done
            if stocks.get(item, 0) < required_quantity:
                return False
        return True
    
    def is_anything_doable(self):
        for i, process in enumerate(self.processes):
            can_do_process = True
            for item, required_quantity in process.needs.items():
                # If the required quantity of any item is greater than the stock, the process cannot be done
                if self.stocks.get(item, 0) < required_quantity:
                    can_do_process = False
            if can_do_process == True and i != 0:
                return True
        if self.current_proccesses != []:
            return True
        return False

    def get_reward(self, process_index, is_doable): 
        if is_doable == False:
            return -100
        elif self.processes[process_index].needs and not self.processes[process_index].results:
            return -100


        processTmp = self.processes[process_index]

        reward = -1
        # reward -= processTmp.cost * 5 # amoindrir la reward en fonction du cout (pas fou)
        # reward -= processTmp.delay * 1 #amoindrir la reward en fonction du delai (pas fou)

        
        for key, value in processTmp.results.items():
            value_needed = processTmp.needs.get(key, 0)
            if value_needed != 0 and value_needed > value:
                reward -= 50 * value_needed
            # Si on a le stock deja au moins 20 fois superieur au resultat alors on achete plus 
            if key not in self.optimized_stock_name and self.stocks[key] > self.max_values[key] * 10:
                reward += -30 * value
            # On donne une reward en fonction de la quantité du resultat
            elif key in self.optimized_stock_name and processTmp in self.optimized_processes:
                reward += 50 * (value - value_needed)

        return reward

    def run_process(self, process_index):
        process = copy.copy(self.processes[process_index])
        is_doable = self.is_doable(self.stocks, process_index)
        if is_doable: 
            if self.verbose and process_index != 0:
                print(f'{self.current_delay}: {self.processes[process_index].name}')
            if self.actions.get(process.name) != None:
                self.actions[process.name] += 1
            else:
                self.actions[process.name] = 1
        reward = self.get_reward(process_index, is_doable)

        # Remove from the stock the needs, and upgrade directly by removing and adding de current_stock
        if is_doable and process_index != 0:
            for key, value in process.needs.items():
                self.stocks[key] -= value
                self.current_stocks[key] -= value
            process.delay += self.current_delay
            heapq.heappush(self.current_proccesses, process)
            for key, value in process.results.items():
                self.current_stocks[key] += value

        next_state = self.get_state(self.current_stocks)

        # If we can only do nothing and there is no current proccess it is then end
        if next_state == (0,) and len(self.current_proccesses) == 0:
            reward -= 100
        return next_state, reward

    def update_q_table(self, process_index):
        state_of_current_stock = self.get_state(self.current_stocks)
        next_state, reward = self.run_process(process_index)

        if process_index == 0:
            stateTmp = copy.copy(self.state)
            # while stateTmp == self.state and self.current_proccesses != []:
            self.update_stock_and_time()
            if stateTmp == next_state:
                reward -= 20
        
        old_value = self.q_table[self.state][process_index]
        # if reward <= 0:
        #     reward = min(reward, min(old_value * 1.1, old_value * -1.1))
        # if type(self.q_table.get(next_state)) != np.ndarray or next_state == self.state or state_of_current_stock == next_state:
        #     next_max = 0
        # else:
        # If we don´t have the q_table set for next_state, the next max will be 0
        if type(self.q_table.get(next_state)) != np.ndarray:
            next_max = 0
        else:
            next_max = self.q_table[next_state][np.argmax(self.q_table[next_state])]

        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[self.state][process_index] = new_value

        self.state = self.get_state(self.stocks)

    def __run_env(self, verbose = False):
        self.verbose = verbose
        # while (self.current_proccesses or self.state != (0,) and self.current_delay < self.delay):
        while (self.is_anything_doable() and self.current_delay < self.delay):

            if type(self.q_table.get(self.state)) != np.ndarray:
                self.q_table[self.state] = np.zeros(len(self.processes))

            if random.uniform(0, 1) < self.epsilon:
                process_index = random.randint(0, len(self.processes) - 1) # Explore process space
            else:
                process_index = np.argmax(self.q_table[self.state]) # Exploit learned values

            # if process_index == 0:
            #     stateTmp = copy.copy(self.state)
            #     # while stateTmp == self.state and self.current_proccesses != []:
            #     self.update_stock_and_time()
            
            # if verbose and process_index in self.state and process_index != 0:
            #     print(f'{self.current_delay}: {self.processes[process_index].name}')
            
            self.update_q_table(process_index)
        print("end")

    def __reinitialize(self, stockTmp, do_random_stock = False):
        if do_random_stock:
            for key in self.stocks:
                if self.max_values.get(key):
                    self.stocks[key] = self.max_values[key] * random.randint(1, 10)
                else:
                    self.stocks[key] = 0
                print(f"{key}  :  {self.stocks[key]}")
        else:
            self.stocks = copy.copy(stockTmp)

        self.current_stocks = copy.copy(self.stocks)

        self.state = self.get_state(self.stocks)
        self.current_delay = 0
        self.current_proccesses = []

    def train(self, epochs):
        stockTmp = copy.copy(self.stocks)

        for i in range (1, epochs):
            if random.uniform(0, 1) < 1:
                self.__reinitialize(stockTmp, False)
            else:
                self.__reinitialize(stockTmp, True)
            self.__run_env(False)
            self.actions_history.append(self.actions)
            self.actions = {}
            print(f"Episode: {i}, delay: {self.current_delay}, epsilone: {self.epsilon}, {self.optimized_stock_name}: {[value for key, value in self.stocks.items() if key in self.optimized_stock_name]}")
            print(f"State number: {len(self.q_table)}")

            if self.epsilon > 0.2 and i % (epochs / 10) == 0:
                self.epsilon -= 0.025
        
        self.__reinitialize(stockTmp, False)

    def run(self):
        self.not_training = True
        self.delay = 10000000
        self.epsilon = 0.1
        self.__run_env(True)
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
