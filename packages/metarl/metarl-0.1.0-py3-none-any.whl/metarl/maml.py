import numpy as np

import gym

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class PolicyNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        """
        Initialize the policy network.
        
        Parameters:
        - input_dim: Dimension of the input state.
        - hidden_dim: Dimension of the hidden layer.
        - output_dim: Dimension of the output action.
        """
        super(PolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x, params=None):
        """
        Forward pass through the policy network.
        
        Parameters:
        - x: Input state.
        - params: Optional dictionary of parameters for the inner loop.
        
        Returns:
        - Action probabilities.
        """
        if params is None:
            params = {k: v for k, v in self.named_parameters()}
        
        x = torch.relu(F.linear(x, params['fc1.weight'], params['fc1.bias']))
        x = F.linear(x, params['fc2.weight'], params['fc2.bias'])
        return torch.softmax(x, dim=-1)


class MAMLRL:
    def __init__(self, policy, meta_lr, task_lr, inner_steps=1):
        """
        Initialize the MAML RL class.
        
        Parameters:
        - policy: The policy network to be trained.
        - meta_lr: The learning rate for the meta-optimizer.
        - task_lr: The learning rate for the inner-loop optimizer.
        - inner_steps: Number of gradient descent steps in the inner loop.
        """
        self.policy = policy
        self.meta_optimizer = optim.Adam(self.policy.parameters(), lr=meta_lr)
        self.task_lr = task_lr
        self.inner_steps = inner_steps

    def train_step(self, tasks, device='cpu'):
        """
        Perform one meta-training step.
        
        Parameters:
        - tasks: A list of tasks, where each task is a tuple (env, trajectories).
        - device: Device to run the computations on (e.g., 'cpu' or 'cuda').
        """
        meta_loss = 0.0
        for env, trajectories in tasks:
            # Inner loop: Adapt the policy to the support set
            fast_params = self._inner_loop(env, trajectories[0], device)
            
            # Outer loop: Evaluate the adapted policy on the query set
            query_loss = self._compute_loss(env, trajectories[1], fast_params, device)
            meta_loss += query_loss

        # Meta-update: Update the policy parameters based on the meta-loss
        meta_loss /= len(tasks)
        self.meta_optimizer.zero_grad()
        meta_loss.backward()
        self.meta_optimizer.step()

    def _inner_loop(self, env, trajectories, device):
        """
        Perform the inner loop adaptation.
        
        Parameters:
        - env: The environment for the current task.
        - trajectories: Trajectories from the support set.
        - device: Device to run the computations on (e.g., 'cpu' or 'cuda').
        
        Returns:
        - fast_params: Updated parameters after inner loop adaptation.
        """
        fast_params = {k: v.clone() for k, v in self.policy.named_parameters()}
        
        for _ in range(self.inner_steps):
            loss = self._compute_loss(env, trajectories, fast_params, device)
            grads = torch.autograd.grad(loss, fast_params.values(), create_graph=True)
            fast_params = {k: v - self.task_lr * grad for k, v, grad in zip(fast_params.keys(), fast_params.values(), grads)}
        
        return fast_params

    def _compute_loss(self, env, trajectories, params, device):
        """
        Compute the loss for a set of trajectories.
        
        Parameters:
        - env: The environment for the current task.
        - trajectories: List of trajectories.
        - params: Parameters to use for the policy.
        - device: Device to run the computations on (e.g., 'cpu' or 'cuda').
        
        Returns:
        - loss: The computed loss.
        """
        states, actions, rewards = zip(*trajectories)
        states = torch.tensor(states, dtype=torch.float32).to(device)
        actions = torch.tensor(actions, dtype=torch.int64).to(device)
        rewards = torch.tensor(rewards, dtype=torch.float32).to(device)
        
        action_probs = self.policy(states, params)
        log_probs = torch.log(action_probs.gather(1, actions.unsqueeze(1)).squeeze())
        loss = -(log_probs * rewards).mean()
        return loss

    def collect_trajectories(self, env, num_episodes, params=None, device='cpu'):
        """
        Collect trajectories from the environment.
        
        Parameters:
        - env: The environment.
        - num_episodes: Number of episodes to collect.
        - params: Parameters to use for the policy.
        - device: Device to run the computations on (e.g., 'cpu' or 'cuda').
        
        Returns:
        - trajectories: List of collected trajectories.
        """
        trajectories = []
        for _ in range(num_episodes):
            state, _ = env.reset()
            done = False
            episode = []
            while not done:
                state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)
                action_probs = self.policy(state_tensor, params)
                action = torch.multinomial(action_probs, 1).item()
                next_state, reward, done, _, _ = env.step(action)
                episode.append((state, action, reward))
                state = next_state
            trajectories.append(episode)
        return trajectories


def example():
    # Hyperparameters
    input_dim = 4
    hidden_dim = 128
    output_dim = 2
    meta_lr = 0.001
    task_lr = 0.1
    inner_steps = 1
    num_tasks = 2
    num_episodes_per_task = 2
    num_epochs = 100

    # Create a policy network
    policy = PolicyNetwork(input_dim, hidden_dim, output_dim)

    # Create a MAML RL instance
    maml_rl = MAMLRL(policy, meta_lr, task_lr, inner_steps)

    # Generate some dummy tasks
    tasks = []
    for _ in range(num_tasks):
        env = gym.make('CartPole-v1')
        support_trajectories = maml_rl.collect_trajectories(env, num_episodes_per_task)
        query_trajectories = maml_rl.collect_trajectories(env, num_episodes_per_task)
        tasks.append((env, (support_trajectories, query_trajectories)))

    # Train the policy
    for epoch in range(num_epochs):
        maml_rl.train_step(tasks)
        if epoch % 10 == 0:
            # Evaluate the policy on the tasks
            total_rewards = 0
            for env, (_, query_trajectories) in tasks:
                for trajectory in query_trajectories:
                    total_rewards += sum([reward for _, _, reward in trajectory])
            avg_reward = total_rewards / (num_tasks * num_episodes_per_task)
            print(f"Epoch {epoch}, Average Reward: {avg_reward:.4f}")

    # Final evaluation
    total_rewards = 0
    for env, (_, query_trajectories) in tasks:
        for trajectory in query_trajectories:
            total_rewards += sum([reward for _, _, reward in trajectory])
    final_avg_reward = total_rewards / (num_tasks * num_episodes_per_task)
    print(f"Final Average Reward: {final_avg_reward:.4f}")
