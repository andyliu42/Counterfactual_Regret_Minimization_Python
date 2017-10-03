import random
import matplotlib.pyplot as plt

ROCK = 0
PAPER = 1
SCISSORS = 2
NUM_ACTIONS = 3

# Player 1
P1regretSum = [0.0] * NUM_ACTIONS
P1strategy = [0.0] * NUM_ACTIONS
P1strategySum = [0.0] * NUM_ACTIONS

# Player 2
P2regretSum = [0.0] * NUM_ACTIONS
P2strategy = [0.0] * NUM_ACTIONS
P2strategySum = [0.0] * NUM_ACTIONS

def getStrategy(regretSum, strategy):
    normalizingSum = 0.0
    for a in range(NUM_ACTIONS):
        if regretSum[a] > 0:
            strategy[a] = regretSum[a]
        else:
            strategy[a] = 0
        normalizingSum += strategy[a]
    for a in range(NUM_ACTIONS):
        if normalizingSum > 0:
            strategy[a] /= normalizingSum
        else:
            strategy[a] = 1.0 / NUM_ACTIONS
        normalizingSum += strategy[a]
    return strategy

def getAction(strategy):
    r = random.random()
    a = 0
    cumulativeProbability = 0.0
    while a < NUM_ACTIONS - 1:
        cumulativeProbability += strategy[a]
        if r < cumulativeProbability:
            break
        a += 1
    return a

def train(iterations, P1strategy, P2strategy):
    P1actionUtility = [0.0] * NUM_ACTIONS
    P2actionUtility = [0.0] * NUM_ACTIONS
    for i in range(iterations):
        # get regret-matched mixed-strategy actions
        P1strategy = getStrategy(P1regretSum, P1strategy)
        P2strategy = getStrategy(P2regretSum, P2strategy)
        P1Action = getAction(P1strategy)
        P2Action = getAction(P2strategy)
        
        # compute action utilities
        P1actionUtility[P2Action] = 0
        if P2Action == NUM_ACTIONS - 1:
            P1actionUtility[0] = 1
        else:
            P1actionUtility[P2Action + 1] = 1
        if P2Action == 0:
            P1actionUtility[NUM_ACTIONS - 1] = -1
        else:
            P1actionUtility[P2Action - 1] = -1
            
        P2actionUtility[P1Action] = 0
        if P1Action == NUM_ACTIONS - 1:
            P2actionUtility[0] = 1
        else:
            P2actionUtility[P1Action + 1] = 1
        if P1Action == 0:
            P2actionUtility[NUM_ACTIONS - 1] = -1
        else:
            P2actionUtility[P1Action - 1] = -1
            
        # accumulate action regrets
        for a in range(NUM_ACTIONS):
            P1regretSum[a] += P1actionUtility[a] - P1actionUtility[P1Action]
            P2regretSum[a] += P2actionUtility[a] - P2actionUtility[P2Action]

def getAverageStrategy(strategySum, strategy):
    avgStrategy = [0.0] * NUM_ACTIONS
    normalizingSum = 0.0
    for a in range(NUM_ACTIONS):
        normalizingSum += strategySum[a]
    for a in range(NUM_ACTIONS):
        if normalizingSum > 0:
            avgStrategy[a] = strategySum[a] / normalizingSum
        else:
            avgStrategy[a] = 1.0 / NUM_ACTIONS
        strategySum[a] += strategy[a]
    return avgStrategy

if __name__ == "__main__":
    P1result = []
    P2result = []
    for i in range(1000):
        train(1, P1strategy, P2strategy)
        # print(getStrategy())
        print("P1 strategy:", getAverageStrategy(P1strategySum, P1strategy))
        print("P2 strategy:", getAverageStrategy(P2strategySum, P2strategy))
        P1result.append(getAverageStrategy(P1strategySum, P1strategy))
        P2result.append(getAverageStrategy(P2strategySum, P2strategy))
    plt.plot(P1result)
    plt.ylabel('P1 Probability')
    plt.show()
    plt.plot(P2result)
    plt.ylabel('P2 Probability')
    plt.show()
