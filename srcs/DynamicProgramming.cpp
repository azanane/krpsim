#include "DynamicProgramming.hpp"

DynamicProgramming::DynamicProgramming(const Krpsim& krpsim) : _stocks(krpsim.getStocks()), _processes(krpsim.getProcesses()), _isTimeOpti(krpsim.getIsTimeOpti()), _optimizedStocks(krpsim.getOptimizedStocks()) {}

DynamicProgramming::~DynamicProgramming() {}

// std::priority_queue< std::pair<std::list<Process>, cost>, cmpCost > 

void DynamicProgramming::_setAllPaths(std::list<Process> path, std::map<Process, std::list<std::list<Process>>> memo, std::list<Stock> neededStocks) {

    for (Stock need : neededStocks) {

        if (memo.find(need)) {
            return memo.find(need)->second;
        }

        for (const std::string& needProcessName : need.getAssociateProcesses()) {

            if (needProcessName != "") {

                const Process& needProcess = this->_processes.find(needProcessName)->second;

                if (memo.find(need)) {
                    return memo.find(need)->second;
                }

                path.push_back(needProcess);
                need.setQuantity(need.getQuantity() - needProcess.getProfits(need.getName()));

                if (need.getQuantity > 0) {

                    
                    this->_setAllPaths(path, memo, neededStocks);
                }
            }
        }
    }

    this->_allPaths.insert(path);
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
