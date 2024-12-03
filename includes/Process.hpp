
#ifndef PROCESSES_HPP
#define PROCESSES_HPP

#include <vector>
#include <string>
#include <unordered_set>
#include "Stock.hpp"

struct HashStock;

class Process {
    private:
        std::string                             name;
        std::unordered_set<Stock, HashStock>    needs;
        std::unordered_set<Stock, HashStock>    results;
        std::unordered_set<Stock, HashStock>    profits;

        unsigned long delay;
        unsigned long currentDelay;

    public:
    Process();
    ~Process();

    std::string getName() const;
    std::unordered_set<Stock, HashStock> getNeeds() const;
    std::unordered_set<Stock, HashStock> getResults() const;
    std::unordered_set<Stock, HashStock> getProfits() const;
    unsigned long getDelay() const;
    unsigned long getCurrentDelay() const;

    void setName(std::string name);
    void setCurrentDelay(unsigned long delay);
    void setDelay(unsigned long delay);
    void addNeed(Stock stock);
    void addResult(Stock stock);
    void addProfit(Stock stock);
};

#endif