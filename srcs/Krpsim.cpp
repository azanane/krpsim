#include "Krpsim.hpp"

Krpsim::Krpsim(std::string fileName, unsigned long delay) {
    (void)fileName;
    (void)isTimeOpti;

    maxDelay = delay;
    currentDelay = 0;
}

Krpsim::~Krpsim() {}


