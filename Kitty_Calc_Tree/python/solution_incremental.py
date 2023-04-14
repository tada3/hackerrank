import sys
from collections import deque, defaultdict

MOD = 10**9 + 7

def mul(x, y):
    return (x * y) % MOD

def add(x, y):
	return (x + y) % MOD

def get_depth(n, ch, root):
	# Breadth-first traversal
	depth = [0] * n
	path = [0] * n
	queue = deque()
	queue.append(root)
	i = 0
	while queue:
		node = queue.popleft()
		path[i] = node
		if ch[node]:
			d = depth[node] + 1
			for c in ch[node]:
				depth[c] = d
				queue.append(c)
		i += 1
	return depth, path

def process_queries(q, path, qset, depth, children):
	node_entries = {}
	S = [0] * q

	for node in reversed(path):
		workplace = {}
		# collect entries in child nodes
		for c in children[node]:
			entry = node_entries[c]
			if not entry:
				continue
			
			for qset_id, node_info in entry.items():
				if qset_id in workplace:
					workplace[qset_id].append(node_info)
				else:
					workplace[qset_id] = [node_info]
			node_entries[c] = None

		if len(workplace) == 0:
			# No entries in child nodes
			node_entries[node] ={qset_id: (depth[node], node+1, 0) for qset_id in qset[node]}
			continue

		processed = {}
		for qset_id in qset[node]:
			processed[qset_id] = (depth[node], node+1, 0)

		
		for qset_id, entries in workplace.items():
			# assume len(entries) >= 1
			if len(entries) == 1 and qset_id not in processed:
				# carry over to the parent node
				processed[qset_id] = entries[0]
				continue

			if qset_id in processed:
				entries.append(processed[qset_id])

			v_total = 0
			t_total = 0
			for d, v, t in entries:
				v_total = add(v_total, v)
				t_entry = add(t, mul(d - depth[node], v))
				t_total = add(t_total, t_entry)

			s_delta_total = 0
			for d, v, t in entries:
				t_entry = add(t, mul(d - depth[node], v))
				s_delta_entry = mul((t_total - t_entry), v)
				s_delta_total = add(s_delta_total, s_delta_entry)

			S[qset_id] = add(S[qset_id], s_delta_total)
			processed[qset_id] = (depth[node], v_total, t_total)

		node_entries[node] = processed
	return S

def process_queries2(q, path, qset, depth, children):
	node_entries = {}
	S = [0] * q

	for node in reversed(path):
		states = [ node_entries[child] for child in children[node] ]
		largest = { s: (depth[node], node+1, 0) for s in qset[node] }

		if states:
			max_index = max( range(len(states)), key=lambda x: len(states[x]))
			if len(states[max_index]) > len(largest):
				states[max_index], largest = largest, states[max_index]

	
		workplace = defaultdict(list)
		for cur_state in states:
			for qset_id, v in cur_state.items():
				workplace[qset_id].append(v)


		for qset_id, entries in workplace.items():
			# assume len(entries) >= 1
			if len(entries) == 1 and qset_id not in largest:
				# carry over to the parent node
				largest[qset_id] = entries[0]
				continue

			if qset_id in largest:
				entries.append(largest.pop(qset_id))

			v_total = 0
			t_total = 0
			for d, v, t in entries:
				v_total = add(v_total, v)
				t_entry = add(t, mul(d - depth[node], v))
				t_total = add(t_total, t_entry)

			s_delta_total = 0
			for d, v, t in entries:
				t_entry = add(t, mul(d - depth[node], v))
				s_delta_entry = mul((t_total - t_entry), v)
				s_delta_total = add(s_delta_total, s_delta_entry)

			S[qset_id] = add(S[qset_id], s_delta_total)
			largest[qset_id] = (depth[node], v_total, t_total)

		node_entries[node] = largest
	return S


def solution():
	N, Q = map(int, sys.stdin.readline().split())
	if N <= 1:
		return
	
	tree = [False] * N
	children = [ [] for _ in range(N)]

	a, b = map(lambda x: int(x)-1, sys.stdin.readline().split())
	root = a
	#print('root', root)
	children[a].append(b)
	tree[a] = True
	tree[b] = True

	for _ in range(N-2):
		a, b = map(lambda x: int(x)-1, sys.stdin.readline().split())
#		if not tree[a] and not tree[b]:
#			raise ValueError(f'Both {a} and {b} are new nodes')
		if not tree[a]:
			children[b].append(a)
			tree[a] = True
		else:
			children[a].append(b)
			tree[b] = True

	depth, path = get_depth(N, children, root)


	qset = [ [] for x in range(N) ]

	for qset_id in range(Q):
		# k = int(sys.stdin.readline())
		sys.stdin.readline() # k is not used
		for node in (int(x)-1 for x in sys.stdin.readline().split()):
			qset[node].append(qset_id)

	S = process_queries2(Q, path, qset, depth, children)

	print(*S, sep='\n')



solution()
	