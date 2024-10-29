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

We also know that the **stock_name** is going to match the **needs**.

#### Stocks
The stocks need to be a map where the name of the stock is going to be the key and the value is going to be the quantity

#### Processes
Each process need to be in a map where the key is going to be its name, and the value is going to be a pair of **list stocks** / **list stocks**, where the first one represent the needs, and the second one represent the results.

#### Optimization
A boolean if we want to optimize time or not
A list of stocks we want to optimize. It needs to be a list where we can easily check wether the sotck is in or not.

#### Delay
We will have the maximum delay, which will be given as argument and the current delay, which will be the delay the process has been running so far.

#### List of actions
This might not be necessary as the actions will be printed each time they are exectued.

A list where we are going to push each action we are taking througought the all process. 
