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
std::map<std::string, long> Stock::getAssociateProcessesProfits() const {
    return associateProcessesProfits;
}

void Stock::setName(std::string name) {
    this->name = name;
}

void Stock::setQuantity(long quantity) {
    this->quantity = quantity;
}

void Stock::addProcessProfits(std::pair<std::string, long> processName) {
    associateProcessesProfits.insert(processName);
}

void Stock::addProcessesProfits(std::map<std::string, long> processesName) {
    for (std::pair<std::string, long> processName : processesName) {
        addProcessProfits(processName);
    }
}

bool Stock::operator==(const Stock &stock) const {

    if (stock.getName() == this->getName() && stock.getQuantity() == this->getQuantity()) {
        return true;
    } 
    return false;
}

std::size_t HashStock::operator()(const Stock &stock) const {
    std::size_t h1 = std::hash<std::string>{}(stock.getName());
    return h1;
}