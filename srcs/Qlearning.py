import copy
import random
import numpy as np
import heapq
import matplotlib.pyplot as plt
import collections

class QLearning:
    def __init__(self, stocks, processes, optimized_stock=["euro"], delay = 1000):
        self.stocks = stocks
        self.current_stocks = copy.copy(stocks)
        self.processes = processes
        self.q_table = {}

        # Hyperparameters
        self.alpha = 0.3
        self.gamma = 0.8
        self.epsilon = 0.5
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

        
        self.state = 0
        self.reward = 0
        self.current_delay = 0
        self.delay = delay
        self.action = 0

        self.not_training = False

        self.stocks_prediction =  copy.copy(stocks)
        self.state_prediction = ()
        self.solution = ()
        self.new_solution_processes = {}

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

        for i, process in enumerate(self.processes):
            # Check if all required items (needs) are available in stock
            can_do_process = True
            for item, required_quantity in process.needs.items():
                # If the required quantity of any item is greater than the stock, the process cannot be done
                if stocks.get(item, 0) < required_quantity:
                    can_do_process = False
                    break
            if can_do_process == True and process not in self.optimized_processes:
                non_needed_stocks_len = 0
                for item, result_quantity in process.results.items():
                    # If the required quantity of any item is greater than the stock, the process cannot be done
                     if (self.max_values.get(item, 0) and self.max_values.get(item, 0) <= self.stocks[item]) or (process.needs.get(item) != None and result_quantity < process.needs[item]):
                        non_needed_stocks_len += 1
                if non_needed_stocks_len == len(process.results) and non_needed_stocks_len != 0:
                    can_do_process = False
        
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

        reward = -10
        # reward -= processTmp.cost * 5 # amoindrir la reward en fonction du cout (pas fou)
        # reward -= processTmp.delay * 1 #amoindrir la reward en fonction du delai (pas fou)

        for key, value in processTmp.needs.items():
            # Si on a le stock deja au moins 20 fois superieur au resultat alors on achete plus 
            # if key not in self.optimized_stock_name and self.stocks[key] > self.max_values[key] * 10:
            #     reward += -30
            # On donne une reward en fonction de la quantité du resultat
            if key in self.optimized_stock_name and processTmp in self.optimized_processes:
                reward -= value


        for key, value in processTmp.results.items():
            # Si on a le stock deja au moins 20 fois superieur au resultat alors on achete plus 
            # if key not in self.optimized_stock_name and self.stocks[key] > self.max_values[key] * 10:
            #     reward += -30
            # On donne une reward en fonction de la quantité du resultat
            if key in self.optimized_stock_name and processTmp in self.optimized_processes:
                reward += value

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
        test_state = self.get_state(self.stocks_prediction)
        if test_state == (0,):
            reward -= 100
        return next_state, reward

    def update_q_table(self, process_index):
        state_of_current_stock = self.get_state(self.current_stocks)
        next_state, reward = self.run_process(process_index)
        
        old_value = self.q_table[self.state][process_index]
        if self.state == state_of_current_stock and process_index == 0 and process_index in self.state and old_value != 0:
            reward = min(reward, min(old_value * 1.1, old_value * -1.1))
        if type(self.q_table.get(next_state)) != np.ndarray or next_state == self.state or state_of_current_stock == next_state:
            next_max = 0
        else:
            next_max = self.q_table[next_state][np.argmax(self.q_table[next_state])]

        # new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[self.state][process_index] = new_value

        self.state = self.get_state(self.stocks)

    def get_stock_prediction(self, process_index_execute):
        
        for key, value in self.processes[process_index_execute].needs.items():
            self.stocks_prediction[key] -= value

        for key, value in self.processes[process_index_execute].results.items():
            self.stocks_prediction[key] += value
    
    def get_state_prediction(self):

        state_prediction = []
 
        for i, process in enumerate(self.processes):
            can_do_process = True
            for item, required_quantity in process.needs.items():
                # If the required quantity of any item is greater than the stock, the process cannot be done
                if self.stocks_prediction.get(item, 0) < required_quantity:
                    can_do_process = False
                    break

            if can_do_process == True and process not in self.optimized_processes:
                non_needed_stocks_len = 0
                for item, result_quantity in process.results.items():
                    # If the required quantity of any item is greater than the stock, the process cannot be done
                    if (self.max_values.get(item, 0) and self.max_values.get(item, 0) <= self.stocks_prediction[item]) or (process.needs.get(item) != None and result_quantity < process.needs[item]):
                        non_needed_stocks_len += 1
                if non_needed_stocks_len == len(process.results) and non_needed_stocks_len != 0:
                    can_do_process = False
            
            if can_do_process:
                # If all requirements are met, add the process index to the list
                state_prediction.append(i)

        self.state_prediction = tuple(state_prediction)

    def __run_env(self, verbose = False):

        process_history = {}
        for index in self.processes:
            process_history[index.name] = 0

        self.stocks_prediction = copy.copy(self.stocks)

        self.new_solution_processes = {}
        new_processes = []
        index_solution_processes = 0

        while (self.current_proccesses or self.state != (0,) and self.current_delay < self.delay):

            if type(self.q_table.get(self.state)) != np.ndarray:
                self.q_table[self.state] = np.zeros(len(self.processes))

            self.get_state_prediction()

            if random.uniform(0, 1) < self.epsilon:
                process_index = random.randint(0, len(self.state_prediction) - 1) # Explore process space
                process_index = self.state_prediction[process_index]
            else:
                state_q_table = []
                for index in self.state_prediction:
                    state_q_table.append(self.q_table[self.state][index])

                process_index = np.argmax(state_q_table)
                process_index = self.state_prediction[process_index] # Exploit learned values

            # If an action is in the state prediction but not in the real state (we do nothing first to get our stocks)
            if process_index not in self.state:
                process_index = 0
            else:
                self.get_stock_prediction(process_index)

            if process_index in self.state and process_index != 0:
                new_processes.append(process_index)
                # We sort our list of new processes in order to don´t re-use it in the list of solution
                new_processes.sort()


            # Keep an history of used processes
            if self.processes[process_index].name in process_history and process_index != 0:
                process_history[self.processes[process_index].name] += 1
            elif process_index != 0:
                process_history[self.processes[process_index].name] = 1

            if process_index == 0:
                stateTmp = copy.copy(self.state)
                while stateTmp == self.state and self.current_proccesses != []:
                    self.update_stock_and_time()

                if new_processes:
                    
                    self.new_solution_processes[index_solution_processes] = copy.copy(new_processes)
                    index_solution_processes += 1
                    new_processes.clear()

            
            if verbose and process_index in self.state and process_index != 0:
                print(f'{self.current_delay}: {self.processes[process_index].name}')
            
            self.update_q_table(process_index)

        if self.stocks[self.optimized_stock_name[0]] > 0:
            fitness = self.current_delay / self.stocks[self.optimized_stock_name[0]]
        else:
            fitness = 0
 
        if not self.solution or self.solution[0] > fitness:
            self.solution = (fitness, self.new_solution_processes)

        print(self.stocks)
        print(process_history)
        print("end")

    def __reinitialize(self, stockTmp, do_random_stock = False):
        # if do_random_stock:
        #     for key in self.stocks:
        #         if self.max_values.get(key):
        #             self.stocks[key] = self.max_values[key] * random.randint(1, 3)
        #         else:
        #             self.stocks[key] = 0
        #         print(f"{key}  :  {self.stocks[key]}")
        # else:
        self.stocks = copy.copy(stockTmp)

        self.current_stocks = copy.copy(self.stocks)

        self.state = self.get_state(self.stocks)
        self.current_delay = 0
        self.current_proccesses = []

    def train(self, epochs):
        stockTmp = copy.copy(self.stocks)

        for i in range (1, epochs):
            # if random.uniform(0, 1) < 0.5:
            #     self.__reinitialize(stockTmp, False)
            # else:
            self.__reinitialize(stockTmp, True)
            self.__run_env(False)
            print(f"Episode: {i}, delay: {self.current_delay}, epsilone: {self.epsilon}, {self.optimized_stock_name}: {[value for key, value in self.stocks.items() if key in self.optimized_stock_name]}")
            # for key, value in actions.items():
            #     for key2, value2 in actions_tmp.items():
            #         if key == key2:
            #             print(f'Action: {key}: {value - value2}')
            # for key, value in self.stocks.items():
            #     print(f'stock: {key}: {value}')

            if self.epsilon > 0.2 and i % (epochs / 10) == 0:
                self.epsilon -= 0.025
        
        self.__reinitialize(stockTmp, False)

    def run(self):
        self.not_training = True
        self.delay = 1000000
        self.epsilon = 0
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
