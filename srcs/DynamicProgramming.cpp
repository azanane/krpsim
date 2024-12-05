#include "DynamicProgramming.hpp"

DynamicProgramming::DynamicProgramming(const Krpsim& krpsim) : _stocks(krpsim.getStocks()), _processes(krpsim.getProcesses()), _isTimeOpti(krpsim.getIsTimeOpti()), _optimizedStocks(krpsim.getOptimizedStocks()) {


    if (!this->_optimizedStocks.empty() && this->_processes.find(*this->_optimizedStocks.begin()) != this->_processes.end()) {

        this->_setAllPaths();
    }
}

DynamicProgramming::~DynamicProgramming() {}

// std::priority_queue< std::pair<std::list<Process>, cost>, cmpCost > 

void DynamicProgramming::_setAllPaths() {

    for (std::set<std::string>::const_iterator itProcesses = this->_optimizedStocks.begin(); itProcesses != this->_optimizedStocks.end(); itProcesses++) {

        if (this->_processes.find(*itProcesses) != this->_processes.end()) {


            std::unordered_set<Stock, HashStock> stockSet = this->_processes.find(*itProcesses)->second.getNeeds();
             
            for (stockSetIterator itStock = stockSet.begin(); itStock != stockSet.end(); itStock++) {

                if (this->_allSolutionsStocks.find(*itStock) != this->_allSolutionsStocks.end()) {}


            }
        }
    }

    //     for (Stock need : neededStocks) {

    //         if (memo.find(need) != memo.end()) {
    //             // return memo.find(need)->second;
    //         }

    //         for (const std::string& needProcessName : need.getAssociateProcesses()) {

    //             if (this->_processes.find(needProcessName) != this->_processes.end()) {

    //                 const Process& needProcess = this->_processes.find(needProcessName)->second;

    //                 // if (memo.find(need)) {
    //                 //     return memo.find(need)->second;
    //             // }

    //             if (needProcess.getProfits().find(need) != needProcess.getProfits().end()) {

    //                 path.push_back(needProcess);
    //                 const stockSetIterator& profit = needProcess.getProfits().find(need);
    //                 need.setQuantity(need.getQuantity() - profit->getQuantity());

    //                 if (need.getQuantity() > 0) {

    //                     this->_setAllPaths(path, memo, neededStocks);
    //                 }
    //             }
    //         }
    //     }
    // }
    // }

    // this->_allPaths.push_back(path);
}

std::list<std::list<Process>> DynamicProgramming::_getStockProcesses(const Stock& stock) const {

    std::map<std::string, long> associateProcessesProfits = stock.getAssociateProcessesProfits();

    for (const std::pair<std::string, long> processProfit : associateProcessesProfits) {

        Stock stockTmp = stock;
        stockTmp.setQuantity(stockTmp.getQuantity() - processProfit.second);
        if (stockTmp.getQuantity() > 0) {

            this->_getStockProcesses(stockTmp);
        }
    }
}

// std::list<Process> DynamicProgramming::_chooseOptiPath() const {

//     const Stock optiStock = this->_stocks.find(this->_optimizedStocks.begin());
//     const std::vector<Process> finalProcesses = optiStock.getAssociateProcesses();

//     std::list<Process> optiPath = NULL;

//     for (const Process& finalProcess : finalProcesses) {

//         const std::vector<Stock> primaryNeeds = this->_getPrimaryNeeds(finalProcess.getNeeds()); 
//     }

//     return optiPath;
// }

// std::vector<Stock> DynamicProgramming::_getPrimaryNeeds(const std::vector<Stock>& needs) const {

//     std::vector<Stock>          primaryNeeds;
//     std::list<std::string>      visited;
//     // Pair between a path and its cost
//     std::pair<std::vector<Process>, float>  path;

//     for (const Stock& need : needs) {

//         std::vector<Process> associateProcesses = need.getAssociateProcesses();

//         for (const Process& associateProcess : associateProcesses) {

//             visited.push_back(associateProcess);
//         }
//     }
// }
