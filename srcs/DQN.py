import numpy as np
import math
import matplotlib.pyplot as plt
from collections import deque
import copy
import random
import heapq
import torch
from torch import nn
import torch.nn.functional as F

# Define model
class DQN(nn.Module):
    def __init__(self, in_states, h1_nodes, out_actions):
        super().__init__()

        # Define network layers
        self.fc1 = nn.Linear(in_states, h1_nodes)   # first fully connected layer
        nn.init.normal_(self.fc1.weight, mean=0, std=0.01)
        nn.init.normal_(self.fc1.bias, mean=0, std=0.01)

        self.out = nn.Linear(h1_nodes, out_actions) # ouptut layer w
        nn.init.normal_(self.out.weight, mean=0, std=0.01)


    def forward(self, x):
        x = F.relu(self.fc1(x)) # Apply rectified linear unit (ReLU) activation
        x = self.out(x)         # Calculate output
        return x

# Define memory for Experience Replay
class ReplayMemory():
    def __init__(self, maxlen):
        self.memory = deque([], maxlen=maxlen)
    
    def append(self, transition):
        self.memory.append(transition)

    def sample(self, sample_size):
        return random.sample(self.memory, sample_size)

    def __len__(self):
        return len(self.memory)

# FrozeLake Deep Q-Learning
class KrpsimDQN():

    ACTIONS = ['0','1','2','3', '4']

    def __init__(self, stocks, processes, optimized_stock=["euro"], delay = 1000):
        self.stocks = stocks
        self.current_stocks = copy.copy(stocks)
        self.processes = processes

        # Hyperparameters (adjustable)
        self.learning_rate_a = 0.01         # learning rate (alpha)
        self.discount_factor_g = 0.9         # discount rate (gamma)    
        self.network_sync_rate = 10          # number of steps the agent takes before syncing the policy and target network
        self.replay_memory_size = 10000       # size of replay memory
        self.mini_batch_size = 32           # size of the training data set sampled from the replay memory

        # Neural Network
        self.loss_fn = nn.MSELoss()          # NN Loss function. MSE=Mean Squared Error can be swapped to something else.
        self.optimizer = None                # NN Optimizer. Initialize later.

        self.optimized_stock_name = optimized_stock

        # Store optimized processes beforehand to reduce looping
        self.optimized_processes = [
            process for process in processes if any(stock in process.results for stock in optimized_stock)
        ]

        # Precompute max stock values for optimization
        self.max_values = {
            key: max(p.needs.get(key, 0) for p in processes)
            for p in processes for key in p.needs
        }

        self.current_processes = []  # This will be our priority queue (min-heap)

        # For ploting
        self.optimized_stock_evo = {}

        self.current_delay = 0
        self.delay = delay

    def is_anything_doable(self, stocks, check_current_process):
        for i, process in enumerate(self.processes):
            can_do_process = True
            for item, required_quantity in process.needs.items():
                # If the required quantity of any item is greater than the stock, the process cannot be done
                if stocks.get(item, 0) < required_quantity:
                    can_do_process = False
            if can_do_process == True and i != 0:
                return True
        if self.current_processes != [] and check_current_process:
            return True
        return False


    def get_processes_with_smallest_delay(self):
        """Retrieve all processes with the smallest delay."""
        if not self.current_processes:
            return []

        # Get the smallest delay
        smallest_delay = self.current_processes[0].delay
        processes_with_smallest_delay = []

        # Pop all processes with the smallest delay
        while self.current_processes and self.current_processes[0].delay == smallest_delay:
            process = heapq.heappop(self.current_processes)
            processes_with_smallest_delay.append(process)

        self.current_delay = smallest_delay

        # Return the list of processes with the smallest delay
        return processes_with_smallest_delay

    def update_stock_and_time(self):
        smallest_process = self.get_processes_with_smallest_delay()
        for process in smallest_process:
            for key, value in process.results.items():
                self.stocks[key] += value

        # faire un graph de l'evo de l'argent en fonction de l'epoch et du delay
        # if self.not_training:
        #     self.optimized_stock_evo[self.current_delay] = self.stocks[self.optimized_stock_name[0]]

    def get_state(self, stocks):

        state = 0

        for i, process in enumerate(self.processes):
            # Check if all required items (needs) are available in stock
            can_do_process = True

            for item, required_quantity in process.needs.items():

                # If the required quantity of any item is greater than the stock, the process cannot be done
                if stocks.get(item, 0) < required_quantity:
                    can_do_process = False
                    break

            if can_do_process and i != 0:
                # If all requirements are met, add the process index to the list
                state += math.pow(2, i - 1)

        # -1 because we use it as an index in state_to_dqn_input 
        return int(state)

    def is_doable(self, stocks, proccess_index):

        for item, required_quantity in self.processes[proccess_index].needs.items():
            # If the required quantity of any item is greater than the stock, the process cannot be done
            if stocks.get(item, 0) < required_quantity:
                return False
        return True
    
    def get_reward(self, process_index, is_doable): 
        if is_doable == False:
            return -1
        # elif self.processes[process_index].needs and not self.processes[process_index].results:
        #     return -100


        processTmp = self.processes[process_index]

        # By default we give negative reward for useless action
        reward = 0

        for key, value in processTmp.results.items():
            # value_needed = processTmp.needs.get(key, 0)
            # if our stock is too big we give negative reward
            # if key not in self.optimized_stock_name and self.current_stocks.get(key, 1) > self.max_values.get(key, 1) * 5:
            #     reward += -10 * value
            # if it is something we want to optimize we give a positive reward
            if key in self.optimized_stock_name and processTmp in self.optimized_processes:
                reward += 1
        
        # for key, value in processTmp.needs.items():
        #     if key in self.optimized_stock_name and self.current_stocks.get(key, 1) > self.max_values.get(key, 1) * 5:
        #         reward += -10 * value

        return reward
    
    def run_process(self, process_index, state):
        process = copy.copy(self.processes[process_index])
        is_doable = self.is_doable(self.stocks, process_index)
        reward = self.get_reward(process_index, is_doable)
        # if is_doable:
        #     if self.verbose == True and process_index != 0:
        #     # if process_index != 0:
        #         print(f'{self.current_delay}: {self.processes[process_index].name}')
        #     if self.actions.get(process.name) != None:
        #         self.actions[process.name] += 1
        #     else:
        #         self.actions[process.name] = 1

        # Remove from the stock the needs, and upgrade directly by removing and adding de current_stock
        if is_doable and process_index != 0:
            for key, value in process.needs.items():
                self.stocks[key] -= value
                self.current_stocks[key] -= value
            process.delay += self.current_delay
            heapq.heappush(self.current_processes, process)
            for key, value in process.results.items():
                self.current_stocks[key] += value
            # if self.get_state(self.current_stocks) == state:
            #     reward -= 50
            if self.get_state(self.current_stocks) == 0 and self.current_stocks["armoire"] == 0:
                reward -= 1

        stateTmp = copy.copy(self.get_state(self.stocks))
        while stateTmp == self.get_state(self.stocks) and self.current_processes != [] and process_index == 0:
            self.update_stock_and_time()

        next_state = self.get_state(self.current_stocks)
        return next_state, reward


    def train(self, episodes, render=False, is_slippery=False, verbose = False):
        self.verbose = verbose

        # -1 because the first action (do nothing is always possible)
        num_states = int(math.pow(2, len(self.processes) - 1))
        num_actions = len(self.processes)
        
        epsilon = 1 # 1 = 100% random actions
        memory = ReplayMemory(self.replay_memory_size)

        # Create policy and target network. Number of nodes in the hidden layer can be adjusted.
        policy_dqn = DQN(in_states=num_states, h1_nodes=num_states, out_actions=num_actions)
        target_dqn = DQN(in_states=num_states, h1_nodes=num_states, out_actions=num_actions)

        # Make the target and policy networks the same (copy weights/biases from one network to the other)
        target_dqn.load_state_dict(policy_dqn.state_dict())

        print('Policy (random, before training):')
        self.print_dqn(policy_dqn)

        # Policy network optimizer. "Adam" optimizer can be swapped to something else. 
        self.optimizer = torch.optim.Adam(policy_dqn.parameters(), lr=self.learning_rate_a)

        # # List to keep track of rewards collected per episode. Initialize list to 0's.
        # rewards_per_episode = np.zeros(episodes)

        # List to keep track of epsilon decay
        epsilon_history = []

        # Track number of steps taken. Used for syncing policy => target network.
        step_count=0
            
        for i in range(episodes):
            state = self.get_state(self.stocks)  # Initialize to state 0
            stocks_tmp = copy.copy(self.stocks)
            terminated = False      # True when agent falls in hole or reached goal
            truncated = False       # True when agent takes more than 200 actions    

            # Agent navigates map until it falls into hole/reaches goal (terminated), or has taken 200 actions (truncated).
            while (self.is_anything_doable(self.stocks, True) and self.current_delay < self.delay):

                # Select action based on epsilon-greedy
                if random.random() < epsilon:
                    # select random action
                    process_index = random.randint(0, len(self.processes) - 1) # Explore process space
                else:
                    # select best action            
                    with torch.no_grad():
                        process_index = policy_dqn(self.state_to_dqn_input(state, num_states)).argmax().item()

                # Execute action
                new_state,reward = self.run_process(process_index, state)


                # Save experience into memory
                memory.append((state, process_index, new_state, reward))


                # Move to the next state
                state = new_state

                # Increment step counter
                step_count+=1

            # # Keep track of the rewards collected per episode.
            # if reward == 1:
            #     rewards_per_episode[i] = 1

            # Check if enough experience has been collected
            if len(memory)>self.mini_batch_size:

                b = 32
                while b < 100:
                    mini_batch = memory.sample(self.mini_batch_size)
                    self.optimize(mini_batch, policy_dqn, target_dqn)
                    b += 32        

                # Decay epsilon
                epsilon = max(epsilon - 1/episodes, 0)
                epsilon_history.append(epsilon)

                # Copy policy network to target network after a certain number of steps
                if step_count > self.network_sync_rate:
                    target_dqn.load_state_dict(policy_dqn.state_dict())
                    step_count=0

            print(self.stocks["armoire"])

            self.stocks = copy.copy(stocks_tmp)
            self.current_stocks = copy.copy(stocks_tmp)

        self.print_dqn(target_dqn)
        # # Save policy
        # torch.save(policy_dqn.state_dict(), "krpsim_dql.pt")

        # # Create new graph 
        # plt.figure(1)

        # # Plot average rewards (Y-axis) vs episodes (X-axis)
        # sum_rewards = np.zeros(episodes)
        # for x in range(episodes):
        #     sum_rewards[x] = np.sum(rewards_per_episode[max(0, x-100):(x+1)])
        # plt.subplot(121) # plot on a 1 row x 2 col grid, at cell 1
        # plt.plot(sum_rewards)
        
        # # Plot epsilon decay (Y-axis) vs episodes (X-axis)
        # plt.subplot(122) # plot on a 1 row x 2 col grid, at cell 2
        # plt.plot(epsilon_history)
        
        # # Save plots
        # plt.savefig('krpsim_dql.png')

    # Optimize policy network
    def optimize(self, mini_batch, policy_dqn, target_dqn):

        # Get number of input nodes
        num_states = policy_dqn.fc1.in_features

        current_q_list = []
        target_q_list = []

        for state, action, new_state, reward in mini_batch:

            with torch.no_grad():
                target = torch.FloatTensor(
                    reward + self.discount_factor_g * target_dqn(self.state_to_dqn_input(new_state, num_states)).max()
                )

            # Get the current set of Q values
            current_q = policy_dqn(self.state_to_dqn_input(state, num_states))
            current_q_list.append(current_q)

            # Get the target set of Q values
            target_q = target_dqn(self.state_to_dqn_input(state, num_states)) 
            # Adjust the specific action to the target that was just calculated
            target_q[action] = target
            target_q_list.append(target_q)
                
        # Compute loss for the whole minibatch
        loss = self.loss_fn(torch.stack(current_q_list), torch.stack(target_q_list))

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    '''
    Converts an state (int) to a tensor representation.
    For example, the FrozenLake 4x4 map has 4x4=16 states numbered from 0 to 15. 

    Parameters: state=1, num_states=16
    Return: tensor([0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
    '''
    def state_to_dqn_input(self, state:int, num_states:int)->torch.Tensor:
        input_tensor = torch.zeros(num_states)
        input_tensor[state] = 1
        return input_tensor





    # Run the FrozeLake environment with the learned policy
    def test(self, episodes, is_slippery=False):
        # Create FrozenLake instance
        num_states = math.pow(2, len(self.processes))
        num_actions = len(self.processes)

        # Load learned policy
        policy_dqn = DQN(in_states=num_states, h1_nodes=num_states, out_actions=num_actions) 
        policy_dqn.load_state_dict(torch.load("krpsim_dql.pt"))
        policy_dqn.eval()    # switch model to evaluation mode

        print('Policy (trained):')
        self.print_dqn(policy_dqn)

        for i in range(episodes):
            state = self.get_state(self.stock)  # Initialize to state 0
            terminated = False      # True when agent falls in hole or reached goal
            truncated = False       # True when agent takes more than 200 actions            

            # Agent navigates map until it falls into a hole (terminated), reaches goal (terminated), or has taken 200 actions (truncated).
            while(not terminated and not truncated):  
                # Select best action   
                with torch.no_grad():
                    action = policy_dqn(self.state_to_dqn_input(state, num_states)).argmax().item()

                # Execute action
                state,reward,terminated,truncated,_ = env.step(action)


    # Print DQN: state, best action, q values
    def print_dqn(self, dqn):
        # Get number of input nodes
        num_states = dqn.fc1.in_features

        # Loop each state and print policy to console
        for s in range(num_states):
            #  Format q values for printing
            q_values = ''
            for q in dqn(self.state_to_dqn_input(s, num_states)).tolist():
                q_values += "{:+.2f}".format(q)+' '  # Concatenate q values, format to 2 decimals
            q_values=q_values.rstrip()              # Remove space at the end

            # Map the best action 
            best_action = self.ACTIONS[dqn(self.state_to_dqn_input(s, num_states)).argmax()]

            # Print policy in the format of: state, action, q values
            # The printed layout matches the FrozenLake map.
            print(f'{s:02},{best_action} [{q_values}]', end=' ')         
            if (s+1)%4==0:
                print() # Print a newline every 4 states
