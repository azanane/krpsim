class Krpsim:
    def __init__(self, stocks = {}, processes = [], optimized_stocks = [], is_time_opti = False, delay = 1000, epochs = 100):
        self.processes = processes
        self.stocks = stocks
        self.optimized_stocks = optimized_stocks
        self.is_time_opti = is_time_opti
        self.delay = delay
        self.epochs = epochs

    # SETTERS
    def add_or_update_stock(self, stock_name, stock_quantity):
        self.stocks[stock_name] = stock_quantity

    def add_process(self, process):
        self.processes.append(process)

    def add_optimized_stocks(self, optimized_stock):
        self.optimized_stocks.append(optimized_stock)
