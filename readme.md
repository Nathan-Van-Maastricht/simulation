# Simulator

This repo has multiple goals, but is ultimately just an experiment for my own education.

## Multiagent RL
Having experimented with single agent RL in the past, I thought it would be fun to learn about multiple agent environments, with both competing and cooperative agents, with various parameters for each agent in the system.

## Graphics
Having mostly been a research analyst I haven't had need to visualise complex environments before, and have managed to get away without learning too much. I want to learn at least a small amount of GL, and this project serves a good spot to learn it, even if it is just dots on a screen.

## Improvements
Over time, I will add more complexity to the simulator at a base level, and instead of using bad heuristics for the decision making over the agents, instead torch will be used to give them a relatively shallow net, and they will be trained over many simulator runs using RL, likely just REINFORCE, although we will see how that develops.