
#ifndef PROCESSES_HPP
#define PROCESSES_HPP

#include <map>
#include <vector>
#include <string>

class Process {
    private:
        typedef std::pair<std::string, unsigned long> stocks;

        std::vector<stocks> needs;
        std::vector<stocks> results;

        unsigned long delay;
        unsigned long currentDelay;

    public:

    Process(std::vector<stocks> needs, std::vector<stocks> results, unsigned long delay);
    ~Process();

    std::vector<stocks> getNeeds() const;
    std::vector<stocks> getResults() const;
    unsigned long getDelay() const;
    unsigned long getCurrentDelay() const;

    void setCurrentDelay(unsigned long delay);
};


#endif