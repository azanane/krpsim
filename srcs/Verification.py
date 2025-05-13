from argparse import ArgumentParser
from srcs.Parsing import Parser
import re
import copy

class Verification:

    def __init__(self):

        self.krpsim = None
        self.stocks = {}
        self.processes = {}

        self.index = 0
        self.new_index = 0
        self.name_tmp = 0

        self.get_file_path()

        print("Valid")

    def check_end_stocks(self, stock_name, quantity):

        if self.stocks[stock_name] != quantity:
            raise ValueError(f"Error in end Stocks : the result for {stock_name} should be {self.stocks.get(stock_name, 0)}, but you find {quantity}")



    def is_doable(self, process_index):

        for item, required_quantity in self.processes[process_index].needs.items():
            # If the required quantity of any item is greater than the stock, the process cannot be done
            if self.stocks.get(item, 0) < required_quantity:
                return False
        
        return True

    def run_process(self, process_index):

        for item, need_quantity in self.processes[process_index].needs.items():

            self.stocks[item] -= need_quantity

    def execute_list(self, list_processes):

        for name in list_processes:
            process_index = self.get_process_index(name)

            for item, result_quantity in self.processes[process_index].results.items():

                self.stocks[item] += result_quantity

    def get_process_index(self, process_name):

        index = 0
        for process in self.processes:

            if process_name == process.name:
                return index
            index += 1

        return -1

    def init_krpsim_class(self, config_file):

        parser_class = Parser(False)

        parser_class.parse_file(config_file)
        parser_class.initialize_stock()
        self.krpsim = copy.copy(parser_class.krpsim)
        self.stocks = self.krpsim.stocks
        self.processes = self.krpsim.processes

    def go_after_next_colon(self, line):
        while self.new_index < len(line) - 1 and line[self.new_index] not in [':']:
            self.new_index += 1

    def read_next_name(self, line):
        self.index = self.new_index
        self.go_after_next_colon(line)
        self.name_tmp = ''.join([line[i] for i in range(self.index, self.new_index)])
        self.name_tmp = self.name_tmp.lower()

    def get_file_path(self):

        parser = ArgumentParser()
        parser.add_argument("-f", "--file", dest="data_file", help="Open ressources/filename file")

        args = parser.parse_args()
        file_path = args.data_file

        if (file_path is None):
            print("Correct format: python3 QLearning.py -f {file_path}")
            exit(1)

        self.iterate_file(file_path)

    def iterate_file(self, file_path):

        is_running = False
        is_end_stocks = False
        current_processes = {}
        current_delay = 0
        end_delay = 0

        with open(file_path) as input_file:

            for line in input_file:
                line = re.sub(r"\s+", "", line, flags=re.UNICODE)
                self.name_tmp = ""
                self.index = 0
                self.new_index = 0

                self.read_next_name(line)
                if len(line) == 0:
                    continue

                if self.name_tmp == "configfile":
                    self.init_krpsim_class(line[len(self.name_tmp) + 1:])
                    is_running = True
                elif self.name_tmp == "nomoreprocessdoableattime":
                    end_delay = int(line[len(self.name_tmp) + 1:])
                    last_delay_add = 0
                    for index_processes in current_processes:
                        self.execute_list(current_processes[index_processes])
                        last_delay_add = index_processes

                    current_delay += last_delay_add
                    if current_delay != end_delay:
                        raise ValueError(f'Error in end delay, the result should be {current_delay}, but we got {end_delay}')
                    is_running = False
                elif self.name_tmp == "stocks":
                    is_end_stocks = True
                elif is_running:

                    if not line[:len(self.name_tmp)].isnumeric():
                        raise ValueError(f'Error ine line : "{line}" , file corrupted')
                    new_delay = int(line[:len(self.name_tmp)])

                    finish_delay = new_delay - current_delay
                    if finish_delay > 0:
                       
                        for index_processes in current_processes.copy():
                            if index_processes <= finish_delay:
                                self.execute_list(current_processes[index_processes])
                            else:
                                if current_processes.get(index_processes - finish_delay):
                                    current_processes[index_processes - finish_delay].append(current_processes[index_processes])
                                else: 
                                    current_processes[index_processes - finish_delay] = current_processes[index_processes]
                                
                            del current_processes[index_processes]

                        current_delay = new_delay

                    new_process = line[len(self.name_tmp) + 1:]
                    process_index = self.get_process_index(new_process)
                    if process_index == -1:
                        raise ValueError(f"Config file {file_path} corrupted")
                    if not self.is_doable(process_index):
                        raise ValueError(f"Cannot do the process {line}")
                   
                    list_processes = []
                    if current_processes.get(self.processes[process_index].delay):
                        list_processes = current_processes[self.processes[process_index].delay]
                        list_processes.append(new_process)
                    else:
                        list_processes.append(new_process)

                    current_processes[self.processes[process_index].delay] =  list_processes

                    # sort current_processes
                    myKeys = list(current_processes.keys())
                    myKeys.sort()

                    # Sorted Dictionary
                    sorted_dict = {i: current_processes[i] for i in myKeys}
                    current_processes = sorted_dict

                    self.run_process(process_index)
                elif is_end_stocks:

                    stock_name = line[:len(self.name_tmp)]
                    quantity = int(line[len(self.name_tmp) + 1:])
                    self.check_end_stocks(stock_name, quantity)
                else:
                    raise ValueError(f"Config file {file_path} corrupted")
