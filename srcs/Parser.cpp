#include "Parser.hpp"

Parser::Parser(const std::string fileName, const std::string delay) {
    this->filename = fileName;
    int maxDelayTmp = std::atoi(delay.c_str());
    if (maxDelayTmp < 0) {
		std::cerr << "Invalid delay" << std::endl;
        exit(1);
    }
    krpsim.setMaxDelay(maxDelayTmp);
    parse();
}

Parser::~Parser() {}

void Parser::parse() {

    std::ifstream inputFile;
    inputFile.open(this->filename);
	if (inputFile.fail()) {
		std::cerr << "Invalid text file" << std::endl;
        exit(1);
	}

    try {
        this->parseFile(inputFile);
        this->initializeStock();
    }
    catch (std::exception &e){
        std::cerr << e.what() << std::endl;
        exit(1);
    }
}

Krpsim Parser::getKrspim() const {
    return krpsim;
}

void Parser::parseFile(std::ifstream& inputFile) {

    std::string                             line;
    std::string                             nameTmp;
    size_t                                  index;
    size_t                                  newIndex;

    while (std::getline(inputFile, line))
	{
        nameTmp = "";
        index = 0;
        newIndex = 0;

        // Read the first word, so we can know if we are in a stock, process or optimize description
        readNextName(line, nameTmp, index, newIndex);
        if (line[index] == '#' || nameTmp == "") {
            continue;
        }
        if (newIndex >= line.size()) {
            throw std::invalid_argument("Error for the line: " + line);
        }
        verifyNextChar(line, ':', index, newIndex);
        if (nameTmp == "optimize") {
            // We are in the optimize case
            readOptimizedStock(line, index, newIndex);
        } else if (line[newIndex] != '(') {
            // We are in a stock with name:quantity
            readStock(line, nameTmp, index, newIndex);
        } else if (line[newIndex] == '(') {
            // We are in a process case
            readProcess(line, nameTmp, index, newIndex);
        } else {
            throw std::invalid_argument("Error for the line: " + line);
        }
    }
}

void Parser::readStock(std::string &line, std::string &nameTmp, std::size_t &index, std::size_t &newIndex) {
    long   quantityTmp;

    readNextQuantity(line, quantityTmp, index, newIndex);
    isEndOfLineValid(line, index, newIndex);           

    krpsim.addOrUpdateStock(Stock(nameTmp, quantityTmp));
}
void Parser::readProcess(std::string &line, std::string &nameTmp, std::size_t &index, std::size_t &newIndex) {

    Process     processTmp;
    long        quantityTmp;
    Stock       stockTmp;

    processTmp.setName(nameTmp);
    
    verifyNextChar(line, '(', index, newIndex);
    // Read the needs
    addStockFromPorcess(line, processTmp, index, newIndex, true);
    if (processTmp.getNeeds().empty()) {
        throw std::invalid_argument("No needs were given for the process: " + processTmp.getName());
    }
    verifyNextChar(line, ')', index, newIndex);
    verifyNextChar(line, ':', index, newIndex);
    // Results can be empty
    try {
        verifyNextChar(line, '(', index, newIndex);
        // Read the results
        addStockFromPorcess(line, processTmp, index, newIndex, false);
        if (processTmp.getResults().empty()) {
            throw std::invalid_argument("No results were given for the process: " + processTmp.getName());
        }
        verifyNextChar(line, ')', index, newIndex);
        verifyNextChar(line, ':', index, newIndex);
    }
    catch (std::exception e) {
        if (!isdigit(line[newIndex])) {
            throw std::invalid_argument("Error occured in line: " + line + ". Char \'" + line[newIndex] + "\' where given at index " + std::to_string(newIndex) + " instead of a delay");
        }
    }
    // Read the delay;
    readNextQuantity(line, quantityTmp, index, newIndex);
    processTmp.setDelay(quantityTmp);
    isEndOfLineValid(line, index, newIndex);

    krpsim.addProcess(processTmp);
}

void Parser::readOptimizedStock(std::string &line, std::size_t &index, std::size_t &newIndex) {
    std::string nameTmp;

    verifyNextChar(line, '(', index, newIndex);
    while (newIndex < line.size() - 1 && line[newIndex - 1] != ')') {
        readNextName(line, nameTmp, index, newIndex);
        if (nameTmp == "time" && krpsim.getIsTimeOpti() != true) {
            krpsim.setIsTimeOpti(true);
        } else {
            krpsim.addOptimizedStocks(nameTmp);
        }
        if (line[newIndex] == ')') {
            break;
        }
        verifyNextChar(line, ';', index, newIndex);
    }
    verifyNextChar(line, ')', index, newIndex);
    isEndOfLineValid(line, index, --newIndex);
}

