#ifndef Parser_HPP
#define Parser_HPP

#include <fstream>
#include <string>
#include <iostream>
#include <map>
#include <algorithm>


class Parser {

private:

    std::string         filename;
    unsigned long       maxDelay;

    int whileIsDigit(std::string &line, std::size_t newIndex) const;
    int goToNextColon(std::string &line, std::size_t newIndex) const;
    void isEndOfLineValid(std::string &line, std::size_t newIndex) const;

public:
    // Constructors and Destructors
    Parser(const std::string fileName, const std::string delay);
    ~Parser();

    void parse();
    void parseFile(std::ifstream& inputFile);
};

#endif