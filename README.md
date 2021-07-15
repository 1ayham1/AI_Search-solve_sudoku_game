# Solve-a-Sudoku-with-AI
Project 1: Udacity Artificial Intelligence and Specializations Nanodegree Program

# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: 

The first step involves locating Naked Twins (NT) boxes. Originally, Suduko values are stored in a dictionary whose keys are the boxes and values of possible solution candidates; i.e. {'A1':'123456789'}. If a given box contains (NT) candidates in its peers, then they should contain the same value. Ex: {'A1': '23'}, {'A7', '23'}. To capture this issue, I utilized a reverse dictionary implementation so that the key will be unique NT candidate while the value is going to store the boxes they belong to.  (http://stackoverflow.com/questions/20672238/find-dictionary-keys-with-duplicate-values)
  
After proprly determining all candidate NT locations,every NT location needs to be associated with its proper file. i.e. do they belong to the same rwo, col, or diagonal. This is very important for the elimination step so that corrosponding values are deleted from the right place.
Finally, a proper call to this function is to be placed in reduce_puzzle_ function, after applying the elimination step as well as removing values using only_choice. Doing so, will allow propagating the constrain to other boxes especially after the recursive call done by the search function. The overall effect is reducing the search space       



# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  

A: 
I only needed to define the two main diagonals (left_Diag, right_Diag) at the beginning and then add them to the unitlist and peers. Everything else was straight forward and already included in every check for a given box peers.  





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