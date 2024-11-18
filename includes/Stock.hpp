#ifndef STOCK_HPP
#define STOCK_HPP

#include <string>
#include <vector>

class Stock
{
private:
    std::string                 name;
    long                        quantity;
    std::vector<std::string>    associateProcesses;

public:
    Stock(std::string name, long quantity);
    ~Stock();

    std::string getName() const;
    long getQuantity() const;
    std::vector<std::string> getAssociateProcesses() const;

    void addProcess(std::string processName);
    void addProcesses(std::vector<std::string> processesName);
};



#endif