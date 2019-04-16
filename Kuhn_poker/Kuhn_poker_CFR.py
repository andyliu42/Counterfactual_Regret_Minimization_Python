import random

# Experiment parameters
numOfCards = 3
trainIteration = 10000
displaySize = 1000

# Game parameters
PASS = 0
BET = 1
numOfActions = 2

nodeMap = dict()

class Node():
    def __init__(self):
        self.infoSet = ""
        self.regretSum = [0.0] * numOfActions
        self.strategy = [0.0] * numOfActions
        self.strategySum = [0.0] * numOfActions

    def getStrategy(self, realizationWeight):
        normalizingSum = 0.0
        for a in range(numOfActions):
            self.strategy[a] = self.regretSum[a] if self.regretSum[a] > 0 else 0
            normalizingSum += self.strategy[a]
        for a in range(numOfActions):
            if normalizingSum > 0:
                self.strategy[a] /= normalizingSum
            else:
                self.strategy[a] = 1.0 / numOfActions
            self.strategySum[a] += realizationWeight * self.strategy[a]
        return self.strategy

    def getAverageStrategy(self):
        avgStrategy = [0.0] * numOfActions
        normalizingSum = 0.0
        for a in range(numOfActions):
            normalizingSum += self.strategySum[a]
        for a in range(numOfActions):
            if normalizingSum > 0:
                avgStrategy[a] = self.strategySum[a] / normalizingSum
            else:
                avgStrategy[a] = 1.0 / numOfActions
        return avgStrategy

    def getInfo(self):
        return self.infoSet + ":" + ",".join(str(round(x,2)) for x in self.getAverageStrategy())
        
def cfr(cards, history, p0, p1):
    plays = len(history)
    player = plays % 2
    opponent = 1 - player
    
    # Return payoff for terminal states
    if plays > 1:
        terminalPass = (history[plays - 1] == 'p')
        doubleBet = (history[plays - 2:plays] == "bb")
        isPlayerCardHigher = (cards[player] > cards[opponent])
        if terminalPass:
            if history == "pp":
                return 1 if isPlayerCardHigher else -1
            else:
                return 1
        elif doubleBet:
            return 2 if isPlayerCardHigher else -2
            
    infoSet = str(cards[player]) + history
    
    # Get info set node or create it if nonexitant
    node = nodeMap.get(infoSet)
    if node == None:
        node = Node()
        node.infoSet = infoSet
        nodeMap[infoSet] = node
    
    # For each action, recursively call cfr with additional history and probability
    if player == 0:
        strategy = node.getStrategy(p0)
    else:
        strategy = node.getStrategy(p1)
        
    util = [0.0] * numOfActions
    nodeUtil = 0
    for a in range(numOfActions):
        if a == 0:
            nextHistory = history + "p"
        else:
            nextHistory = history + "b"
        
        if player == 0:
            util[a] = -cfr(cards, nextHistory, p0 * strategy[a], p1)
        else:
            util[a] = -cfr(cards, nextHistory, p0, p1 * strategy[a])
        nodeUtil += strategy[a] * util[a]
    
    # For each action, compute and accumulate counterfactual regretSum
    for a in range(numOfActions):
        regret = util[a] - nodeUtil
        node.regretSum[a] += (p1 if player == 0 else p0) * regret
    
    return nodeUtil

def train(iterations):
    cards = []
    for i in range(numOfCards):
        cards.append(i + 1)
        
    util = 0.0
    for i in range(iterations):
        # Shuffle cards
        for c1 in range(len(cards) - 1, -1, -1):
            c2 = random.randint(0, c1)
            temp = cards[c1]
            cards[c1] = cards[c2]
            cards[c2] = temp
        util += cfr(cards, "", 1, 1)

        if (i + 1) % displaySize == 0:
            print("\n\nRound #", i + 1, ", Cards:", cards, "Average game value: ", util / iterations)

            # Node traversal
            for node in nodeMap:
                print(nodeMap[node].getInfo(), end = '; ')

if __name__ == "__main__":
    train(trainIteration)
