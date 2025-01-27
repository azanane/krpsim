[<-- Back](../../README.md)
## Greedy Search algorithms

There are a lot of [differents algorithms](##Sources) that implement greedy search (first link in sources).

### Characteristics of a greedy algorithm: 

- Greedy algorithms are simple and easy to implement.
They are efficient in terms of time complexity, often providing quick solutions.
- Greedy Algorithms are typically preferred over Dynamic Programming for the problems where both are applied. For example, Jump Game problem and Single Source Shortest Path Problem (Dijkstra is preferred over Bellman Ford where we do not have negative weights)..
- These algorithms do not reconsider previous choices, as they make decisions based on current information without looking ahead.

### Here’s how it works:

- Start with the initial state of the problem. This is the starting point from where you begin making choices.
- Evaluate all possible choices you can make from the current state. Consider all the options available at that specific moment.
- Choose the option that seems best at that moment, regardless of future consequences. This is the “greedy” part – you take the best option available now, even if it might not be the best in the long run.
- Move to the new state based on your chosen option. This becomes your new starting point for the next iteration.
- Repeat steps 2-4 until you reach the goal state or no further progress is possible. Keep making the best local choices until you reach the end of the problem or get stuck..


### Is Greedy approch good for our project

The greedy algorithm approch assume that we will be able to find the optimal global solution by finding optimal local solutions. 
While this is true for simple processes, it is not for harder one such as the "pomme" in resources.  
Therefore, we either will have to use another type of algroithm such as **Dynamic computing** or we will have to optimize our greedy search in order to take in account future needs instead of just immediate gains.
For this we enhance our search with: 
- Defining a Dynamic Priority Heuristic:
    - Start with a priority heuristic that considers both immediate gains and future needs. For example, prioritize actions that yield high profits relative to cost and time but adjust this priority based on remaining resources like "euro" and "four."
    - Adjust priorities dynamically, so actions like "do_boite" are only prioritized if the resources needed (e.g., "tarte_citron", "tarte_pomme") are available or near availability. 
- Resource-Based Decision Pruning:
    - Prune actions that don’t align with available or obtainable resources. For instance, if "pate sablee" isn’t available, deprioritize "do_tarte_pomme" and instead focus on actions that could bring in the necessary resources.
    - Set rules to prioritize actions that generate essential resources if they’re low (like "euro" or "four").
- Track and Reevaluate:
    - After each greedy selection, re-evaluate the priority of future actions based on the updated state. This iterative refinement ensures that the algorithm remains adaptive to the evolving resources and constraints.
- Use Look-Ahead or Limited Depth Search:
    - Implement a limited look-ahead by simulating a few actions forward and choosing the path that yields the highest return within the limits of current resources.
    - Alternatively, use a breadth-first search (BFS) up to a certain depth to explore multiple sequences and pick the best-performing initial actions, which will help avoid premature greedy decisions.


## Sources
[Geeks for geeks : Greedy algorithm](https://www.geeksforgeeks.org/greedy-algorithms/)