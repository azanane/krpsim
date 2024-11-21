#include "DynamicProgramming.hpp"

DynamicProgramming::DynamicProgramming(const Krpsim& krpsim) : _stocks(krpsim.getStocks()), _processes(krpsim.getProcesses()),
    _optimizedStocks(krpsim.getOptimizedStocks()), _isTimeOpti(krpsim.getIsTimeOpti()) {}

DynamicProgramming::~DynamicProgramming() {}

Process DynamicProgramming::_chooseOptiFinalProcess() const {

    const Stock optiStock = this->_stocks.find(this->_optimizedStocks.begin());
    const std::vector<Process> finalProcesses = optiStock.getAssociateProcesses();

    Process whichFinalProcess = NULL;

    for (const Process& finalProcess : finalProcesses) {

        const std::vector<Stock> primaryNeeds = this->_getPrimaryNeeds(finalProcess.getNeeds()); 
        
    
    }

    return whichFinalProcess;
}

std::vector<Stock> DynamicProgramming::_getPrimaryNeeds(const std::vector<Stock>& needs) const {

    std::vector<Stock>          primaryNeeds;
    std::list<std::string>      visited;
    // Pair between a path and its cost
    std::pair<std::vector<Process>, float>  path;

    for (const Stock& need : needs) {

        std::vector<Process> associateProcesses = need.getAssociateProcesses();

        for (const Process& associateProcess : associateProcesses) {

            visited.push_back(associateProcess);
        }
    }
}
