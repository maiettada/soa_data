from automata.fa.dfa import DFA


class Distribution_automaton:
    # default constructor
    # DFA which matches all binary strings ending in an odd number of '1's
    def __init__(self, label=""):
        self.dfa = DFA(
    states={'q0', 'q1'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q0'}
    },
    initial_state='q0',
    final_states={'q1','q0'}
)

    def read_decision(self, input=''):
        """returns 0 meaning put into train set  (desired size 70%),
                   1 meaning put into dev set    (desired size 10%),
                   or
                   2 meaning put into test set   (desired size 20%)
        """
        state = self.dfa.read_input(input)
        decision = 0
        if state == 'q0':
            decision = 0
        elif state == 'q1':
            decision = 1
        elif state == 'q2':
            decision = 2
        return decision


autom = Distribution_automaton()

print(autom.read_decision())
print(autom.read_decision('00111'))
print(autom.read_decision('001111'))


