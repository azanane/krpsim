#ifndef KRPSIM_HPP
#define KRPSIM_HPP

#include <map>
#include <string>
#include <set>
#include <chrono>
#include "Process.hpp"
#include "Stock.hpp"

class Krpsim {
    private:

        // Stocks and processes        
        std::map<std::string, Stock> stocks;
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

        std::map<std::string, Stock> getStocks() const;
        std::vector<Process> getProcesses() const;
        std::vector<Process> getInUsedProcess() const;

        // Optimization
        bool getIsTimeOpti() const;
        std::set<std::string> getOptimizedStocks() const;

        // Delays
        unsigned long getMaxDelay() const;
        unsigned long getCurrentDelay() const;
};


#endif