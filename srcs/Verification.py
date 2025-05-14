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

        self.current_processes = {}
        self.current_delay = 0
        self.file_path = ""

        self.get_file_path()

        print("Valid")

    def check_end_stocks(self, stock_name, quantity):

        if self.stocks[stock_name] != quantity:
            raise ValueError(f"Error in end Stocks : the result for {stock_name} should be {self.stocks.get(stock_name, 0)}, but you find {quantity}")

    def check_end_delay(self, end_time):

        end_delay = int(end_time)
        last_delay_add = 0
        for index_processes in self.current_processes:

            self.execute_list(self.current_processes[index_processes])
            last_delay_add = index_processes

        self.current_delay += last_delay_add
        if self.current_delay != end_delay:
            raise ValueError(f'Error in end delay, the result should be {self.current_delay}, but we got {end_delay}')
        
    def check_processes(self, line):

        if not line[:len(self.name_tmp)].isnumeric():
            raise ValueError(f'Error ine line : "{line}" , file corrupted')
        new_delay = int(line[:len(self.name_tmp)])

        finish_delay = new_delay - self.current_delay
        if finish_delay > 0:

            for index_processes in self.current_processes.copy():
                if index_processes <= finish_delay:
                    self.execute_list(self.current_processes[index_processes])
                else:
                    if self.current_processes.get(index_processes - finish_delay):
                        self.current_processes[index_processes - finish_delay].append(self.current_processes[index_processes])
                    else:
                        self.current_processes[index_processes - finish_delay] = self.current_processes[index_processes]
                                
                del self.current_processes[index_processes]

            self.current_delay = new_delay

        new_process = line[len(self.name_tmp) + 1:]
        process_index = self.get_process_index(new_process)
        if process_index == -1:
            raise ValueError(f"Config file {self.file_path} corrupted")
        if not self.is_doable(process_index):
            raise ValueError(f"Cannot do the process {line}")
                   
        if self.current_processes.get(self.processes[process_index].delay):
            self.current_processes[self.processes[process_index].delay].append(new_process)
        else:
            list_processes = []
            list_processes.append(new_process)
            self.current_processes[self.processes[process_index].delay] =  list_processes


        # sort self.current_processes
        myKeys = list(self.current_processes.keys())
        myKeys.sort()

        # Sorted Dictionary
        sorted_dict = {i: self.current_processes[i] for i in myKeys}
        self.current_processes = sorted_dict

        self.run_process(process_index)

        

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
        self.file_path = args.data_file

        if (self.file_path is None):
            print("Correct format: python3 QLearning.py -f {self.file_path}")
            exit(1)

        self.iterate_file()

    def iterate_file(self):

        is_running = False
        is_end_stocks = False

        config_file_bool = True
        end_delay_bool = True
        stocks_bool = True

        with open(self.file_path) as input_file:

            for line in input_file:
                line = re.sub(r"\s+", "", line, flags=re.UNICODE)
                self.name_tmp = ""
                self.index = 0
                self.new_index = 0

                self.read_next_name(line)
                if len(line) == 0:
                    continue

                if self.name_tmp == "configfile" and config_file_bool:

                    self.init_krpsim_class(line[len(self.name_tmp) + 1:])
                    is_running = True
                    config_file_bool = False
                elif self.name_tmp == "nomoreprocessdoableattime" and end_delay_bool:

                    self.check_end_delay(line[len(self.name_tmp) + 1:])
                    is_running = False
                    end_delay_bool = False
                elif self.name_tmp == "stocks" and stocks_bool:

                    is_end_stocks = True
                    stocks_bool = False
                elif is_running:

                    self.check_processes(line)
                elif is_end_stocks and line[len(self.name_tmp) + 1:].isnumeric() and self.stocks.get(line[:len(self.name_tmp)]):

                    stock_name = line[:len(self.name_tmp)]
                    quantity = int(line[len(self.name_tmp) + 1:])

                    self.check_end_stocks(stock_name, quantity)
                else:
                    raise ValueError(f"Config file {self.file_path} corrupted")
