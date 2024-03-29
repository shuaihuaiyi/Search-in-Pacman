# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu)


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


class Node:
    """
    A container storing the current state of a node, the list 
    of  directions that need to be followed from the start state to
    get to the current state and the specific problem in which the
    node will be used.
    """

    def __init__(self, state, path, cost=0, heuristic=0, problem=None):
        self.state = state
        self.path = path
        self.cost = cost
        self.heuristic = heuristic
        self.problem = problem

    def getSuccessors(self, heuristicFunction=None):
        children = []
        for successor in self.problem.getSuccessors(self.state):
            state = successor[0]
            path = list(self.path)
            path.append(successor[1])
            cost = self.cost + successor[2]
            if heuristicFunction:
                heuristic = heuristicFunction(state, self.problem)
            else:
                heuristic = 0
            node = Node(state, path, cost, heuristic, self.problem)
            children.append(node)
        return children


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def search(problem, func, heuristic=None):
    """The common search function"""
    # initiate closed list and open list
    closedList = []
    if func == "dfs":  # depthFirstSearch
        openList = util.Stack()
    elif func == "bfs":  # breadthFirstSearch
        openList = util.Queue()
    elif func == "ucs" or func == "astar":  # uniformCostSearch or aStarSearch
        openList = util.PriorityQueue()
    else:
        return
    # first step: put start node into open list
    startNode = Node(problem.getStartState(), [], 0, 0, problem)
    if func == "dfs" or func == "bfs":
        openList.push(startNode)
    elif func == "ucs":
        openList.push(startNode, startNode.cost)
    elif func == "astar":
        openList.push(startNode, startNode.cost + startNode.heuristic)
    # loop from step 2 to step 6
    while True:
        if openList.isEmpty():
            return False
        node = openList.pop()
        if problem.isGoalState(node.state):
            return node.path
        if node.state not in closedList:
            closedList.append(node.state)
            for childNode in node.getSuccessors(heuristic):
                if func == "dfs" or func == "bfs":
                    openList.push(childNode)
                elif func == "ucs":
                    openList.push(childNode, childNode.cost)
                elif func == "astar":
                    openList.push(childNode, childNode.cost + childNode.heuristic)


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    """
    return search(problem, "dfs")


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    return search(problem, "bfs")


def uniformCostSearch(problem):
    """Search the node of least total cost first. """
    return search(problem, "ucs")


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    return search(problem, "astar", heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
