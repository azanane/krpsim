
#ifndef PROCESSES_HPP
#define PROCESSES_HPP

#include <map>
#include <vector>
#include <string>
#include "Stock.hpp"

class Process {
    private:
        std::string             name;
        std::vector<Stock>  needs;
        std::vector<Stock>  results;

        unsigned long delay;
        unsigned long currentDelay;

    public:

    Process(std::vector<Stock> needs, std::vector<Stock> results, unsigned long delay);
    ~Process();

    std::vector<Stock> getNeeds() const;
    std::vector<Stock> getResults() const;
    unsigned long getDelay() const;
    unsigned long getCurrentDelay() const;

    void setCurrentDelay(unsigned long delay);
};


#endif