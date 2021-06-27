from automata.fa.dfa import DFA
# DFA which matches all binary strings ending in an odd number of '1's
dfa = DFA(
    states={'q0', 'q1'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q0'}
    },
    initial_state='q0',
    final_states={'q1','q0'}
)


print(dfa.read_input('0011'))
print(dfa.read_input('00111'))
print(dfa.read_input('001111'))


