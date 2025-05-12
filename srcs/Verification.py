from argparse import ArgumentParser
from srcs.Parsing import Parser
import re
import copy

class Verification:

    def __init__(self):

        self.get_file_path()
        self.krpsim = None
        self.stocks = {}
        self.processes = {}

        self.index = 0
        self.new_index = 0
        self.name_tmp = 0

        self.get_file_path()

    def is_doable(self, proccess_index):

        for item, required_quantity in self.processes[proccess_index].needs.items():
            # If the required quantity of any item is greater than the stock, the process cannot be done
            if self.stocks.get(item, 0) < required_quantity:
                return False
        
        return True

    def execute_list(self, list_processes):

        for name in list_processes:
            process_index = self.get_process_index(name)
            


    def get_process_index(self, process_name):

        for index, process in self.processes:

            if process_name == process.name:
                return index

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
                    is_running = False
                elif self.name_tmp == "stock":
                    is_end_stocks = True
                elif is_running:
                   new_delay = int(line[:len(self.name_tmp)])

                   finish_delay = new_delay - current_delay
                   if finish_delay > 0:
                       
                       for index_processes in current_processes:
                           if index_processes < finish_delay:
                                self.execute_list(current_processes[index_processes])


                   new_process = line[len(self.name_tmp) + 1:]
                   process_index = self.get_process_index(new_process)
                   if process_index == -1:
                       raise ValueError(f"Config file {file_path} corrupted")
                   
                   if current_processes[self.processes[process_index].delay]:
                        list_processes = current_processes[self.processes[process_index].delay]
                        list_processes.append(new_process)
                   else:
                        current_processes[self.processes[process_index].delay] =  [new_process]
                # elif is_end_stocks:
                else:
                    raise ValueError(f"Config file {file_path} corrupted")

