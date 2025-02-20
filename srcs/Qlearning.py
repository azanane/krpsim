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
        self.alpha = 0.2
        self.gamma = 0.7
        self.epsilon = 0.1

        # For plotting metrics
        self.all_epochs = []
        self.all_penalties = []

        self.optimized_stock_evo = {}

        self.current_proccesses = []  # This will be our priority queue (min-heap)
        self.optimized_stock_name = optimized_stock
        # Store optimized processes beforehand to reduce looping
        self.optimized_processes = [
            process for process in processes if any(stock in process.results for stock in optimized_stock)
        ]

        # Precompute max stock values for optimization
        self.max_values = {
            key: max(p.needs.get(key, 0) for p in processes)
            for p in processes for key in p.needs
        }

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
            min_need = self.max_values.get(key, 0) # default 0
        #     real_values_coef = 1
            # if len(self.stocks) > 10:
            #     real_values_coef = .2
            if min_need != 0 and value > min_need * 5:
                state.append(min_need * 5)
        #     elif min_need != 0 and value > min_need * 3:
        #         state.append(min_need * 3)
            # elif min_need != 0 and value > min_need * real_values_coef:
            elif min_need != 0 and value > min_need * 1:
                state.append(min_need * 1)
        #     else:
            else:
                state.append(value)

        return tuple(state)

    def is_doable(self, stocks, proccess_index):

        for item, required_quantity in self.processes[proccess_index].needs.items():
            # If the required quantity of any item is greater than the stock, the process cannot be done
            if stocks.get(item, 0) < required_quantity:
                return False
        return True
    
    def is_anything_doable(self, stocks, check_current_process):
        for i, process in enumerate(self.processes):
            can_do_process = True
            for item, required_quantity in process.needs.items():
                # If the required quantity of any item is greater than the stock, the process cannot be done
                if stocks.get(item, 0) < required_quantity:
                    can_do_process = False
            if can_do_process == True and i != 0:
                return True
        if self.current_proccesses != [] and check_current_process:
            return True
        return False

    def get_reward(self, process_index, is_doable): 
        if is_doable == False:
            return -100
        elif self.processes[process_index].needs and not self.processes[process_index].results:
            return -100


        processTmp = self.processes[process_index]

        # By default we give negative reward for useless action
        reward = -20 

        for key, value in processTmp.results.items():
            # value_needed = processTmp.needs.get(key, 0)
            # if our stock is too big we give negative reward
            if key not in self.optimized_stock_name and self.current_stocks.get(key, 1) > self.max_values.get(key, 1) * 5:
                reward += -10 * value
            # if it is something we want to optimize we give a positive reward
            if key in self.optimized_stock_name and processTmp in self.optimized_processes:
                reward += 50 * value
        
        for key, value in processTmp.needs.items():
            if key in self.optimized_stock_name and self.current_stocks.get(key, 1) > self.max_values.get(key, 1) * 5:
                reward += -10 * value

        return reward

    def run_process(self, process_index):
        process = copy.copy(self.processes[process_index])
        is_doable = self.is_doable(self.stocks, process_index)
        if is_doable:
            if self.verbose == True and process_index != 0:
            # if process_index != 0:
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
            if self.get_state(self.current_stocks) == self.state:
                reward -= 50

        next_state = self.get_state(self.current_stocks)
        return next_state, reward

    def update_q_table(self, process_index):
        state_of_current_stock = self.get_state(self.current_stocks)
        next_state, reward = self.run_process(process_index)

        stateTmp = copy.copy(self.get_state(self.stocks))
        while stateTmp == self.get_state(self.stocks) and self.current_proccesses != [] and process_index == 0:
            self.update_stock_and_time()
            
        old_value = self.q_table[self.state][process_index]
        if type(self.q_table.get(next_state)) != np.ndarray:
            next_max = 0
        else:
            next_max = self.q_table[next_state][np.argmax(self.q_table[next_state])]

        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[self.state][process_index] = new_value

        self.state = self.get_state(self.current_stocks)

    def __run_env(self, verbose = False):
        self.verbose = verbose
        # while (self.current_proccesses or self.state != (0,) and self.current_delay < self.delay):
        while (self.is_anything_doable(self.stocks, True) and self.current_delay < self.delay):

            if type(self.q_table.get(self.state)) != np.ndarray:
                self.q_table[self.state] = np.zeros(len(self.processes))

            if random.uniform(0, 1) < self.epsilon:
                process_index = random.randint(0, len(self.processes) - 1) # Explore process space
            else:
                process_index = np.argmax(self.q_table[self.state]) # Exploit learned values


            self.update_q_table(process_index)

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
        self.epsilon = 0.1
        self.__run_env(True)

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
