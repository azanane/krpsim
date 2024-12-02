#include "Stock.hpp"

Stock::Stock(){}

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

void Stock::setName(std::string name) {
    this->name = name;
}

void Stock::setQuantity(long quantity) {
    this->quantity = quantity;
}

void Stock::addProcess(std::string processName) {
    associateProcesses.push_back(processName);
}

void Stock::addProcesses(std::vector<std::string> processesName) {
    for (std::string processName : processesName) {
        addProcess(processName);
    }
}

bool Stock::operator==(const Stock &stock) const{ 
    if (stock.getName() == this->getName()) {
        return true;
    } 
    return false;
} 

std::size_t HashStock::operator()(const Stock &stock) const {
    std::size_t h1 = std::hash<std::string>{}(stock.getName());
    return h1;
}