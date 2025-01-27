#include "QLearning.hpp"

QLearning::QLearning(const Krpsim& krpsim) : _stocks(krpsim.getStocks()), _processes(krpsim.getProcesses()), _isTimeOpti(krpsim.getIsTimeOpti()) {

	this->_learningRate = 0.5;
	this->_discountFactor = 0.9;
	this->_explorationProb = 0.2;

	this->_epochs = 1000;
}

QLearning:~QLearning() {}

void QLearning::solve() {
	
	for (int epoch : this->_epochs) {

		
	}
}
