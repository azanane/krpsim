#include "Process.hpp"

Process::Process(std::vector<Stock> needs, std::vector<Stock> results, unsigned long delay): needs(needs), results(results), delay(delay) {
}

Process::~Process() {}

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

void Process::setCurrentDelay(unsigned long delay) {
    currentDelay += delay;
}