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
