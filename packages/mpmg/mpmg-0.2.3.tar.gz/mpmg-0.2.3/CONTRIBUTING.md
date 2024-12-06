# For Potential Contributors
If you want to contribute to the project please make sure to read the following paper: https://arxiv.org/abs/2407.03521, as well as the project README.md. Then, please contact me (igor.sadoune@polymtl.ca).

Feel free to suggest any improvements or new features, I am open to any relevant improvement.

## Project Structure

```
mpmg/
├── mpmg/                  # Main package directory
│   ├── __init__.py        # Package initialization
│   └── mpmg_env.py        # Environment implementation
├── .gitignore             # Ignored files for git
├── README.md              # Project description and usage guide
├── MANIFEST.in            # Includes support files 
├── setup.py               # Installation script
└── LICENSE                # License information
```

## Contribution Avenues

There are many ways the MPMG can be enhanced, the end goal being to reach a realistic full-scale simulation. However, here are three potential improvements that I have in mind.  

### Dynamic Beta Parameters
Beta parameters represent agents' power (or market shares if we think of the MPMG as a market). When those parameters differ from agent ot agent, the game is heterogeneous. Having dynamic beta values that change overtime and according to the current game's state brings an element of dynamic allowing agent to grow or to weaken in strength.

Such feature should be implemented in mpmg/mpmg_env.py in the MPMGEnv class:

```python
def _update_beta(self) -> None:
    '''
    Placeholder method for future beta parameter updates.
    '''
    pass
```
and integrated to the flow of the `step()` method. Power parameters are currently initialized using 

```python
def _get_power_parameters(self) -> None:
    '''
    Generates market shares as power parameters based on market heterogeneity.
    '''
    # Homogeneous agents
    if self.sigma_beta == 0:
        self.beta_parameters = np.ones(self.num_agents) / self.num_agents
    # Heterogeneous agents
    else:
        beta = np.abs(np.random.normal(1 / self.num_agents, self.sigma_beta, self.num_agents))
        self.beta_parameters = beta / np.sum(beta)
```
which should be renamed as `_get_initial_power_parameters()` in such case.

### Bigger Observation Space
The observation space is defined in (mpmg/mpmg_env.py, MPMGEnv class)
```python
    def __init__(
        self, 
        num_agents: int = 2, 
        sigma_beta: float = 0.0, 
        alpha: float = 1.3
    ):

        # Validate num_agents
        if not isinstance(num_agents, int) or num_agents <= 0:
            raise ValueError(f'num_agents must be a positive integer, not {num_agents}.')
        self.num_agents = num_agents

        # Validate sigma_beta
        if not isinstance(sigma_beta, (float, int)) or not (0 <= sigma_beta <= 1):
            raise ValueError(f'sigma_beta must be a float in the range [0, 1], not {sigma_beta}.')
        self.sigma_beta = sigma_beta

        # Validate alpha
        if not isinstance(alpha, (float, int)) or alpha <= 1:
            raise ValueError(f'alpha must be a float greater than 1, not {alpha}.')
        self.alpha = alpha

        # Internal state action variables
        self.action_size = 2
        self.joint_action_size = self.action_size ** self.num_agents
        self.beta_size = self.num_agents
        self.state_size = self.num_agents + self.joint_action_size + self.beta_size
        self.state_space = {
            'action_frequencies': None,
            'joint_action_frequencies': None,
            'beta_parameters': None
        }
```
and updated by 

```python
    def _get_state(self) -> np.ndarray:
        '''
        Observation space can be incremented here.
        '''
        self.state_space['action_frequencies'] = self.action_frequencies
        self.state_space['joint_action_frequencies'] = self.joint_action_frequencies
        self.state_space['beta_parameters'] = self.beta_parameters
        # To extend the state space
        # self.state_space['additional_variable'] = self.additional_variable
        return np.concatenate([v.flatten() for v in self.state_space.values()])
```
in the same class. Both needs to be modified upon chanegs to the observation space, and additional methods might be needed to support your idea.

### Continuous Action Space
Adding a game version with continuous action space should involve a new class `MPMGContinuousEnv`, in a new file `mpmg_continuous_env.py`, so that the continuous implementation is contained in its own thread. Users could then potentially use both by importing those class from the main `mpmg` directory.

The continuous action space could be convexe (e.g., [0,1]) or non-convexe using continuous and separate ranges, depending on what you want to implement.  

## Project Integrity and Coding Convention
Upon request, I would make you contributor of the project. Your contribution must be developed on a separate branch as you would not have access to the master banch. I would be the one to review the associated Pull Request.

please respect Python conventions for private and public methods and attributes, as well as naming conventions for code portability. Also, please use Typing for further clarity and portability. 

To contribute to the MPMG project, please follow these steps:

1. **Fork** the repository to your GitHub account.
2. **Clone** your fork to your local machine.
3. Create a new **branch** for your contribution (`git checkout -b feature-new-observation-space`).
4. Implement your changes, making sure to follow the coding conventions outlined below.
5. **Add tests** to validate your changes, if applicable.
6. Push your branch to your fork and submit a **pull request** to the main repository.
7. Provide a detailed description of your changes in the pull request, referencing any related issues.

## Testing and Validation

Before submitting your changes, make sure to:

- If your changes introduce new functionality, **add unit tests** to validate your implementation.
- Use consistent **naming conventions** and **typing** to keep the codebase clean and readable.

## Author 
Igor Sadoune - igor.sadoune@polymtl.ca
