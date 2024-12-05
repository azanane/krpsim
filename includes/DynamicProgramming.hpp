#ifndef DYNAMICPROGRAMMING_HPP
#define DYNAMICPROGRAMMING_HPP

#include "Process.hpp"
#include <list>
#include <queue>
#include "Krpsim.hpp"

// Make a getStockPrice function 


class DynamicProgramming {

private:

    typedef std::unordered_set<Stock, HashStock>::const_iterator stockSetIterator;
                      // Order them with cost
    // std::map<Process, std::priority_queue<std::map<Stock, std::list<Process>>, CmpCostPath>> _allSolutionsProcesses;
    std::map<Stock, std::list<std::list<Process>>> _allSolutionsStocks;

    const std::map<std::string, Stock>      _stocks;
    const std::map<std::string, Process>    _processes;

    std::list<std::list<Process>>   _allPaths;

    // Optimization
    const bool                    _isTimeOpti;
    const std::set<std::string>   _optimizedStocks;

    std::vector<Stock>              _getPrimaryNeeds(const std::vector<Stock>& needs) const;

    void                            _setAllPaths();
    std::list<std::list<Process>>   _getStockProcesses(const Stock& stock) const; 

public:

    DynamicProgramming(const Krpsim& krpsim);
    ~DynamicProgramming();
};

struct CmpCostPath
{
    bool operator()(std::list<Process>* lhs, std::list<Process>* rhs) const;
};

#endif
