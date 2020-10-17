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
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFood = successorGameState.getFood().asList()
        minFoodist = float("inf")
        for food in newFood:
            minFoodist = min(minFoodist, manhattanDistance(newPos, food))

        # avoid ghost if too close
        for ghost in successorGameState.getGhostPositions():
            if (manhattanDistance(newPos, ghost) < 2):
                return -float('inf')
        # reciprocal
        return successorGameState.getScore() + 1.0/minFoodist
        # return successorGameState.getScore();


def scoreEvaluationFunction(currentGameState):
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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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
        """
        depth = 0
        return self.getMaxValue(gameState, depth)[1]

    def getMaxValue(self, gameState, depth, agent=0):
        actions = gameState.getLegalActions(agent)

        if not actions or gameState.isWin() or depth >= self.depth:
            return self.evaluationFunction(gameState), Directions.STOP

        successorCost = float('-inf')
        successorAction = Directions.STOP

        for action in actions:
            successor = gameState.generateSuccessor(agent, action)

            cost = self.getMinValue(successor, depth, agent + 1)[0]

            if cost > successorCost:
                successorCost = cost
                successorAction = action

        return successorCost, successorAction

    def getMinValue(self, gameState, depth, agent):
        actions = gameState.getLegalActions(agent)

        if not actions or gameState.isLose() or depth >= self.depth:
            return self.evaluationFunction(gameState), Directions.STOP

        successorCost = float('inf')
        successorAction = Directions.STOP

        for action in actions:
            successor = gameState.generateSuccessor(agent, action)

            cost = 0

            if agent == gameState.getNumAgents() - 1:
                cost = self.getMaxValue(successor, depth + 1)[0]
            else:
                cost = self.getMinValue(successor, depth, agent + 1)[0]

            if cost < successorCost:
                successorCost = cost
                successorAction = action

        return successorCost, successorAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        """CODE YOUR HERE"""
        depth = 0
        alpha = float('-inf')
        beta = float('inf')
        return self.getMaxValue(gameState, alpha, beta, depth)[1]

    def getMaxValue(self, gameState, alpha, beta, depth, agent=0):
        actions = gameState.getLegalActions(agent)

        if not actions or gameState.isWin() or depth >= self.depth:
            return self.evaluationFunction(gameState), Directions.STOP

        successorCost = float('-inf')
        successorAction = Directions.STOP

        for action in actions:
            successor = gameState.generateSuccessor(agent, action)

            cost = self.getMinValue(
                successor, alpha, beta, depth, agent + 1)[0]

            if cost > successorCost:
                successorCost = cost
                successorAction = action

            if successorCost > beta:
                return successorCost, successorAction

            alpha = max(alpha, successorCost)

        return successorCost, successorAction

    def getMinValue(self, gameState, alpha, beta, depth, agent):
        actions = gameState.getLegalActions(agent)

        if not actions or gameState.isLose() or depth >= self.depth:
            return self.evaluationFunction(gameState), Directions.STOP

        successorCost = float('inf')
        successorAction = Directions.STOP

        for action in actions:
            successor = gameState.generateSuccessor(agent, action)

            cost = 0

            if agent == gameState.getNumAgents() - 1:
                cost = self.getMaxValue(successor, alpha, beta, depth + 1)[0]
            else:
                cost = self.getMinValue(
                    successor, alpha, beta, depth, agent + 1)[0]

            if cost < successorCost:
                successorCost = cost
                successorAction = action

            if successorCost < alpha:
                return successorCost, successorAction

            beta = min(beta, successorCost)

        return successorCost, successorAction


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
        """CODE YOUR HERE"""
        depth = 0
        return self.getMaxValue(gameState, depth)[1]

    def getMaxValue(self, gameState, depth, agent=0):
        actions = gameState.getLegalActions(agent)

        if not actions or gameState.isWin() or depth >= self.depth:
            return self.evaluationFunction(gameState), Directions.STOP

        successorCost = float('-inf')
        successorAction = Directions.STOP

        for action in actions:
            successor = gameState.generateSuccessor(agent, action)

            cost = self.getMinValue(successor, depth, agent + 1)[0]

            if cost > successorCost:
                successorCost = cost
                successorAction = action

        return successorCost, successorAction

    def getMinValue(self, gameState, depth, agent):
        actions = gameState.getLegalActions(agent)

        if not actions or gameState.isLose() or depth >= self.depth:
            return self.evaluationFunction(gameState), None

        successorCosts = []

        for action in actions:
            successor = gameState.generateSuccessor(agent, action)

            cost = 0

            if agent == gameState.getNumAgents() - 1:
                cost = self.getMaxValue(successor, depth + 1)[0]
            else:
                cost = self.getMinValue(successor, depth, agent + 1)[0]

            successorCosts.append(cost)

        return sum(successorCosts) / float(len(successorCosts)), None


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    evalNum = 0
    pacmanPosition = currentGameState.getPacmanPosition()
    foodPositions = currentGameState.getFood().asList()
    minDistance = 10000
    setMinDistance = False
    for foodPosition in foodPositions:
        foodDistance = util.manhattanDistance(pacmanPosition, foodPosition)
        if foodDistance < minDistance:
            minDistance = foodDistance
            setMinDistance = True
    if setMinDistance:
        evalNum += minDistance
    evalNum += 1000*currentGameState.getNumFood()
    evalNum += 10*len(currentGameState.getCapsules())
    ghostPositions = currentGameState.getGhostPositions()
    for ghostPosition in ghostPositions:
        ghostDistance = util.manhattanDistance(pacmanPosition, ghostPosition)
        if ghostDistance < 2:
            evalNum = float('inf')
    evalNum -= 10*currentGameState.getScore()
    # print("min distance: " + str(minDistance) + " num food: " + str(len(foodPositions)) + " eval num: " + str(evalNum*(-1)))
    return evalNum*(-1)


# Abbreviation
better = betterEvaluationFunction
