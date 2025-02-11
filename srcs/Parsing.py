from argparse import ArgumentParser
from Process import Process
from Krpsim import Krpsim

class Parser:

    def __init__(self):
        self.time_is_opti = False
        self.optimized_stock = ""
        self.krpsim = Krpsim()

        self.get_file_path()
        
    def get_file_path(self):
        parser = ArgumentParser()
        parser.add_argument("-f", "--file", dest="data_file", help="Open ressources/filename file")

        args = parser.parse_args()
        file_path = args.data_file
        if (file_path is None):
            print("Correct format: python3 QLearning.py -f {file_path}")
            exit(1)
        self.parse_file(file_path)
        self.initialize_stock()

    def parse_file(self, input_file):

        for line in input_file:
            line = line.strip()
            name_tmp = ""
            index = 0
            new_index = 0

            self.read_next_name(line, name_tmp, index, new_index)
            if line[index] == '#' or name_tmp == "":
                continue
            if new_index >= len(line):
                raise ValueError(f"Error for the line: {line}")
            self.verify_next_char(line, ':', index, new_index)
            if name_tmp == "optimize":
                self.read_optimized_stock(line, index, new_index)
            elif line[new_index] != '(':
                self.read_stock(line, name_tmp, index, new_index)
            elif line[new_index] == '(':
                self.read_process(line, name_tmp, index, new_index)
            else:
                raise ValueError(f"Error for the line: {line}")

    def read_stock(self, line, name_tmp, index, new_index):
        quantity_tmp = 0
        self.read_next_quantity(line, quantity_tmp, index, new_index)
        self.is_end_of_line_valid(line, index, new_index)
        self.krpsim.add_or_update_stock(name_tmp, quantity_tmp)

    def read_process(self, line, name_tmp, index, new_index):
        process_tmp = Process()
        quantity_tmp = 0

        process_tmp.set_name(name_tmp)

        self.verify_next_char(line, '(', index, new_index)
        self.add_stock_from_process(line, process_tmp, index, new_index, True)
        if not process_tmp.get_needs():
            raise ValueError(f"No needs were given for the process: {process_tmp.get_name()}")

        self.verify_next_char(line, ')', index, new_index)
        self.verify_next_char(line, ':', index, new_index)

        try:
            self.verify_next_char(line, '(', index, new_index)
            self.add_stock_from_process(line, process_tmp, index, new_index, False)
            if not process_tmp.get_results():
                raise ValueError(f"No results were given for the process: {process_tmp.get_name()}")

            self.verify_next_char(line, ')', index, new_index)
            self.verify_next_char(line, ':', index, new_index)

        except Exception as e:
            if not line[new_index].isdigit():
                raise ValueError(f"Error occurred in line: {line}. Char '{line[new_index]}' was given at index {new_index} instead of a delay")

        self.read_next_quantity(line, quantity_tmp, index, new_index)
        process_tmp.set_delay(quantity_tmp)
        self.is_end_of_line_valid(line, index, new_index)

        self.krpsim.add_process(process_tmp)

    def read_optimized_stock(self, line, index, new_index):
        name_tmp = ""
        self.verify_next_char(line, '(', index, new_index)

        while new_index < len(line) - 1 and line[new_index - 1] != ')':
            self.read_next_name(line, name_tmp, index, new_index)
            if name_tmp == "time" and not self.krpsim.get_is_time_opti():
                self.krpsim.set_is_time_opti(True)
            else:
                self.krpsim.add_optimized_stocks(name_tmp)
            if line[new_index] == ')':
                break
            self.verify_next_char(line, ';', index, new_index)
        
        self.verify_next_char(line, ')', index, new_index)
        self.is_end_of_line_valid(line, index, new_index - 1)

    def read_next_quantity(self, line, quantity, index, new_index):
        index = new_index
        self.while_is_digit(line, new_index)
        quantity = int(line[index:new_index + 1 - index])
        if quantity < 0:
            raise ValueError(f"Error occurred in line: {line}. Quantity: {quantity} cannot be negative.")

    def add_stock_from_process(self, line, process_tmp, index, new_index, is_need):
        name_tmp = ""
        quantity_tmp = 0

        while new_index < len(line) - 1 and line[new_index] != ')':
            self.read_next_name(line, name_tmp, index, new_index)
            self.verify_next_char(line, ':', index, new_index)
            self.read_next_quantity(line, quantity_tmp, index, new_index)
            self.pass_char(line, ' ', index, new_index)
            if line[new_index] != ')':
                self.verify_next_char(line, ';', index, new_index)
            if is_need:
                process_tmp.add_need(name_tmp, quantity_tmp)
            else:
                process_tmp.add_result(name_tmp, quantity_tmp)

        index = new_index

    def pass_char(self, line, c, index, new_index):
        while line[new_index] == c:
            new_index += 1
        index = new_index

    def verify_next_char(self, line, c, index, new_index):
        self.pass_char(line, ' ', index, new_index)
        if line[new_index] != c:
            raise ValueError(f"Error occurred in line: {line}. Char '{line[new_index]}' was given at index {new_index} instead of char '{c}'")
        else:
            self.pass_char(line, c, index, new_index)
        self.pass_char(line, ' ', index, new_index)

    def read_next_name(self, line, name_tmp, index, new_index):
        index = new_index
        self.go_after_next_colon(line, new_index)
        name_tmp = line[index:new_index]
        name_tmp = name_tmp.lower()

    def while_is_digit(self, line, new_index):
        if line[new_index] == '-':
            new_index += 1
        while new_index < len(line) and line[new_index].isdigit():
            new_index += 1

    def go_after_next_colon(self, line, new_index):
        while new_index < len(line) and line[new_index] not in [':', '#', ';', ' ']:
            new_index += 1

    def is_end_of_line_valid(self, line, index, new_index):
        index = new_index
        while new_index < len(line) and line[new_index] != ' ':
            new_index += 1
        if not (new_index == len(line) - 1 or line[new_index] == '#'):
            raise ValueError(f"Wrong end of process or optimized line: {line}")

    def initialize_stock(self):
        stocks = self.krpsim.get_stocks()
        for process in self.krpsim.get_processes():
            for key in process.get_needs():
                if key not in stocks:
                    self.krpsim.add_stock(key, 0)

            for key in process.get_results():
                if key not in stocks:
                    quantity = 0
                else:
                    quantity = stocks[key]

                self.krpsim.add_or_update_stock(key, quantity)


parser = Parser()