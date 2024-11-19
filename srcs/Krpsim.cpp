#include "Krpsim.hpp"

Krpsim::Krpsim(std::string fileName, unsigned long delay) {
    (void)fileName;
    (void)isTimeOpti;

    maxDelay = delay;
    currentDelay = 0;
}

Krpsim::~Krpsim() {}

std::map<std::string, Stock> Krpsim::getStocks() const {
    return stocks;
}
std::vector<Process>  Krpsim::getProcesses() const {
    return processes;
}
std::vector<Process>  Krpsim::getInUsedProcess() const {
    return inUsedProcess;
}

// Optimization
bool Krpsim::getIsTimeOpti() const {
    return isTimeOpti;
}
std::set<std::string>  Krpsim::getOptimizedStocks() const {
    return optimizedStocks;
}

// Delays
unsigned long  Krpsim::getMaxDelay() const {
    return maxDelay;
}
unsigned long  Krpsim::getCurrentDelay() const {
    return currentDelay;
}

