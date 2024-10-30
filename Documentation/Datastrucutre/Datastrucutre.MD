[<-- Back](../../README.md)
## The datastructure

Lets check what the file input contains : 
- A description of the available stocks in the beginning, in a simple <stock_name>:<quantity\> format
- A process description
<name\>:(<need\>:<qty\>[;<need\>:<qty\>[...]]):(<result\>:<qty\>[;<result\>:<qty\>[...]]):<nb_cycle\>
A process can start as soon as the stocks allow it. This can happen several times
in the same cycle.
- One line only to indicate the elements that would need optimizing containing the
key word time :
optimize:(<stock_name>|time[;<stock_name>|time[...]])

Moreover, we have a maximum delay that is going to be given as an argument.

We also know that the **stock_name** is going to match the **needs**.map


### Process class

The stock will be represented by a std::pair<std::string, unsigned long>, which are going to be the name and the value

The Process class will have:
- A list of stocks that are going to represent the needs
- A list of stocks that are going to represent the results
- The delay the process is going to take
- The current delay the process has been running

### Krpsim class

The stocks are going to be represented by a std::map<std::string, unsigned long>, which are going to be the name and the value

The Krpsim class will have: 
- The current stocks we have
- A list of procceses that are defined in the file
- A list of processes that are in used 
- A boolean to know if we want to optimize the time
- A set of stocks to optimized
- The maximum delay
- The current delay
