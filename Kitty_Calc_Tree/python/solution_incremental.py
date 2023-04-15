import sys
from collections import deque, defaultdict

MOD = 10**9 + 7

def mul(x, y):
    return (x * y) % MOD

def add(x, y):
	return (x + y) % MOD

def build_tree(n):
	tree = [False] * n
	children = [ [] for _ in range(n)]

	a, b = [ int(x)-1 for x in sys.stdin.readline().split() ]
	root = a
	children[a].append(b)
	tree[a] = True
	tree[b] = True

	for _ in range(n-2):
		a, b = [ int(x)-1 for x in sys.stdin.readline().split() ]
#		if not tree[a] and not tree[b]:
#			raise ValueError(f'Both {a} and {b} are new nodes')
		if not tree[a]:
			children[b].append(a)
			tree[a] = True
		else:
			children[a].append(b)
			tree[b] = True
	
	return children, root

def get_depth(n, ch, root):
	# Breadth-first traversal
	# Result is the same for BFS and DFS. But BFS seems be a bit faster in this problem.
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
		workplace = defaultdict(list)
		post_processed = {}

		# collect entries in child nodes
		for c in children[node]:
			entry = node_entries[c]
			if not entry:
				continue
			
			tmp = entry
			if len(entry) > len(post_processed):
				tmp = post_processed
				post_processed = entry

			for qset_id, node_info in tmp.items():
				workplace[qset_id].append(node_info)
			node_entries[c] = None

		# add entry of the current node
		pre_processed =  {qset_id: (depth[node], node+1, 0) for qset_id in qset[node]}
		tmp = pre_processed
		if len(pre_processed) > len(post_processed):
			tmp = post_processed
			post_processed = pre_processed
		for qset_id, node_info in tmp.items():
			workplace[qset_id].append(node_info)

		# proess data in workplace
		for qset_id, node_infos in workplace.items():
			# assume len(entries) >= 1
			if len(node_infos) == 1 and qset_id not in post_processed:
				# carry over to the parent node
				post_processed[qset_id] = node_infos[0]
				continue

			if qset_id in post_processed:
				node_infos.append(post_processed[qset_id])

			v_total = 0
			t_total = 0
			for d, v, t in node_infos:
				v_total = add(v_total, v)
				t_entry = add(t, mul(d - depth[node], v))
				t_total = add(t_total, t_entry)

			s_delta_total = 0
			for d, v, t in node_infos:
				t_entry = add(t, mul(d - depth[node], v))
				s_delta_entry = mul((t_total - t_entry), v)
				s_delta_total = add(s_delta_total, s_delta_entry)

			S[qset_id] = add(S[qset_id], s_delta_total)
			post_processed[qset_id] = (depth[node], v_total, t_total)

		node_entries[node] = post_processed
	return S

def solution():
	N, Q = map(int, sys.stdin.readline().split())
	if N <= 1:
		return
	
	children, root = build_tree(N)

	depth, path = get_depth(N, children, root)

	qset = [ [] for _ in range(N) ]
	for qset_id in range(Q):
		# k = int(sys.stdin.readline())
		sys.stdin.readline() # k is not used
		for node in (int(x)-1 for x in sys.stdin.readline().split()):
			qset[node].append(qset_id)

	S = process_queries(Q, path, qset, depth, children)

	print(*S, sep='\n')



solution()
