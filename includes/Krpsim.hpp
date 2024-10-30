#ifndef KRPSIM_HPP
#define KRPSIM_HPP

#include <map>
#include <string>
#include <set>
#include <chrono>
#include "Process.hpp"

class Krpsim {
    private:
        typedef std::map<std::string, unsigned long> stocksType;

        // Stocks and processes        
        stocksType stocks;
        std::vector<Process> processes;
        std::vector<Process> inUsedProcess;

        // Optimization
        bool isTimeOpti;
        std::set<std::string> optimizedStocks;

        // Delays
        unsigned long maxDelay;
        unsigned long currentDelay;

    public:

    Krpsim(std::string fileName, unsigned long delay);
    ~Krpsim();
};


#endif