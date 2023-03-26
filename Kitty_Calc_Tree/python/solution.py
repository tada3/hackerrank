import math
from collections import deque

MOD = 10**9 + 7
	
def get_depth(n, c, root):
	max_depth = 0
	depth = [0] * n
	# Breadth-first
	queue = deque()
	queue.append(root)
	while True:
		if not queue:
			# Not found
			break
		x = queue.pop()
		if not c[x]:
			continue
		d = depth[x] + 1
		if d > max_depth:
			max_depth = d
		for i in c[x]:
			depth[i] = d
			queue.append(i)
	return depth, max_depth

def get_ancestor(n, logn, p):
	anc = [ [0] * n for _ in range(logn+1)]
	for i in range(n):
		anc[0][i] = p[i]

	for j in range(logn):
		for i in range(n):
			if anc[j][i] == -1:
				anc[j+1][i] = -1
			else:
				anc[j+1][i] = anc[j][anc[j][i]]
	return anc    

def get_lca(logn, u, v, depth, anc):
	uu = u
	vv = v
	# Move the lower to the same level with the other
	if depth[uu] != depth[vv]:
		if depth[uu] < depth[vv]:
			uu, vv = vv, uu

		for j in range(logn, -1, -1):
			diff = depth[uu] - depth[vv]
			if (diff >> j) > 0:
				uu = anc[j][uu]

	# Get LCA
	if uu == vv:
		return uu

	for j in range(logn, -1, -1):
		if anc[j][uu] != anc[j][vv]:
			uu = anc[j][uu]
			vv = anc[j][vv]

	return anc[0][uu]	

def get_dist(logn, depth, anc, u, v):
	lca = get_lca(logn, u, v, depth, anc)
	return depth[u] + depth[v] - 2 * depth[lca]



def solution():
	n, q = map(int, input().split())
	if n <= 1:
		return

	tree = [False] * n
	children = [ [] for _ in range(n)]
	parent = [-1] * n

	a, b = map(lambda x: int(x)-1, input().split())
	root = a
	children[a].append(b)
	parent[b] = a
	tree[a] = True
	tree[b] = True

	for _ in range(n-2):
		a, b = map(lambda x: int(x)-1, input().split())
		if not tree[a] and not tree[b]:
			raise ValueError(f'Both {a} and {b} are new nodes')
		if not tree[a]:
			children[b].append(a)
			parent[a] = b
			tree[a] = True
			tree[b] = True
		else:
			children[a].append(b)
			parent[b] = a
			tree[a] = True
			tree[b] = True

	depth, max_depth = get_depth(n, children, root)
	logn = math.ceil(math.log2(max_depth))
	ancestor = get_ancestor(n, logn, parent)

	for _ in range(q):
		k = int(input())
		queries = [ int(x)-1 for x in input().split() ]
		result = 0
		for i in range(k-1):
			for j in range(i+1, k):
				u = queries[i]
				v = queries[j]
				dist = get_dist(logn, depth, ancestor, u, v)
				delta = (u+1) * (v+1) % MOD
				delta = delta * dist % MOD
				result = (result + delta) % MOD
		print(result)
	
solution()

	