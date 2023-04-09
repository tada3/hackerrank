# https://iqcode.com/code/python/kittys-calculations-on-a-tree-hackerrank-solution
from collections import Counter, defaultdict

MOD = 10**9 + 7

def read_row():
    return (int(x) for x in input().split())

def mul(x, y):
    return (x * y) % MOD

def add(*args):
    return sum(args) % MOD

def sub(x, y):
    return (x - y) % MOD

n, q = read_row()

# Construct adjacency list of the tree
adj_list = defaultdict(list)

for _ in range(n - 1):
    u, v = read_row()
    adj_list[u].append(v)
    adj_list[v].append(u)

# Construct element to set mapping {element: [sets it belongs to]}
elements = {v: set() for v in adj_list}

for set_no in range(q):
    read_row()
    for x in read_row():
        elements[x].add(set_no)

print('ELEMENTS', elements)

# Do BFS to find parent for each node and order them in reverse depth
print('ADJ', adj_list)
root = next(iter(adj_list))
print('ROOT', root)
current = [root]
current_depth = 0
order = []
parent = {root: None}
depth = {root: current_depth}

while current:
    current_depth += 1
    order.extend(current)
    nxt = []
    for node in current:
        for neighbor in adj_list[node]:
            if neighbor not in parent:
                parent[neighbor] = node
                depth[neighbor] = current_depth
                nxt.append(neighbor)

    current = nxt

print('PARENT', parent)

# Process nodes in the order created above
score = Counter()
# {node: {set_a: [depth, sum of nodes, flow]}}
state = {}
for node in reversed(order):
    print('NODE', node)
    states = [state[neighbor] for neighbor in adj_list[node] if neighbor != parent[node]]
    largest = {s: [depth[node], node, 0] for s in elements[node]}

    print('STATES', states)
    print('LARGEST', largest)

    if states:
        max_index = max(range(len(states)), key=lambda x: len(states[x]))
        if len(states[max_index]) > len(largest):
            states[max_index], largest = largest, states[max_index]

    print('STATES2', states)
    print('LARGEST2', largest)


    sets = defaultdict(list)
    for cur_state in states:
        for set_no, v in cur_state.items():
            sets[set_no].append(v)

    print('SETS', sets)

    for set_no, states in sets.items():
        print('    SETS LOOP', set_no, states)
        if len(states) == 1 and set_no not in largest:
            largest[set_no] = states[0]
            print('    CONTINUE', largest)

            continue

        if set_no in largest:
            states.append(largest.pop(set_no))
            print('    STATES APPEND', states)

    

        total_flow = 0
        total_node_sum = 0

        for node_depth, node_sum, node_flow in states:
            print('        STATES LOOP1', node_depth, node_sum, node_flow)
            flow_delta = mul(node_depth - depth[node], node_sum)
            print('        flow_delta', flow_delta)
            total_flow = add(total_flow, flow_delta, node_flow)
            print('        total_flow', total_flow)
            total_node_sum += node_sum
            print('        total_node_sum', total_node_sum)

        set_score = 0

        for node_depth, node_sum, node_flow in states:
            print('        STATES LOOP2', node_depth, node_sum, node_flow)
            node_flow = add(mul(node_depth - depth[node], node_sum), node_flow)
            print('        node_flow', node_flow)
            diff = mul(sub(total_flow, node_flow), node_sum)
            print('        diff', diff)
            set_score = add(set_score, diff)
            print('        SET_SCORE', set_score)

        score[set_no] = add(score[set_no], set_score)
        largest[set_no] = (depth[node], total_node_sum, total_flow)
        print('    LARGEST (END LOOP)', largest)


    state[node] = largest
    print('STATE', state)
    print('SCORE', score)

print(*(score[i] for i in range(q)), sep='\n')
