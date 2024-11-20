
#ifndef PROCESSES_HPP
#define PROCESSES_HPP

#include <map>
#include <vector>
#include <string>
#include "Stock.hpp"

class Process {
    private:
        std::string         name;
        std::vector<Stock>  needs;
        std::vector<Stock>  results;

        unsigned long delay;
        unsigned long currentDelay;

    public:



    Process();
    ~Process();

    std::string getName() const;
    std::vector<Stock> getNeeds() const;
    std::vector<Stock> getResults() const;
    unsigned long getDelay() const;
    unsigned long getCurrentDelay() const;

    void setName(std::string name);
    void setCurrentDelay(unsigned long delay);
    void setDelay(unsigned long delay);
    void addNeed(Stock stock);
    void addResult(Stock stock);
};


#endif