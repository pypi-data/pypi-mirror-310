# Minimum Price Markov Game (MPMG) Environment

## Overview

`mpmg` is a modular environment designed for studying the Minimum Price Markov Game (MPMG), a concept in game theory and algorithmic game theory. It provides an easy-to-use framework for conducting experiments with multiple agents using collusion and cooperation dynamics. This environment is useful for researchers and developers interested in game theory, reinforcement learning, and multi-agent systems.

## Features
- **Customizable Multi-Agent Environment**: Supports different numbers of agents and heterogeneous vs. homogeneous settings.

## Project Structure

```
mpmg/
├── mpmg/                  # Main package directory
│   ├── __init__.py        # Package initialization
│   └── mpmg_env.py        # Environment implementation
├── .gitignore             # Ignored files for git
├── README.md              # Project description and usage guide
├── setup.py               # Installation script
└── LICENSE                # License information
```

## Installation

To install the package locally, run the following command from the root directory:

```sh
pip install mpmg
```

This installs the package in "editable" mode, meaning any changes made in the source code will immediately reflect in the installed package.

## Requirements
- Python 3.6+

## Usage

### Input Parameters
```
num_agents (int): Number of agents. Must be a positive integer, default value is 2.

sigma_beta (float): Heterogeneity level, standard deviation of the power parameters' distribution. Must be in [0,1], default value is 0.

alpha (float): Collusive bid multiplier. Must be > 1.
```

### Methods And Attributes
The `MPMGEnv` class provides methods for resetting the environment, taking steps, and observing the state, rewards, and dynamics of multi-agent interactions.

```
Methods
-------

  reset():
    reset the environment, and returns the initial state
    input: no input
    output: np.ndarray
  
  step(actions):
    returns rewards, next_state and  the done use in episodic task.
    input: List[int]  
    output: (np.ndarray, np.ndarray, bool)

Attributes
----------
num_agents (int): Number of agents.

sigma_beta (float): Heterogeneity level.

alpha (float): Collusive bid multiplier. 

action_size (int): action space size, which is always 2.

joint_action_size (int): action_size ** num_agents, joint action space size.

beta_size (int): num_agents, the size of the beta parameters array.

state_size (int): num_agents + joint_action_size + beta_size. Size of the observation space. May change upon customization of the state space.

state_space: The observation space is composed of 'action_frequencies', 'joint_action_frequencies', and 'beta_parameters', and is of size state_size.

action_frequencies (np.ndarray(num_agents)): action frequencies of action 1 for each player.         

joint_action_frequencies (np.ndarray(joint_action_size)): joint action frequencies for each joint action.
```

Example use:

```python

# import the environment
from mpmg import MPMGEnv

# Create an instance of the environment
env = MPMGEnv(n_agents=2, sigma_beta=0.0, alpha=1.3)

# Reset the environment
state = env.reset() 

# Probably a loop here
for i in range(...):

  # Sample actions
  actions = [1, 0]  # Example of actions array for 2-players

  # Take a step in the environment
  rewards, next_state, done = env.step(actions)
  
  # Do what you need
  ...
  
  # Update state
  state = next_state
```

## Scenarios
`MPMGEnv` is a social dilemma based on the Prisoner's Dilemma. 

- **Full Defection**: All agents choose to defect (action 0), Nash Equilibrium.
- **Full Cooperation**: All agents cooperate (action 1), Pareto Optimal.
- **Asymmetric play**: actions taken can be separated into two sets, other suboptimal outcome.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for improvements, bug fixes, or new features.

## Author

Igor Sadoune - igor.sadoune@polymtl.ca

