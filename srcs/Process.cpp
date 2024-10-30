#include "Process.hpp"

Process::Process(std::vector<stockType> needs, std::vector<stockType> results, unsigned long delay): needs(needs), results(results), delay(delay) {
}

Process::~Process() {}

std::vector<std::pair<std::string, unsigned long>> Process::getNeeds() const {
    return needs;
}

std::vector<std::pair<std::string, unsigned long>> Process::getResults() const {
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