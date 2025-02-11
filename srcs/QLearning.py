import numpy as np
from itertools import combinations

# Define the environment
n_actions = 4  # Number of possible actions (do_montant, do_fond, do_etagere, do_armoire)
n_states = 16  # Number of states in the grid world (2^n_actions)
comb_list = [comb for i in range(1, n_actions + 1) for comb in combinations(range(n_actions), i)]
print(comb_list)

# Initialize Q-table with zeros
Q_table = np.zeros((n_states, n_actions))

# Define parameters
learning_rate = 0.8
discount_factor = 0.95
exploration_prob = 0.2
epochs = 1000

if __name__ == "__main__":
    
    for epoch in range(epochs):
    current_state = np.random.randint(0, n_states)  # Start from a random state

        while last_action != opti:

            # Choose action with epsilon-greedy strategy
            if np.random.rand() < exploration_prob:
                action = np.random.randint(0, n_actions)  # Explore
            else:
                action = np.argmax(Q_table[current_state])  # Exploit

            # actualiser notre etat en fonction du nouveau stock``
        

    