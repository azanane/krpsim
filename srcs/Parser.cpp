#include "Parser.hpp"

Parser::Parser(const std::string fileName, const std::string delay) : filename(fileName) {
    int maxDelayTmp = std::atoi(delay.c_str());
    if (maxDelayTmp < 0) {
		throw std::invalid_argument("Invalid delay");
    }
    maxDelay = maxDelayTmp;
}

Parser::~Parser() {}

void Parser::parse() {

    std::ifstream inputFile;
    inputFile.open(this->filename);
	if (inputFile.fail()) {
		throw std::invalid_argument("Invalid text file");
	}

    try {
        this->parseFile(inputFile);
    }
    catch (std::exception &e){
        throw std::invalid_argument( e.what() );
    }
}

void Parser::parseFile(std::ifstream& inputFile) {

    std::string                             line;
    std::map<std::string, int>    stocks;
    std::string                             nameTmp;
    long                                    quantityTmp;
    int                                     indexTmp;

    while (std::getline(inputFile, line))
	{
        int i = 0;
        if (line[i] == '#')
            continue;
        indexTmp = goToNextColon(line, i);
        if (line[indexTmp] != '(') {
            // We are in a stock with name:quantity
            nameTmp = line.substr(i, indexTmp - i - 1);
            i = indexTmp;
            indexTmp = whileIsDigit(line, i);
            quantityTmp = std::atoi(line.substr(i, indexTmp - i).c_str());
            if (quantityTmp < 0) {
                throw std::invalid_argument("Quantity of " + nameTmp + " cannot be negative");
            }
            i = indexTmp;
            isEndOfLineValid(line, i);                
            stocks.insert(std::make_pair(nameTmp, quantityTmp));
        } else if (line[indexTmp] == '(') {

        } else {
            throw std::invalid_argument("Error for the line: " + line);
        }
    }

}

int Parser::whileIsDigit(std::string &line, std::size_t newIndex) const {
    while (std::isdigit(line[newIndex]) && newIndex < line.size()) {
        newIndex++;
    }
    return newIndex;
}

int Parser::goToNextColon(std::string &line, std::size_t newIndex) const {
    while (line[newIndex] != ':' && newIndex < line.size()) {
        newIndex++;
    }
    return ++newIndex;
}

void Parser::isEndOfLineValid(std::string &line, std::size_t newIndex) const {
    while (line[newIndex] != ' ' && newIndex < line.size()) {
        newIndex++;
    }
    if (!(newIndex == line.size() - 1 || line[newIndex] == '#')) {
        throw std::invalid_argument("Error for the line: " + line);
    } 
}