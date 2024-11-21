#ifndef DYNAMICPROGRAMMING_HPP
#define DYNAMICPROGRAMMING_HPP

#include "Process.hpp"
#include "list"
#include "Krpsim.hpp"

// Make a getStockPrice function 

class DynamicProgramming {

private:

    const std::map<std::string, Stock>    _stocks;
    const std::vector<Process>            _processes;

    // Optimization
    const bool                    _isTimeOpti;
    const std::set<std::string>   _optimizedStocks;

    Process             _chooseOptiFinalProcess() const;
    std::vector<Stock>  _getPrimaryNeeds(const std::vector<Stock>& needs) const;

public:

    DynamicProgramming(const Krpsim& krpsim);
    ~DynamicProgramming();
};

#endif
