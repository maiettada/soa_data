class DistributionAutomaton:
    # default constructor
    # DFA which matches all binary strings ending in an odd number of '1's
    def __init__(self, label=""):
        self.label = label
        self.count = 0
        self.used = False

    train_decision = 0
    test_decision = 2
    dev_decision = 1

    def get_label(self):
        return self.label

    def label_increase(self):
        self.used = True
        self.count = self.count + 1

    def is_it_used(self):
        return self.used

    def how_many_distributions(self):
        return self.count/10

    def read_decision(self, input: int = 0):
        """
        Outputs a decision of the automaton

        :param input:
        :return:    0 ("train_decision"), meaning put into train set  (desired size 70%),
                    1 ("dev_decision") , meaning put into dev set    (desired size 10%),
                    2 ("test_decision"), meaning put into test set   (desired size 20%)


        :rtype: object
        """
        for i in range(input):
            self.label_increase()
        state = self.count % 10
        decision = 0
        if state == 1:
            decision = 2
        elif state == 2:
            decision = 2
        elif state == 3:
            decision = 1
        else:
            decision = 0
        return decision


def debug_distribution_automaton():
    autom = DistributionAutomaton()
    autom.label_increase()
    print(autom.read_decision()) # decision: insert into train set
    autom.label_increase()
    print(autom.read_decision()) # decision: insert into dev set
    #equivale a increase+read_decision()
    print(autom.read_decision(1)) # decision: insert into test set
    #insert 7 more to complete the distribution
    print(autom.read_decision(7)) # decision: insert into train set
    print("How many distributions were completed?", autom.how_many_distributions())
    return
