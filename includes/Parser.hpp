#ifndef Parser_HPP
#define Parser_HPP

#include <fstream>
#include <string>
#include <iostream>
#include <map>
#include <algorithm>
#include <set>
#include "Krpsim.hpp"
#include "Stock.hpp"
#include "Process.hpp"


class Parser {

private:

    std::string         filename;

    Krpsim              krpsim;

    void whileIsDigit(std::string &line, std::size_t &newIndex);
    void goAfterNextColon(std::string &line, std::size_t &newIndex);
    void isEndOfLineValid(std::string &line, std::size_t &index, std::size_t &newIndex);

    void verifyNextChar(std::string &line, char c, std::size_t &index, std::size_t &newIndex);
    void passChar(std::string &line, char c, std::size_t &index, std::size_t &newIndex);

    void readNextName(std::string &line, std::string &nameTmp, std::size_t &index, std::size_t &newIndex);
    void readNextQuantity(std::string &line, long &quantity, std::size_t &index, std::size_t &newIndex);

    void readStock(std::string &line, std::string &nameTmp, std::size_t &index, std::size_t &newIndex);
    void readProcess(std::string &line, std::string &nameTmp, std::size_t &index, std::size_t &newIndex);
    void readOptimizedStock(std::string &line, std::size_t &index, std::size_t &newIndex);

    void addStockFromPorcess(std::string &line, Process &processTmp, std::size_t &index, std::size_t &newIndex, bool isNeed);
    void initializeStock();

public:
    // Constructors and Destructors
    Parser(const std::string fileName, const std::string delay);
    ~Parser();

    void parse();
    void parseFile(std::ifstream& inputFile);

    Krpsim getKrspim() const;
};

#endif