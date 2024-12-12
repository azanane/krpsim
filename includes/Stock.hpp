#ifndef STOCK_HPP
#define STOCK_HPP

#include <string>
#include <vector>
#include <map>

class Stock
{
private:
    std::string                     name;
    long                            quantity;
    std::map<std::string, long>     associateProcessesProfits;

public:
    Stock();
    Stock(std::string name, long quantity);
    ~Stock();

    std::string getName() const;
    long getQuantity() const;
    std::map<std::string, long> getAssociateProcessesProfits() const;

    void setName(std::string name);
    void setQuantity(long quantity);

    void addProcessProfits(std::pair<std::string, long> processName);
    void addProcessesProfits(std::map<std::string, long> processesName);

    bool operator==(const Stock &stock) const;
    bool operator<(const Stock &stock) const; 
};

struct HashStock
{
    std::size_t operator()(const Stock &stock) const;
};

#endif