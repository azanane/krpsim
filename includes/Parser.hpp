#ifndef Parser_HPP
#define Parser_HPP

#include <fstream>
#include <string>
#include <iostream>
#include <map>
#include <algorithm>
#include <set>
#include "Stock.hpp"

class Parser {

private:

    std::string         filename;
    unsigned long       maxDelay;

    int whileIsDigit(std::string &line, std::size_t newIndex) const;
    int goAfterNextColon(std::string &line, std::size_t newIndex) const;
    void isEndOfQuantityLineValid(std::string &line, std::size_t &index, std::size_t &newIndex) const;
    void isEndOfStockLineValid(std::string &line, std::size_t &index, std::size_t &newIndex) const;

    void readNextName(std::string &line, std::string &nameTmp, std::size_t &index, std::size_t &newIndex);
    void readNextQuantity(std::string &line, long &quantity, std::size_t &index, std::size_t &newIndex);

public:
    // Constructors and Destructors
    Parser(const std::string fileName, const std::string delay);
    ~Parser();

    void parse();
    void parseFile(std::ifstream& inputFile);
};

#endif