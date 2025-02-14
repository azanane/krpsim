class Krpsim:
    def __init__(self, stocks = {}, processes = [], optimized_stocks = [], is_time_opti = False):
        self.processes = processes
        self.stocks = stocks
        self.optimized_stocks = optimized_stocks
        self.is_time_opti = is_time_opti

    # SETTERS
    def add_or_update_stock(self, stock_name, stock_quantity):
        self.stocks[stock_name] = stock_quantity

    def add_process(self, process):
        self.processes.append(process)

    def add_optimized_stocks(self, optimized_stock):
        self.optimized_stocks.append(optimized_stock)

    def set_is_time_opti(self, is_time_opti):
        self.is_time_opti = is_time_opti


    # GETTERS
    def get_stocks(self):
        return self.stocks

    def get_processes(self):
        return self.processes
    
    def get_optimized_stocks(self):
        return self.optimized_stocks
    
    def get_is_time_opti(self):
        return self.is_time_opti