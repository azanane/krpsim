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

        Krpsim();
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

        void setMaxDelay(unsigned long maxDelay);
        void setCurrentDelay(unsigned long currentDelay);

        void addOrUpdateStock(Stock stock);
        void addStock(Stock stock);
        void updateStock(Stock stock, std::map<std::string, Stock>::iterator &it);
        void addProcess(Process process);
        void addInUsedProcess(Process process);

        // Optimization
        void setIsTimeOpti(bool isTimeOpti);
        void addOptimizedStocks(std::string optimizedStock);
};


#endif