#include "DynamicProgramming.hpp"

DynamicProgramming::DynamicProgramming(const Krpsim& krpsim) : _stocks(krpsim.getStocks()), _processes(krpsim.getProcesses()), _isTimeOpti(krpsim.getIsTimeOpti()), _optimizedStocks(krpsim.getOptimizedStocks()) {

    if (!this->_optimizedStocks.empty()) {

        this->_setAllPaths();
    }
}

DynamicProgramming::~DynamicProgramming() {}

// std::priority_queue< std::pair<std::list<Process>, cost>, cmpCost > 

void DynamicProgramming::_setAllPaths() {

    for (std::set<std::string>::const_iterator itStockOpti = this->_optimizedStocks.begin(); itStockOpti != this->_optimizedStocks.end(); itStockOpti++) {

        std::map<std::string, Stock>::const_iterator stockFind = this->_stocks.find(*itStockOpti);
        std::map<std::string, long> processesMap = this->_stocks.find(*itStockOpti)->second.getAssociateProcessesProfits();

        // if the stock to optimize do exists and if it have associate processes
        if (stockFind != this->_stocks.end() && !processesMap.empty()) {

            // if (this->_allSolutionsStocks.find(*itStockOpti) != this->_allSolutionsStocks.end()) {}

            Stock stockToResolve = stockFind->second;

            for (std::map<std::string, long>::const_iterator itProcessesOpti = processesMap.begin(); itProcessesOpti != processesMap.end(); itProcessesOpti++) {

                std::map<std::string, Process>::const_iterator processFind = this->_processes.find(itProcessesOpti->first);
                if (processFind != this->_processes.end()) {

                    const Process& processParent = processFind->second;

                    stockToResolve.setQuantity(itProcessesOpti->second);
                    this->_getStockProcesses(stockToResolve, processParent, -1);
                }
            }
        }
    }
}

std::list<Process> DynamicProgramming::_getStockProcesses(const Stock& stockToResolve, const Process& processParent, long quantityNeeded) const {

    const std::unordered_set<Stock, HashStock>& needs = processParent.getNeeds();
    for (const Stock& need : needs) {

        std::map<std::string, long> processesNames = need.getAssociateProcessesProfits();

        // if we get more than 1 new process we can execute, we get a whole new path in our tree, so we duplicate the existants solutions
        if (processesNames.size() > 1) {
            
        }

        for (const std::pair<std::string, long>& processInfos : processesNames) {

            const std::map<std::string, Process>::const_iterator& processFind = this->_processes.find(processInfos.second);
            if (processFind != this->_processes.end()) {

                quantityNeeded = quantityNeeded - processInfos.second;
                if (quantityNeeded > 0) {
                    this->_getStockProcesses(stockToResolve, processFind->second, quantityNeeded);
                }
                else {
                    this->_getStockProcesses(stockToResolve, processFind->second, quantityNeeded);
                }
            }
        }
    }
}
