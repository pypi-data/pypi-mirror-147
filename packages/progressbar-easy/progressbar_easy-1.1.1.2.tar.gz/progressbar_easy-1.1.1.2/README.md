# Progress Bar
This is a simple progress bar that allows for easy use to display progress.

# Features
- Timer to estimate time remaining
- Timer adjusts to rates
- Learning rate can be changed
- Choice of length of bar
- Choice of character bar is made of
- Option for item count or percentage completed (or both)
- Option for method of computing completion time.

# Installation
Install with pip: `pip install progressbar_easy`

# Usage
Imported with `from progressbar import ProgressBar`

Initialize object with `bar = ProgressBar(number of iterations)`

Use in loop. Inside loop at the end, put `bar.update(K)` or `bar += K` where K is the number of iterations completed since last update.
Prefer `bar.update(K)` if you want to update the bar every iteration.

Defaults to use the Bellman equation to estimate time remaining.
Add `use_average=(True, N)` arguement to use the average of the last N iterations instead of Bellman equation.

Example: `bar = ProgressBar(range(2000), use_average=(True, 420)):`

## Or
Use as an iterator object

```Python
for i in ProgressBar(range(100), lr=.0001):
    ...
```
