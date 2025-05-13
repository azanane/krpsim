import copy
import random
import numpy as np
import heapq

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

        self.current_processes = []  # This will be our priority queue (min-heap)
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

        self.solution = ()
        self.new_solution_processes = {}
        self.solution_stock = {}

        self.not_training = False

    def get_processes_with_smallest_delay(self):
        """Retrieve all processes with the smallest delay."""
        if not self.current_processes:
            return []

        # Get the smallest delay
        smallest_delay = self.current_processes[0].delay
        processes_with_smallest_delay = []

        # Pop all processes with the smallest delay
        while self.current_processes and self.current_processes[0].delay == smallest_delay:
            process = heapq.heappop(self.current_processes)
            processes_with_smallest_delay.append(process)

        self.current_delay = smallest_delay

        # Return the list of processes with the smallest delay
        return processes_with_smallest_delay

    def update_stock_and_time(self):
        smallest_process = self.get_processes_with_smallest_delay()
        for process in smallest_process:
            for key, value in process.results.items():
                self.stocks[key] += value

    def get_state(self, stocks):

        state = []
        
        for key, value in stocks.items():
            if len(stocks) > 10:
                min_need = self.max_values.get(key, 0) # default 0
            
                # Categorize dynamically based on min_need
                if value == 0 or min_need == 0:
                    category = 0  # No stock
                elif value <= min_need:
                    category = 1  # Bare minimum available
                elif value <= min_need * 2:
                    category = 2  # Sufficient stock
                elif value <= min_need * 5:
                    category = 3  # Well-stocked
                else:
                    category = 4  # Excess stock
                state.append(category)
            else:
                state.append(value)

        return tuple(state)

    def is_doable(self, stocks, process_index):

        for item, required_quantity in self.processes[process_index].needs.items():
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
        
        if self.current_processes != []:
            return True
        
        return False

    def get_reward(self, process_index, is_doable):

        if is_doable == False:
            return -100
        elif self.processes[process_index].needs and not self.processes[process_index].results:
            return -100

        processTmp = self.processes[process_index]

        reward = -1

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
        reward = self.get_reward(process_index, is_doable)

        # Remove from the stock the needs, and upgrade directly by removing and adding de current_stock
        if is_doable and process_index != 0:
            for key, value in process.needs.items():
                self.stocks[key] -= value
                self.current_stocks[key] -= value
            process.delay += self.current_delay
            heapq.heappush(self.current_processes, process)
            for key, value in process.results.items():
                self.current_stocks[key] += value

        next_state = self.get_state(self.current_stocks)

        # If we can only do nothing and there is no current process it is then end
        if next_state == (0,) and len(self.current_processes) == 0:
            reward -= 100
        return next_state, reward

    def update_q_table(self, process_index, new_processes, index_solution_processes):
        next_state, reward = self.run_process(process_index)

        if process_index == 0:
            self.update_stock_and_time()

            self.new_solution_processes[index_solution_processes] = copy.copy(new_processes)
            index_solution_processes += 1
            new_processes.clear()

        
        old_value = self.q_table[self.state][process_index]
        if type(self.q_table.get(next_state)) != np.ndarray:
            next_max = 0
        else:
            next_max = self.q_table[next_state][np.argmax(self.q_table[next_state])]

        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[self.state][process_index] = new_value

        self.state = self.get_state(self.stocks)

        return index_solution_processes

    def __run_env(self):

        self.new_solution_processes = {}
        new_processes = []
        index_solution_processes = 0

        while (self.is_anything_doable() and self.current_delay < self.delay):

            if type(self.q_table.get(self.state)) != np.ndarray:
                self.q_table[self.state] = np.zeros(len(self.processes))

            if random.uniform(0, 1) < self.epsilon:
                process_index = random.randint(0, len(self.processes) - 1) # Explore process space
            else:
                process_index = np.argmax(self.q_table[self.state]) # Exploit learned values

            if self.processes[process_index].is_feasible(self.stocks) and process_index != 0:
                new_processes.append(process_index)
                # We sort our list of new processes in order to don´t re-use it in the list of solution
                new_processes.sort()

            index_solution_processes = self.update_q_table(process_index, new_processes, index_solution_processes)

        while self.current_processes:
            self.update_stock_and_time()
        
        if self.stocks[self.optimized_stock_name[0]] > 0:
            fitness = self.current_delay / self.stocks[self.optimized_stock_name[0]]
        else:
            fitness = -1

        if fitness >= 0 and (not self.solution or self.solution[0] > fitness):
            self.solution = (fitness, self.new_solution_processes)
            self.solution_stock = self.stocks


    def __reinitialize(self, stockTmp):
        
        self.stocks = copy.copy(stockTmp)

        self.current_stocks = copy.copy(self.stocks)

        self.state = self.get_state(self.stocks)
        self.current_delay = 0
        self.current_processes = []

    def train(self, epochs):
        
        stockTmp = copy.copy(self.stocks)

        table = []

        for i in range (1, epochs):

            self.__reinitialize(stockTmp)
            self.__run_env()

            if self.stocks[self.optimized_stock_name[0]] > 0:
                fitness = self.current_delay / self.stocks[self.optimized_stock_name[0]]
            else:
                fitness = -1
 
            table.append(fitness)

            if self.epsilon > 0.2 and i % (epochs / 10) == 0:
                self.epsilon -= 0.025
        
        self.__reinitialize(stockTmp)

    def __print_stocks_results(self):

        print("Stocks :")
        for name in self.solution_stock:

            print(f'{name} : {self.solution_stock[name]}')

    def __run_solution(self):

        solution_runnable = self.solution[1]
        current_delay = 0
      
        delays = []
        delay_index = 0

        
        for index in solution_runnable:

            if solution_runnable[index]:

                if delays:
                    current_delay += delays[delay_index]

                if delay_index < len(delays) - 1:

                    past_delay = delays[delay_index]
                    # remove all delays of finished processes
                    delays = delays[delay_index + 1:]

                    for i_delay in range(len(delays)):
                        delays[i_delay] -= past_delay
                else:
                    delays = []

                delay_index = 0
            else:
                if delay_index < len(delays) - 1:
                    delay_index += 1

            for process_index in solution_runnable[index]:
                
                if process_index:

                    if not delays or self.processes[process_index].delay not in delays:
                        delays.append(self.processes[process_index].delay)
                        delays.sort()
                    
                    print(f'{current_delay}: {self.processes[process_index].name}')

        current_delay = current_delay + delays[len(delays) - 1]
        print(f'no more process doable at time : {current_delay}')

        self.__print_stocks_results()


    def run(self):

        self.not_training = True
        self.epsilon = 0.1

        if self.solution:
            self.__run_solution()
        else:
            print("Solution not found, please re-launch the search with more epochs or a with a bigger delay")
