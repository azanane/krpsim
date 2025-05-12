from argparse import ArgumentParser
from srcs.Process import Process
from srcs.Krpsim import Krpsim

class Parser:

    def __init__(self, verbose=True):
        self.index = 0
        self.new_index = 0
        self.name_tmp = 0

        self.time_is_opti = False
        self.optimized_stock = ""
        self.krpsim = Krpsim()

        if verbose == True:
            self.get_file_path()
        
    def get_file_path(self):
        parser = ArgumentParser()
        parser.add_argument("-f", "--file", dest="data_file", help="Open ressources/filename file")
        parser.add_argument("-d", "--delay", dest="delay", help="Delay")
        parser.add_argument("-e", "--epochs", dest="epochs", help="number of training epochs")

        args = parser.parse_args()
        file_path = args.data_file
        delay = args.delay
        epochs = args.epochs
        if (file_path is None or delay is None):
            print("Correct format: python3 QLearning.py -f {file_path} -d {delay}")
            exit(1)
        print(f'Config File : {file_path}\n')
        self.krpsim.delay = int(delay)
        if epochs is None:
            self.krpsim.epochs = 100
        else:
            self.krpsim.epochs = int(epochs)
        self.parse_file(file_path)
        self.initialize_stock()

    def parse_file(self, file_path):
        rien_faire = Process()
        rien_faire.name = "rien_faire"
        self.krpsim.processes.append(rien_faire)
        with open(file_path) as input_file:
            for line in input_file:
                line = line.strip()
                self.name_tmp = ""
                self.index = 0
                self.new_index = 0

                self.read_next_name(line)
                if len(line) == 0 or line[self.index] == '#' or self.name_tmp == "":
                    continue
                if self.new_index >= len(line):
                    raise ValueError(f"Error for the line: {line}")
                self.verify_next_char(line, ':', only_one=True)
                if line[self.new_index] == ":":
                    raise ValueError(f"No needs were given for the line: {line}")
                if self.name_tmp == "optimize":
                    self.read_optimized_stock(line)
                elif line[self.new_index] != '(':
                    self.read_stock(line)
                elif line[self.new_index] == '(':
                    self.read_process(line)
                else:
                    raise ValueError(f"Error for the line: {line}")

    def read_stock(self, line):
        quantity_tmp = 0
        quantity_tmp = self.read_next_quantity(line, quantity_tmp)
        self.is_end_of_line_valid(line)
        self.krpsim.add_or_update_stock(self.name_tmp, quantity_tmp)

    def read_process(self, line):
        process_tmp = Process()
        quantity_tmp = 0

        process_tmp.name = self.name_tmp

        self.verify_next_char(line, '(')
        process_tmp = self.add_stock_from_process(line, process_tmp, True)
        if not process_tmp.needs:
            raise ValueError(f"No needs were given for the process: {process_tmp.name}")

        self.verify_next_char(line, ')')
        self.verify_next_char(line, ':')

        try:
            self.verify_next_char(line, '(')
            process_tmp = self.add_stock_from_process(line, process_tmp, False)
            if not process_tmp.results:
                raise ValueError(f"No results were given for the process: {process_tmp.name}")

            self.verify_next_char(line, ')')
            self.verify_next_char(line, ':')

        except Exception as e:
            if not line[self.new_index].isdigit():
                raise ValueError(f"Error occurred in line: {line}. Char '{line[self.new_index]}' was given at index {self.new_index} instead of a delay")

        quantity_tmp = self.read_next_quantity(line, quantity_tmp)
        process_tmp.delay = quantity_tmp
        self.is_end_of_line_valid(line)

        self.krpsim.add_process(process_tmp)

    def read_optimized_stock(self, line):
        self.name_tmp = ""
        self.verify_next_char(line, '(')

        while self.new_index < len(line) - 1 and line[self.new_index - 1] != ')':
            self.read_next_name(line)
            if self.name_tmp == "time" and not self.krpsim.is_time_opti:
                self.krpsim.is_time_opti = True
            else:
                self.krpsim.add_optimized_stocks(self.name_tmp)
            if line[self.new_index] == ')':
                break
            self.verify_next_char(line, ';')

        
        self.verify_next_char(line, ')')
        self.new_index -= 1
        self.is_end_of_line_valid(line)

    def read_next_quantity(self, line, quantity):
        self.index = self.new_index
        self.while_is_digit(line)
        substring = ''.join([line[i] for i in range(self.index, self.new_index)])
        quantity = int(substring)
        if quantity < 0:
            raise ValueError(f"Error occurred in line: {line}. Quantity: {quantity} cannot be negative.")
        return quantity

    def add_stock_from_process(self, line, process_tmp, is_need):
        self.name_tmp = ""
        quantity_tmp = 0

        while self.new_index < len(line) - 1 and line[self.new_index] != ')':
            self.read_next_name(line)
            self.verify_next_char(line, ':')
            quantity_tmp = self.read_next_quantity(line, quantity_tmp)
            self.pass_char(line, ' ')
            if line[self.new_index] != ')':
                self.verify_next_char(line, ';')
            if is_need:
                process_tmp.add_need(self.name_tmp, quantity_tmp)
            else:
                process_tmp.add_result(self.name_tmp, quantity_tmp)

        self.index = self.new_index
        return process_tmp

    def pass_char(self, line, c, only_one = False):
        while self.new_index < len(line) and line[self.new_index] == c:
            self.new_index += 1
            if only_one:
                break
        self.index = self.new_index

    def verify_next_char(self, line, c, only_one = False):
        self.pass_char(line, ' ')
        if line[self.new_index] != c:
            raise ValueError(f"Error occurred in line: {line}. Char '{line[self.new_index]}' was given at index {self.new_index} instead of char '{c}'")
        else:
            self.pass_char(line, c, only_one)
        self.pass_char(line, ' ')

    def read_next_name(self, line):
        self.index = self.new_index
        self.go_after_next_colon(line)
        self.name_tmp = ''.join([line[i] for i in range(self.index, self.new_index)])
        self.name_tmp = self.name_tmp.lower()

    def while_is_digit(self, line):
        if line[self.new_index] == '-':
            self.new_index += 1
        while self.new_index < len(line) and line[self.new_index].isdigit():
            self.new_index += 1

    def go_after_next_colon(self, line):
        while self.new_index < len(line) - 1 and line[self.new_index] not in [':', '#', ';', ' ']:
            self.new_index += 1

    def is_end_of_line_valid(self, line):
        self.index = self.new_index
        while self.new_index < len(line) and line[self.new_index] != ' ':
            self.new_index += 1
        if self.new_index < len(line) and not (self.new_index == len(line) - 1 or line[self.new_index] == '#'):
            raise ValueError(f"Wrong end of process or optimized line: {line}")

    def initialize_stock(self):
        stocks = self.krpsim.stocks
        for process in self.krpsim.processes:
            for key in process.needs:
                if key not in stocks:
                    self.krpsim.add_or_update_stock(key, 0)

            for key in process.results:
                if key not in stocks:
                    quantity = 0
                else:
                    quantity = stocks[key]

                self.krpsim.add_or_update_stock(key, quantity)