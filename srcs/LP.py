import copy

class KrpsimLP():


    def __init__(self, stocks, processes, optimized_stock=["euro"], delay = 1000):
        self.stocks = stocks
        self.current_stocks = copy.copy(stocks)
        self.processes = processes

        self.optimized_stock_name = optimized_stock

        # Store optimized processes beforehand to reduce looping
        self.optimized_processes = [
            process for process in processes if any(stock in process.benef for stock in optimized_stock)
        ]

        self.lp_table = self.get_lp_table()

        self.current_processes = []  # This will be our priority queue (min-heap)

        self.current_delay = 0
        self.delay = delay

    def get_lp_table(self):

        lp_table = {}

        for process in self.processes:

            for stock in self.stocks:

                if process.benef and process.benef.get(stock):

                    lp_table[(process.name, stock)] = process.benef[stock]

        return lp_table

                    

    def lp(self):

        solutionFound = False

        optimisationProcessesHistory = []
        optimisationProcessesHistory.append(self.choose_optimisation(self.optimized_processes, self.optimized_stock[0]))

        # while solutionFound:

        #     if 

    def choose_optimisation(self, processes, stockToGet):

        processToChoose = processes[0]
        ratioProcessTmp = processes[0].benef[stockToGet] / processes[0].delay

        for process in processes:

            newRatio = process.benef[stockToGet] / process.delay

            if newRatio > ratioProcessTmp:

                processToChoose = process
                processToChoose = newRatio

        return processToChoose