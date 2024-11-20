#include "Krpsim.hpp"

Krpsim::Krpsim() {
    this->maxDelay = 0;
    this->currentDelay = 0;
    this->isTimeOpti = false;
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

// Delays
void Krpsim::setMaxDelay(unsigned long maxDelay) {
    this->maxDelay = maxDelay;
}

void Krpsim::setCurrentDelay(unsigned long currentDelay) {
    this->currentDelay = currentDelay;
}

void Krpsim::addOrUpdateStock(Stock stock) {
    std::map<std::string, Stock>::iterator it = this->stocks.find(stock.getName());
    if (it != this->stocks.end()){
        updateStock(stock, it);
    } else {
        addStock(stock);
    }
}

void Krpsim::addStock(Stock stock) {
    this->stocks.insert(std::make_pair(stock.getName(), stock));
}

void Krpsim::updateStock(Stock stock, std::map<std::string, Stock>::iterator &it) {
    it->second.setQuantity(stock.getQuantity());
    it->second.addProcesses(stock.getAssociateProcesses());
}

void Krpsim::addProcess(Process process){
    this->processes.push_back(process);
}

void Krpsim::addInUsedProcess(Process process) {
    this->inUsedProcess.push_back(process);
}

// Optimization
void Krpsim::setIsTimeOpti(bool isTimeOpti) {
    this->isTimeOpti = isTimeOpti;
}

void Krpsim::addOptimizedStocks(std::string optimizedStock){
    this->optimizedStocks.insert(optimizedStock);
}
