#ifndef DYNAMICPROGRAMMING_HPP
#define DYNAMICPROGRAMMING_HPP

#include "Process.hpp"
#include "vector"

// Make a getStockPrice function 

class DynamicProgramming {

private:
    std::vector<Process> chooseOptiFinalProcess();
    std::vector<Process> getFinalProcesses() const;

public:
    DynamicProgramming();
    ~DynamicProgramming();
};

#endif
