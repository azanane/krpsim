#include "Process.hpp"

Process::Process() {
    this->currentDelay = 0;
}

Process::~Process() {}

std::string Process::getName() const {
    return name;
}

std::unordered_set<Stock, HashStock> Process::getNeeds() const {
    return needs;
}

std::unordered_set<Stock, HashStock> Process::getResults() const {
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
    this->needs.insert(stock);
}

void Process::addResult(Stock stock) {
    this->results.insert(stock);
}

void Process::setCurrentDelay(unsigned long delay) {
    this->currentDelay += delay;
}
