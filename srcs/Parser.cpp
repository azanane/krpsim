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
    isEndOfStockAndProcessLineValid(line, index, newIndex);           

    krpsim.addStock(Stock(nameTmp, quantityTmp));

}
void Parser::readProcess(std::string &line, std::string &nameTmp, std::size_t &index, std::size_t &newIndex) {

    Process     processTmp;
    long        quantityTmp;
    Stock       stockTmp;

    processTmp.setName(nameTmp);
    
    newIndex++;
    // Read the needs
    while (newIndex < line.size() - 1 && line[newIndex - 1] != ')') {
        readNextName(line, nameTmp, index, newIndex);
        readNextQuantity(line, quantityTmp, index, newIndex);
        stockTmp.setName(nameTmp);
        stockTmp.setQuantity(quantityTmp);
        processTmp.addNeed(stockTmp);
        newIndex++;
    }
    if (processTmp.getNeeds().empty()) {
        throw std::invalid_argument("No needs were given for the process: " + processTmp.getName());
    }
    newIndex += 2;
    // Read the results
    while (newIndex < line.size() -1 && line[newIndex - 1] != ')') {
        readNextName(line, nameTmp, index, newIndex);
        readNextQuantity(line, quantityTmp, index, newIndex);
        stockTmp.setName(nameTmp);
        stockTmp.setQuantity(quantityTmp);
        processTmp.addResult(stockTmp);
        newIndex++;
    }
    if (processTmp.getResults().empty()) {
        throw std::invalid_argument("No results were given for the process: " + processTmp.getName());
    }
    // Read the delay;
    if (newIndex < line.size() - 1 && line[newIndex] == ':') {
        newIndex++;
        readNextQuantity(line, quantityTmp, index, newIndex);
        processTmp.setDelay(quantityTmp);
    } else {
        throw std::invalid_argument("No delay were given for the process: " + processTmp.getName());
    }
    isEndOfStockAndProcessLineValid(line, index, newIndex);

    krpsim.addProcess(processTmp);
}
void Parser::readOptimizedStock(std::string &line, std::size_t &index, std::size_t &newIndex) {
    std::string nameTmp;
    newIndex++;
    while (newIndex < line.size() - 1 && line[newIndex - 1] != ')') {
        readNextName(line, nameTmp, index, newIndex);
        if (nameTmp == "time" && krpsim.getIsTimeOpti() != true) {
            krpsim.setIsTimeOpti(true);
        } else {
            krpsim.addOptimizedStocks(nameTmp);
        }
    }
    isEndOfOptiLineValid(line, index, --newIndex);
}

void Parser::readNextQuantity(std::string &line, long &quantity, std::size_t &index, std::size_t &newIndex) {
    index = newIndex;
    whileIsDigit(line, newIndex);
    quantity = std::atoi(line.substr(index, newIndex - index).c_str());
    if (quantity < 0) {
        throw std::invalid_argument("Quantity: " + std::to_string(quantity) + " cannot be negative");
    }
}

void Parser::readNextName(std::string &line, std::string &nameTmp, std::size_t &index, std::size_t &newIndex) {
    index = newIndex;
    goAfterNextColon(line, newIndex);
    nameTmp = line.substr(index, newIndex - index - 1);
    std::transform(nameTmp.begin(), nameTmp.end(), nameTmp.begin(), ::tolower);
}

void Parser::whileIsDigit(std::string &line, std::size_t &newIndex) {
    while (std::isdigit(line[newIndex]) && newIndex < line.size()) {
        newIndex++;
    }
}

void Parser::goAfterNextColon(std::string &line, std::size_t &newIndex) {
    while (line[newIndex] != ':' && line[newIndex] != '#' && line[newIndex] != ';' && newIndex < line.size() - 1) {
        newIndex++;
    }
    newIndex++;
}

void Parser::isEndOfStockAndProcessLineValid(std::string &line, std::size_t &index, std::size_t &newIndex) {
    index = newIndex;
    while (line[newIndex] != ' ' && newIndex < line.size()) {
        newIndex++;
    }
    if (!(newIndex == line.size() || line[newIndex] == '#')) {
        throw std::invalid_argument("Error for the line: " + line);
    } 
}

void Parser::isEndOfOptiLineValid(std::string &line, std::size_t &index, std::size_t &newIndex) {
    index = newIndex;
    if (line[newIndex] != ')') {
        throw std::invalid_argument("Wrong end of process or optimized line: " + line);
    }
    newIndex++;
    while (line[newIndex] != ' ' && newIndex < line.size()) {
        newIndex++;
    }
    if (!(newIndex == line.size() || line[newIndex] == '#')) {
        throw std::invalid_argument("Wrong end of process or optimzed line: " + line);
    } 
}

void Parser::initializeStock() {
    for (Process process : krpsim.getProcesses()) {
        for (Stock stock : process.getNeeds()) {
            if (krpsim.getStocks().find(stock.getName()) == krpsim.getStocks().end()) {
                stock.setQuantity(0);
                krpsim.addStock(stock);
            }
        }

        for (Stock stock : process.getResults()) {
            if (krpsim.getStocks().find(stock.getName()) == krpsim.getStocks().end()) {
                stock.setQuantity(0);
                krpsim.addStock(stock);
            }
        }
    }
}