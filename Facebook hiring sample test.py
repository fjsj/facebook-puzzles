'''
Facebook hiring sample test

There are K pegs. Each peg can hold discs in decreasing order of radius when looked from bottom to top of the peg. There are N discs which have radius 1 to N; Given the initial configuration of the pegs and the final configuration of the pegs, output the moves required to transform from the initial to final configuration. You are required to do the transformations in minimal number of moves.

A move consists of picking the topmost disc of any one of the pegs and placing it on top of anyother peg.
At anypoint of time, the decreasing radius property of all the pegs must be maintained.

Constraints:
1<= N<=8
3<= K<=5

Input Format:
N K
2nd line contains N integers.
Each integer in the second line is in the range 1 to K where the i-th integer denotes the peg to which disc of radius i is present in the initial configuration.
3rd line denotes the final configuration in a format similar to the initial configuration.

Output Format:
The first line contains M - The minimal number of moves required to complete the transformation. 
The following M lines describe a move, by a peg number to pick from and a peg number to place on.
If there are more than one solutions, it's sufficient to output any one of them. You can assume, there is always a solution with less than 7 moves and the initial confirguration will not be same as the final one.

Sample Input #00:
 
2 3
1 1
2 2

Sample Output #00:
 
3
1 3
1 2
3 2

Sample Input #01:

6 4
4 2 4 3 1 1
1 1 1 1 1 1

Sample Output #01:

5
3 1
4 3
4 1
2 1
3 1

NOTE: You need to write the full code taking all inputs are from stdin and outputs to stdout 
If you are using "Java", the classname is "Solution"
'''

import sys
import itertools
from collections import deque

class Node(object):
    def __init__(self, parent, last_move, config_str):
        self.parent = parent
        self.last_move = last_move
        self.config_str = config_str
    
    def next_configs(self, k_pegs, permutations):
        pegs = config_to_pegs(self.config_str, k_pegs)
        nexts = []

        for frm, to in permutations:
            if pegs[frm] != [] and (pegs[to] == [] or pegs[frm][-1] < pegs[to][-1]):
                moved = pegs[frm][-1]
                next = self.config_str.split(' ')
                next[moved - 1] = str(to + 1)
                nexts.append(Node(self, (frm + 1, to + 1), " ".join(next)))

        return nexts
    
    def __hash__(self):
        return hash(self.config_str)
    
    def __eq__(self, other):
        return self.config_str == other.config_str

def config_to_pegs(config_str, n_pegs):
    config = [int(x) for x in config_str.split(' ')]
    pegs = [[] for _ in range(n_pegs)]
    ints = range(1, len(config) + 1)
    for i in reversed(range(len(config))):
        pegs[config[i] - 1].append(ints[i])
    return pegs

def pegs_to_config(pegs):
    config = [None] * len(pegs)
    for i in range(len(pegs)):
        peg = pegs[i]
        for x in peg:
            config[x - 1] = i + 1
    return " ".join(map(str, config))

def bfs(s_config, e_config, k_pegs):
    permutations = list(itertools.permutations(range(k_pegs), 2))
    visited_nodes = set()
    queue = deque([Node(None, None, s_config)])
    
    while queue:
        node = queue.popleft()
        if node not in visited_nodes:
            visited_nodes.add(node)
            if node.config_str == e_config:
                break
            nexts = node.next_configs(k_pegs, permutations)
            queue.extend(nexts)
        
    moves = []
    while node:
        if node.last_move:
            moves.append(node.last_move)
        node = node.parent
    moves.reverse()

    return moves
    
while True:
    try:
        line = raw_input()
        n, k = [int(x) for x in line.split(' ')]
        s_config = raw_input()
        e_config = raw_input()

        moves = bfs(s_config, e_config, k)

        print len(moves)
        for x, y in moves:
            print x, y
    except EOFError:
        break

