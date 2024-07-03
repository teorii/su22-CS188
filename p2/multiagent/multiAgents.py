# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        inf = float("inf")
        foodLoc = []
        for xPos in range (newFood.width):
            for yPos in range (newFood.height):
                if newFood[xPos][yPos] == True:
                    foodLoc.append((xPos, yPos))
        foodDifferential = [manhattanDistance(i, newPos) for i in foodLoc]

        if successorGameState.getNumFood() == 0:
            return inf

        for i in newGhostStates:
            if manhattanDistance(i.getPosition(), newPos) < 3:
                return -inf
        
        return 2*successorGameState.getScore() - (min(foodDifferential)) - successorGameState.getNumFood()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        val, accion = self.minimax(gameState, self.index, 0)  
        return accion

    def minimax(self, gameState: GameState, agent, depth):
        if depth == self.depth and agent >= gameState.getNumAgents():
            currEval = self.evaluationFunction(gameState)
            return currEval, None
        return self.minimaxHelper(gameState, agent % gameState.getNumAgents(), depth)

    def minimaxHelper(self, gameState: GameState, agent, depth):
        # checking
        posActions = []
        for action in gameState.getLegalActions(agent):
            nextState = gameState.generateSuccessor(agent, action)
            posActions.append((nextState, action))
        if len(posActions) == 0:
            currEval = self.evaluationFunction(gameState)
            return currEval, None

        # pac and spooks
        inf = float("inf")
        opAction = None
        if agent == 0:
            currVal = -inf
            for accion in posActions:
                nextVal = self.minimax(accion[0], agent + 1, depth + 1)[0]
                if nextVal > currVal:
                    currVal = nextVal
                    opAction = accion[1]
        else:
            currVal = inf
            for accion in posActions:
                nextVal = self.minimax(accion[0], agent + 1, depth)[0]
                if nextVal < currVal:
                    currVal = nextVal
                    opAction = accion[1]
        return currVal, opAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        inf = float("inf")
        val, accion = self.alphaBeta(gameState, self.index, 0, -inf, inf)  
        return accion

    def alphaBeta(self, gameState: GameState, agent, depth, alpha, beta):
        if agent == gameState.getNumAgents():
            agent = 0
            depth += 1
        if depth == self.depth:
            currEval = self.evaluationFunction(gameState)
            return currEval, None
        return self.alphaBetaHelper(gameState, agent, depth, alpha, beta)

    def alphaBetaHelper(self, gameState: GameState, agent, depth, alpha, beta):
        # checking
        actions = gameState.getLegalActions(agent)
        if len(actions) == 0:
            return self.evaluationFunction(gameState), None

        # pac and spooks
        inf = float("inf")
        opAction = None
        if agent == 0:
            value = -inf
            for action in actions:
                nextState = gameState.generateSuccessor(agent, action)
                nextValue, _ = self.alphaBeta(nextState, agent + 1, depth, alpha, beta)
                if nextValue > value:
                    value = nextValue
                    opAction = action
                if value > beta:
                    return value, opAction
                alpha = max(alpha, value)
        else:
            value = inf
            for action in actions:
                nextState = gameState.generateSuccessor(agent, action)
                nextValue, _ = self.alphaBeta(nextState, agent + 1, depth, alpha, beta)
                if nextValue < value:
                    value = nextValue
                    opAction = action
                if value < alpha:
                    return value, opAction
                beta = min(beta, value)
        return value, opAction 


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        max, accion = self.expectimax(gameState, self.index, 0)
        return accion

    def expectimax(self, gameState: GameState, agent, depth):
        if agent == gameState.getNumAgents():
            agent = 0
            depth += 1
        if depth == self.depth:
            currEval = self.evaluationFunction(gameState)
            return currEval, None
        return self.expectimaxHelper(gameState, agent, depth)

    def expectimaxHelper(self, gameState: GameState, agent, depth):
        # checking
        actions = gameState.getLegalActions(agent)
        if len(actions) == 0:
            return self.evaluationFunction(gameState), None

        # pac and spooks
        inf = float("inf")
        opAction = None
        if agent == 0:
            value = -inf
            for action in actions:
                nextState = gameState.generateSuccessor(agent, action)
                nextValue, _ = self.expectimax(nextState, agent + 1, depth)
                if nextValue > value:
                    value = nextValue
                    opAction = action
        else:
            value = 0
            for action in actions:
                nextState = gameState.generateSuccessor(agent, action)
                nextValue, _ = self.expectimax(nextState, agent + 1, depth)
                value += nextValue / len(actions)
            opAction = actions[0]
                
        return value, opAction


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()

    for i in newGhostStates:
        if manhattanDistance(i.getPosition(), newPos) < 4:
            return -1
    
    foodLoc = []
    for xPos in range (newFood.width):
        for yPos in range (newFood.height):
            if newFood[xPos][yPos] == True:
                foodLoc.append((xPos, yPos))
    foodDifferential = [manhattanDistance(loc, newPos) for loc in foodLoc]

    if min([ghost.scaredTimer for ghost in newGhostStates], default=0) == 0:
        scaredGhosts = 0
    else:
        scaredGhosts = min([ghost.scaredTimer for ghost in newGhostStates])
    
    return 1.25*currentGameState.getScore() - (min(foodDifferential, default=-1)) - currentGameState.getNumFood() + 2*scaredGhosts

# Abbreviation
better = betterEvaluationFunction