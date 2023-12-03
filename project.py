from queue import Queue
class lambda_NFA:
    def __init__(self, Q, sigma, initial_state, accepting_states, all_transition):
        self.Q = Q
        self.sigma = []
        self.sigma = sigma
        self.initial_state = initial_state
        self.accepting_states = []
        self.accepting_states = accepting_states
        self.all_transitions = [[[]]]
        self.all_transitions = all_transition
        
    
    def delta_star(self, q, x):
        current = Queue()
        current.put(q)
        result = []
        was_checked = [False for i in range(self.Q)]
        was_checked[q] = True
        while not(current.empty()):
            state = current.get()
            for j in range(self.Q):
                if self.all_transitions[state][j].count(x) != 0:
                    result.append(j)
                elif self.all_transitions[state][j].count('$') != 0 and was_checked[j] == False:
                    current.put(j)
                    was_checked[j] = True
                    if state == int(self.initial_state) and self.accepting_states.count(str(j)) != 0 and self.accepting_states.count(self.initial_state) == 0:
                        self.accepting_states.append(self.initial_state)  
            
        resultQ = Queue()
        for element in result:
            resultQ.put(element)
            
        while not(resultQ.empty()):
            state = resultQ.get()
            
            for i in range(self.Q):
                if self.all_transitions[state][i].count('$') >= 1:
                    result.append(i)
                    resultQ.put(i)
        return result                        
    
    
    def convert_to_NFA(self):
        new_transitions = [[[None for k in range(self.Q)]for i in range(self.Q)]for j in range(self.Q)]
        for q in range(self.Q):
            for alpha in self.sigma:
                new_transition = self.delta_star(q, alpha)
                for target in new_transition:
                    new_transitions[q][target].append(alpha)
        self.all_transitions = new_transitions
    
    
    def convert_to_DFA(self):
        current = Queue()
        trash = [self.Q]
        states = []
        states.append([int(self.initial_state)])
        moves = []
        q = int(self.initial_state)
        current.put([q])
        while not(current.empty()):
            before = current.get()
            for x in self.sigma:
                after = []
                for j in before:
                    for i in range(self.Q):
                        if self.all_transitions[int(j)][int(i)].count(x) != 0 and after.count(i) == 0:
                            after.append(i)
                found = 0            
                for state in states:
                    if len(state) == len(after):
                        found = 1
                        for i in state:
                            if after.count(i) == 0:
                                found = 0
                                break
                        if found == 1:
                            break
                if found != 1 and len(after) != 0:
                    states.append(after)
                    current.put(after)        
                            
                if len(after) != 0:
                    moves.append([before, x, after])
                else:
                    moves.append([before, x, trash])
        states.append(trash)
        new_accepting = []
        for state in states:
            for i in self.accepting_states:
                if state.count(int(i)) != 0:
                    new_accepting.append(state)
                    break
        self.accepting_states = new_accepting                            
        return moves, states 
    
    
    def find_string(self, moves, str):
        state = [int(self.initial_state)]
        if str == '$':
            if self.accepting_states.count(state) != 0:
                result = 'Yes'
            else:
                result = 'No'
            return result             
        
        for i in str:
            if self.sigma.count(i) == 0:
                result = 'No'
                return result
            for move in moves:
                if move[0] == state and move[1] == i:
                   state = move[2]
                   #print(move)
                   break           
        
        if self.accepting_states.count(state) != 0:
            result = 'Yes'
        else:
            result = 'No'
        return result                            


in_list = []
in_list = list(map(int, input().strip().split()))

n = in_list[0]
s = in_list[1]
a = in_list[2]
d = in_list[3]
test_case = in_list[4]

sigma = []
for i in range(s):
    c = input()
    sigma.append(c)
initial_state = input()
accepting_states = []
for i in range(a):
    c = input()
    accepting_states.append(c)
all_transitions = [[[None for k in range(s)]for i in range(n)]for j in range(n)]
for i in range(d):
    in_list = []
    in_list = list(map(str, input().strip().split()))
    w = in_list[0]
    e = in_list[1]
    r = in_list[2]
    
    all_transitions[int(w)][int(r)].append(e)  
    
l_NFA = lambda_NFA(n, sigma, initial_state, accepting_states, all_transitions)

l_NFA.convert_to_NFA()
                
moves, states = l_NFA.convert_to_DFA()

result = []                         
for i in range(test_case):
    str = input()
    ans = l_NFA.find_string(moves, str)
    result.append(ans)  

for ans in result:
    print(ans)                                              
                    
                                      