# Pong with Q-Learning

Train agent using state - action method, where state is 1, 0 or -1 representing if the player is above, same level or below the ball's y-coordinate. Action represents a string, either moving "UP", "DOWN", or "NOTHING".

For each `q[state, action]` a q-value or reward is saved for this event.

The agent plays against itself for n rounds, then the Human gets to play against it.


## Installation

1. Clone repo

3. Install python compiler if not already installed using your package manager. Example for Fedora run `sudo dnf install python3`

2. Install pygame library, example using pip `pip3 install pygame`

3. run `python3 play.py`

Modify the training sessions `n` to your desire in /play.py line 3:`train(n)`
