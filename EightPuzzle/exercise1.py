from cosc343EightPuzzle import EightPuzzle
import time
import math
# Helper class
class Node:
    def __init__(self, s, parent=None, g=0, h=0, action=None):
        self.s = s # State
        self.parent = parent #Reference to parent node
        self.g = g #cost
        self.f = g + h # Evaluation function
        self.action = action #Action taken from parent nodes state to this node state

# Heuristic function that uses manhattan distance (stolen!!)
def heuristic(s, goal):
    h = 0
    #Walk through all tiles in current state
    for i in range(len(s)):
        # Stolen from Lachlan (2nd year), why do we take the modulus of 3? idkkk
        x_goal = s[i] % 3
        y_goal = math.floor(s[i]/3)
        x_state = i % 3
        y_state = math.floor(i/3)
        # applying Manhattan Distance formula ( |x1 - x2| + |y1 - y2|
        print(x_goal,y_goal,x_state,y_state," :  " , s , " {", s[i], "}")
        h += abs((x_goal - x_state)) + abs((y_goal - y_state))
    return h

# Start time
start_time = time.time()

# Run puzzle
puzzle = EightPuzzle(mode='medium')
init_state = puzzle.reset()
goal_state = puzzle.goal()
# print(init_state)
# print(goal_state)

#Set nodes
root_node = Node(s=init_state, parent=None, g=0, h=heuristic(s=init_state, goal=goal_state))
fringe = [root_node]

# Find solution
solution_node = None
# Store previous states
closed_states = []

#Using informed search pseudocode from lecture
while len(fringe) > 0: #while fringe not empty
    #Thanks to sort at end of while loop, first pop will be the smallest
    current_node = fringe.pop(0)
    current_state = current_node.s

    #Check previous states, continue if found
    if current_state in closed_states:
        continue
    #if goal has been reached, end loop
    if current_state == goal_state:
        solution_node = current_node
        break
    #Find next node
    else:
        # Append currend state to previous states
        closed_states.append(current_state)
        # Copy paste from lab pdf
        available_actions = puzzle.actions(s=current_state)
        for a in available_actions:
            next_state = puzzle.step(s=current_state, a=a)
            #Create new node
            new_node = Node(s=next_state,
                            parent=current_node,
                            g=current_node.g+1,
                            h=heuristic(s=next_state, goal=goal_state),
                            action=a)
            # Store this step
            fringe.append(new_node)
            # why are we sorting
            fringe.sort(key=lambda x: x.f)

# If no solution
if solution_node is None:
    print("No solution found")
# Print solution
else:
    action_sequence = []
    next_node = solution_node
    while True:
        if next_node == root_node:
            break
        action_sequence.append(next_node.action)
        next_node = next_node.parent

    action_sequence.reverse()
    print("Number of moves: %d" % solution_node.g)

# show time
elapsed_time = time.time()-start_time
print("Elapsed time: %.1f seconds" % elapsed_time)
# show puzzle
puzzle.show(s=init_state, a=action_sequence)

# Comments for ex1 and 2
# Easy code took quite fast and 10 moves to solve easy mode
# For medium mode, I waited for 5 mins and it didnt solve it

# Sorting is very good for speed
# Things done to improve speed:
# - Used Manhattan distance instead of shitty provided h+1 heuristic
# - Stored previous states in memory

