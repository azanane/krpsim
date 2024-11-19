#include "Parser.hpp"

Parser::Parser(const std::string fileName, const std::string delay) : filename(fileName) {
    int maxDelayTmp = std::atoi(delay.c_str());
    if (maxDelayTmp < 0) {
		throw std::invalid_argument("Invalid delay");
    }
    maxDelay = maxDelayTmp;
    parse();
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
    std::map<std::string, Stock>            stocks;
    Stock                                   stockTmp;
    std::string                             nameTmp;
    long                                    quantityTmp;
    size_t                                  newIndex;
    size_t                                  index;
    std::set<std::string>                   optimizedStocks;
    bool                                    isTimeOpti = false;

    while (std::getline(inputFile, line))
	{
        nameTmp = "";
        quantityTmp = 0;
        index = 0;
        newIndex = 0;

        // Read the first word, so we can know if we are in a stock, process or optimize description
        readNextName(line, nameTmp, index, newIndex);
        if (line[index] == '#' || nameTmp == "") {
            continue;
        }

        if (nameTmp == "optimize") {
            // We are in the optimize case
            while (newIndex != line.size() - 1) {
                readNextName(line, nameTmp, index, newIndex);
                if (nameTmp == "time" && isTimeOpti != true) {
                    isTimeOpti = true;
                } else {
                    optimizedStocks.insert(nameTmp);
                }
            }
            isEndOfQuantityLineValid(line, index, newIndex);
        } else if (line[newIndex] != '(') {
            // We are in a stock with name:quantity
            readNextQuantity(line, quantityTmp, index, newIndex);
            isEndOfStockLineValid(line, index, newIndex);           

            stockTmp.setName(nameTmp);
            stockTmp.setQuantity(quantityTmp);
            stocks.insert(std::make_pair(nameTmp, stockTmp));
        } else if (line[newIndex] == '(') {
            // We are in a process case
            break;

        } else {
            throw std::invalid_argument("Error for the line: " + line);
        }
    }

}

void Parser::readNextQuantity(std::string &line, long &quantity, std::size_t &index, std::size_t &newIndex) {
    index = newIndex;
    newIndex = whileIsDigit(line, index);
    quantity = std::atoi(line.substr(index, newIndex - index).c_str());
    if (quantity < 0) {
        throw std::invalid_argument("Quantity: " + std::to_string(quantity) + " cannot be negative");
    }
}

void Parser::readNextName(std::string &line, std::string &nameTmp, std::size_t &index, std::size_t &newIndex) {
    index = newIndex;
    newIndex = goAfterNextColon(line, index);
    if (newIndex == line.size() - 1) {
        return;
    }
    nameTmp = line.substr(index, newIndex - index - 1);
    std::transform(nameTmp.begin(), nameTmp.end(), nameTmp.begin(), ::tolower);
}

int Parser::whileIsDigit(std::string &line, std::size_t newIndex) const {
    while (std::isdigit(line[newIndex]) && newIndex < line.size()) {
        newIndex++;
    }
    return newIndex;
}

int Parser::goAfterNextColon(std::string &line, std::size_t newIndex) const {
    while ((line[newIndex] != ':' || line[newIndex] != '#' || line[newIndex] != ';') && newIndex < line.size()) {
        newIndex++;
    }
    return ++newIndex;
}

void Parser::isEndOfStockLineValid(std::string &line, std::size_t &index, std::size_t &newIndex) const {
    index = newIndex;
    while (line[newIndex] != ' ' && newIndex < line.size()) {
        newIndex++;
    }
    if (!(newIndex == line.size() - 1 || line[newIndex] == '#')) {
        throw std::invalid_argument("Error for the line: " + line);
    } 
}

void Parser::isEndOfQuantityLineValid(std::string &line, std::size_t &index, std::size_t &newIndex) const {
    index = newIndex;
    if (line[newIndex] != ')') {
        throw std::invalid_argument("Wrong end of Quantity line: " + line);
    }
    newIndex++;
    while (line[newIndex] != ' ' && newIndex < line.size()) {
        newIndex++;
    }
    if (!(newIndex == line.size() - 1 || line[newIndex] == '#')) {
        throw std::invalid_argument("Wrong end of Quantity line: " + line);
    } 
}