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

    void whileIsDigit(const std::string &line, std::size_t &newIndex);
    void goAfterNextColon(const std::string &line, std::size_t &newIndex);
    void isEndOfLineValid(const std::string &line, std::size_t &index, std::size_t &newIndex);

    void verifyNextChar(const std::string &line, char c, std::size_t &index, std::size_t &newIndex);
    void passChar(const std::string &line, char c, std::size_t &index, std::size_t &newIndex);

    void readDelay(const std::string &delay);

    void readNextName(const std::string &line, std::string &nameTmp, std::size_t &index, std::size_t &newIndex);
    void readNextQuantity(const std::string &line, long &quantity, std::size_t &index, std::size_t &newIndex);

    void readStock(const std::string &line, std::string &nameTmp, std::size_t &index, std::size_t &newIndex);
    void readProcess(const std::string &line, std::string &nameTmp, std::size_t &index, std::size_t &newIndex);
    void readOptimizedStock(const std::string &line, std::size_t &index, std::size_t &newIndex);

    void addStockFromPorcess(const std::string &line, Process &processTmp, std::size_t &index, std::size_t &newIndex, bool isNeed);
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