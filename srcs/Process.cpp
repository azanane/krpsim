#include "Process.hpp"

Process::Process() {
    this->currentDelay = 0;
}

Process::~Process() {}

std::string Process::getName() const {
    return name;
}

std::vector<Stock> Process::getNeeds() const {
    return needs;
}

std::vector<Stock> Process::getResults() const {
    return results;
}

unsigned long Process::getDelay() const {
    return delay;
}

unsigned long Process::getCurrentDelay() const {
    return currentDelay;
}

void Process::setName(std::string name) {
    this->name = name;
}

void Process::setDelay(unsigned long delay) {
    this->delay = delay;
}

void Process::addNeed(Stock stock) {
    this->needs.push_back(stock);
}

void Process::addResult(Stock stock) {
    this->results.push_back(stock);
}

void Process::setCurrentDelay(unsigned long delay) {
    this->currentDelay += delay;
}