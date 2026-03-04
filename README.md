This project has been created as part of the 42 curriculum by _obakri_, _ikabboud_

# A_MAZE_ING
## Description
a_maze_ing is a project that aims to create an interactive maze and pathfinding visualization tool built from scratch using python programming language and minilibx library .The project demonstrates advanced algorithm implementation, low-level graphics programming, and real-time animation rendering.

### maze generation algorithms :

for the maze generation , we used two :
- **Wilson**'s Algorithm generates mazes through loop-erased random walks, where you perform a random walk from an unvisited cell until hitting the existing maze, then erase any loops the path created by crossing itself. This produces completely unbiased mazes where all possible configurations are equally likely, unlike DFS which favors long corridors. It's slower but guarantees perfect uniformity in maze generation.

- **dfs** : Depth-First Search generates mazes by exploring paths as deeply as possible before backtracking. It picks random unvisited neighbors, removes walls between cells, and uses a stack to backtrack when stuck, creating a perfect maze with long winding corridors. It's fast (O(n)), simple to implement, and widely used in maze-based games.

By default we're using dfs algorithm to generate the maze, and then the user can switch to wilson algorithm by clicking the button 'change algorithm'

### reusable part of my code :


### the roles of each member team :

_ikkaboud_ : was responsible of implementing the algorithm of dfs, bfs and wilson , and also she handeled the perfect / unperfect maze , and output file generation .

_obakri_ : was responsible of the graphical interface using minilibx , also config file parsing and generating makefile and this readme file

## Instructions


## Resources
