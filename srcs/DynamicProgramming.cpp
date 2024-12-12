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

                    // const Process& processParent = processFind->second;
                    std::unordered_set<Stock, HashStock> needs = processFind->second.getNeeds();
                    for (Stock need : needs) {

                        // Want to change the way to get associate processes (need to find a way to include adsociateProcessProfits in needs)
                        std::map<std::string, Stock>::const_iterator getAssociateProcesses = this->_stocks.find(need.getName());
                        if (getAssociateProcesses != this->_stocks.end()) {

                            need.addProcessesProfits(getAssociateProcesses->second.getAssociateProcessesProfits());
                            this->_getStockProcesses(need);
                        }
                    }
                }
            }
        }
    }
}

std::list<std::list<std::string>> DynamicProgramming::_getStockProcesses(const Stock& stockToResolve) {

    std::map<std::pair<std::string,long>, std::list<std::list<std::string>>>::const_iterator solutionAlreadyExist = this->_allSolutionsStocks.find({stockToResolve.getName(), stockToResolve.getQuantity()});
    if (solutionAlreadyExist != this->_allSolutionsStocks.end()) {

        return solutionAlreadyExist->second;
    }

    std::map<std::string, long> processesProfits = stockToResolve.getAssociateProcessesProfits();
    std::list<std::list<std::string>> allStockSolutions;

    for (std::map<std::string, long>::const_iterator processProfits = processesProfits.begin(); processProfits != processesProfits.end(); processProfits++) {

        // find the process that give us a profit for the needed stock
        std::map<std::string, Process>::const_iterator processFind = this->_processes.find(processProfits->first);
        if (processFind != this->_processes.end()) {

            long newQuantity = stockToResolve.getQuantity() - processProfits->second;

            if (newQuantity > 0) {

                Stock newStockToResolve(stockToResolve.getName(), newQuantity);
                newStockToResolve.addProcessesProfits(stockToResolve.getAssociateProcessesProfits());
                std::list<std::list<std::string>> newSolutions = this->_getStockProcesses(newStockToResolve);
                
                // create new branchs im my tree
                for (std::list<std::string> newSolution : newSolutions) {

                    newSolution.push_front(processProfits->first);
                    allStockSolutions.push_back(newSolution);
                }
            }
            else {

                std::list<std::string> newSolution;
                newSolution.push_back(processProfits->first);
                allStockSolutions.push_back(newSolution);
            }
        }
    }

    this->_allSolutionsStocks.insert({{stockToResolve.getName(), stockToResolve.getQuantity()}, allStockSolutions});

    return allStockSolutions;
}
