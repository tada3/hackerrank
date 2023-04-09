import sys
from collections import deque

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

def process_queries(n, q, path, qset, depth, children):
	node_entries = [None] * n
	S = [0] * q

	for node in reversed(path):
		node_entry = {}
		for qset_id in qset[node]:
			node_entry[qset_id] = (depth[node], node+1, 0)

		workplace = {}
		for c in children[node]:
			entry = node_entries[c]
			if not entry:
				continue
			
			for qset_id, node_info in entry.items():
				if qset_id in workplace:
					workplace[qset_id].append(node_info)
				else:
					workplace[qset_id] = [node_info]

		for qset_id, entries in workplace.items():
			# assume len(entries) >= 1
			if qset_id in node_entry:
				entries.append(node_entry.pop(qset_id))

			
			if len(entries) == 1:
				# carry over to the parent node
				node_entry[qset_id] = entries[0]
				continue

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
			node_entry[qset_id] = (depth[node], v_total, t_total)

		node_entries[node] = node_entry
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

	S = process_queries(N, Q, path, qset, depth, children)

	print(*S, sep='\n')



solution()
	