
#ifndef PROCESSES_HPP
#define PROCESSES_HPP

#include <map>
#include <vector>
#include <string>

class Process {
    private:
        typedef std::pair<std::string, unsigned long> stockType;

        std::vector<stockType> needs;
        std::vector<stockType> results;

        unsigned long delay;
        unsigned long currentDelay;

    public:

    Process(std::vector<stockType> needs, std::vector<stockType> results, unsigned long delay);
    ~Process();

    std::vector<stockType> getNeeds() const;
    std::vector<stockType> getResults() const;
    unsigned long getDelay() const;
    unsigned long getCurrentDelay() const;

    void setCurrentDelay(unsigned long delay);
};


#endif