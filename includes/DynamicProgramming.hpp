#ifndef DYNAMICPROGRAMMING_HPP
#define DYNAMICPROGRAMMING_HPP

#include "Process.hpp"
#include <list>
#include <queue>
#include "Krpsim.hpp"

// Make a getStockPrice function 

class DynamicProgramming {

private:

    const std::map<std::string, Stock>      _stocks;
    const std::map<std::string, Process>    _processes;

    std::list<std::list<Process>>   _allPaths;

    // Optimization
    const bool                    _isTimeOpti;
    const std::set<std::string>   _optimizedStocks;

    Process                         _chooseOptiPath() const;
    std::vector<Stock>              _getPrimaryNeeds(const std::vector<Stock>& needs) const;

    void    _setAllPaths(std::list<std::list<Process>> path, std::map<Stock, std::list<std::list<Process>>> memo);

public:

    DynamicProgramming(const Krpsim& krpsim);
    ~DynamicProgramming();
};

#endif
