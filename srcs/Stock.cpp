#include "Stock.hpp"

Stock::Stock(std::string name, long quantity) : name(name), quantity(quantity){
}

Stock::~Stock(){}


std::string Stock::getName() const {
    return name;
}
long Stock::getQuantity() const {
    return quantity;
}
std::vector<std::string> Stock::getAssociateProcesses() const {
    return associateProcesses;
}

void Stock::addProcess(std::string processName) {
    associateProcesses.push_back(processName);
}

void Stock::addProcesses(std::vector<std::string> processesName) {
    for (std::string processName : processesName) {
        addProcess(processName);
    }
}