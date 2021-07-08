class DistributionAutomaton:
    # default constructor
    # DFA which matches all binary strings ending in an odd number of '1's
    def __init__(self, label=""):
        self.label = label
        self.count = 0

    def get_label(self):
        return self.label

    def label_increase(self):
        self.count = self.count + 1

    def how_many_distributions(self):
        return self.count/10

    def read_decision(self, input=''):
        for ch in input:
            if ch == "1":
                self.label_increase()
        """returns 0 meaning put into train set  (desired size 70%),
                   1 meaning put into dev set    (desired size 10%),
                   or
                   2 meaning put into test set   (desired size 20%)
        """
        state = self.count % 10
        decision = 0
        if state == 1:
            decision = 0
        elif state == 2:
            decision = 1
        elif state == 3:
            decision = 2
        elif state == 4:
            decision = 0
        elif state == 5:
            decision = 2
        else:
            decision = 0
        return decision

    train_decision = 0
    test_decision = 1
    dev_decision = 2


def debug_distribution_automaton():
    autom = DistributionAutomaton()
    autom.label_increase()
    print(autom.read_decision()) # decision: insert into train set
    autom.label_increase()
    print(autom.read_decision()) # decision: insert into dev set
    #equivale a increase+read_decision()
    print(autom.read_decision('1')) # decision: insert into test set
    #insert 7 more to complete the distribution
    print(autom.read_decision('1111111')) # decision: insert into test set
    print("How many distributions were completed?", autom.how_many_distributions())
    return