void Parser::readNextQuantity(std::string &line, long &quantity, std::size_t &index, std::size_t &newIndex) {
    index = newIndex;
    whileIsDigit(line, newIndex);
    quantity = std::atoi(line.substr(index, newIndex + 1 - index).c_str());
    if (quantity < 0) {
        throw std::invalid_argument("Error occured ine line: " + line + ". Quantity: " + std::to_string(quantity) + " cannot be negative");
    }
}

void Parser::addStockFromPorcess(std::string &line, Process &processTmp, std::size_t &index, std::size_t &newIndex, bool isNeed) {
    std::string nameTmp;
    long        quantityTmp;
    Stock       stockTmp;

    while (newIndex < line.size() - 1 && line[newIndex] != ')') {
        readNextName(line, nameTmp, index, newIndex);
        verifyNextChar(line, ':', index, newIndex);
        readNextQuantity(line, quantityTmp, index, newIndex);
        passChar(line, ' ', index, newIndex);
        if (line[newIndex] != ')') {
            verifyNextChar(line, ';', index, newIndex);
        }
        stockTmp.setName(nameTmp);
        stockTmp.setQuantity(quantityTmp);
        isNeed ? processTmp.addNeed(stockTmp) : processTmp.addResult(stockTmp);
    }
    index = newIndex;
}

void Parser::passChar(std::string &line, char c, std::size_t &index, std::size_t &newIndex) {
    while (line[newIndex] == c) {
        newIndex++;
    }
    index = newIndex;
}

void Parser::verifyNextChar(std::string &line, char c, std::size_t &index, std::size_t &newIndex) {
    passChar(line, ' ', index, newIndex);
    if (line[newIndex] != c){
        throw std::invalid_argument("Error occured in line: " + line + ". Char \'" + line[newIndex] + "\' where given at index " + std::to_string(newIndex) + " instead of char \'" + c + "\'");
    } else {
        passChar(line, c, index, newIndex);
    }
    passChar(line, ' ', index, newIndex);
}

void Parser::readNextName(std::string &line, std::string &nameTmp, std::size_t &index, std::size_t &newIndex) {
    index = newIndex;
    goAfterNextColon(line, newIndex);
    nameTmp = line.substr(index, newIndex - index);
    std::transform(nameTmp.begin(), nameTmp.end(), nameTmp.begin(), ::tolower);
}

void Parser::whileIsDigit(std::string &line, std::size_t &newIndex) {
    if (line[newIndex] == '-') {
        newIndex++;
    }
    while (std::isdigit(line[newIndex]) && newIndex < line.size() - 1) {
        newIndex++;
    }
}

void Parser::goAfterNextColon(std::string &line, std::size_t &newIndex) {
    while (line[newIndex] != ':' && line[newIndex] != '#' && line[newIndex] != ';' && line[newIndex] != ' ' && newIndex < line.size() - 1) {
        newIndex++;
    }
}

void Parser::isEndOfLineValid(std::string &line, std::size_t &index, std::size_t &newIndex) {
    index = newIndex;
    while (line[newIndex] != ' ' && newIndex < line.size() - 1) {
        newIndex++;
    }
    if (!(newIndex == line.size() - 1 || line[newIndex] == '#')) {
        throw std::invalid_argument("Wrong end of process or optimzed line: " + line);
    } 
}

void Parser::initializeStock() {
    std::map<std::string, Stock> stocks = krpsim.getStocks();
    for (Process process : krpsim.getProcesses()) {
        for (Stock stock : process.getNeeds()) {
            if (stocks.find(stock.getName()) == stocks.end()) {
                stock.setQuantity(0);
                krpsim.addStock(stock);
            }
        }
        for (Stock stock : process.getResults()) {
            std::map<std::string, Stock>::iterator it = stocks.find(stock.getName());
            if (it == stocks.end()) {
                stock.setQuantity(0);
            } else {
                stock.setQuantity(it->second.getQuantity());
            }
            stock.addProcess(process.getName());
            krpsim.addOrUpdateStock(stock);
        }
    }
}
