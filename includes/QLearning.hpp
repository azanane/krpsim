#ifndef QLEARNING_HPP
#define QLEARNING_HPP

#include "Process.hpp"
#include <map>
#include "Krpsim.hpp"
#include <cstdlib>

class QLearning {

private:

	float	_learningRate;
	float	_discountFactor;
	float	_explorationProb;

	int		_epochs;

	std::map<Process, float>	_qTable;

public:

	QLearning(const Krpsim& krpsim);
	~QLearning();

	void solve();
};

#endif