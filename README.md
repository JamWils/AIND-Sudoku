# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We've established that each element in a row, column, or square cannot be the same.  With those constraints in mind we can than infer that if there are a pair of twins in a row such as the number 23, then we know that all other elements in that row cannot be 2 or 3.  By eliminating 2 and 3 from the other 7 boxes in that row we are reducing the scope of our search afterwards.  This same theory can then be applied to all columns, square and diagonals that have a pair.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: This constraint was placed at a higher-level than elimination, only choice, and naked twins.  Basically, we can treat the diagonals as another set of units.  By doing this the diagonals are also added to the peers list as well.  This allows us to apply this constraint to all of our different strategies.  For example, when elimination is run we can also eliminate numbers in those diagonal spaces or in the case of 'E5' it will look at both diagonals.  This is because those locations were added to the peers list.  Ultimately, this will help us eliminate more possibilities before the first search is conducted.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.