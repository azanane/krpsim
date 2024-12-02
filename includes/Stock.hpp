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
    Stock();
    Stock(std::string name, long quantity);
    ~Stock();

    std::string getName() const;
    long getQuantity() const;
    std::vector<std::string> getAssociateProcesses() const;

    void setName(std::string name);
    void setQuantity(long quantity);

    void addProcess(std::string processName);
    void addProcesses(std::vector<std::string> processesName);

    bool operator==(const Stock &stock) const; 
};

struct HashStock
{
    std::size_t operator()(const Stock &stock) const;
};



#endif