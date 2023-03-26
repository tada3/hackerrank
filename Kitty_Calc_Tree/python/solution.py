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


def get_delta(q, processed, lca, depth, anc):
	res = 0
	lca1 = get_lca(lca, q, depth, anc)
	if depth[lca1] < depth[lca]:
		# q is outside of the subtree of the processed nodes.
		# So, LCAs of (q, p) is lca1
		for p in processed:
			dist = get_dist_with_lca(q, p, lca1, depth)
			res = add_exp(res, q, p, dist)
	else:
		# q is inside of the subtree of the prcessed nodes.
		lca1 = lca
		for p in processed:
			dist = get_dist(depth, anc, q, p)
			res = add_exp(res, q, p, dist)
	return res, lca1

def get_delta2(q, processed, lca, depth, anc):
	res = 0
	lca1 = get_lca(lca, q, depth, anc)
	#print('get_delta2 lca1, lca', lca1, lca)
	if lca1 == lca:
		# q is inside of the subtree of the prcessed nodes.
		for p in processed:
			dist = get_dist(depth, anc, q, p)
			res = add_exp(res, q, p, dist)
	else:
		# q is outside of the subtree of the processed nodes.
		# So, LCAs of (q, p) is lca1
		for p in processed:
			dist = get_dist_with_lca(q, p, lca1, depth)
			res = add_exp(res, q, p, dist)
	return res, lca1




def get_lca(u, v, depth, anc):
	uu = u
	vv = v
	# Move the lower to the same level with the other
	if depth[uu] != depth[vv]:
		if depth[uu] > depth[vv]:
			uu, vv = vv, uu

		diff = depth[vv] - depth[uu]
		max_logn = log_ceil(diff)
		for j in range(max_logn, -1, -1):
			if (diff >> j) > 0:
				vv = anc[j][vv]
				diff = depth[vv] - depth[uu]

	# Get LCA
	if uu == vv:
		return uu

	max_logn = log_ceil(depth[uu])
	for j in range(max_logn, -1, -1):
		if anc[j][uu] != anc[j][vv]:
			uu = anc[j][uu]
			vv = anc[j][vv]

	return anc[0][uu]	

def get_dist(depth, anc, u, v):
	lca = get_lca(u, v, depth, anc)
	#print('get_dist', u, v, lca, depth[u] + depth[v] - 2 * depth[lca])
	return depth[u] + depth[v] - 2 * depth[lca]

def get_dist2(depth, anc, u, v):
	lca = get_lca(u, v, depth, anc)
	#print('get_dist2', u, v, lca, depth[u] + depth[v] - 2 * depth[lca])
	return depth[u] + depth[v] - 2 * depth[lca], lca

def get_dist_with_lca(u, v, lca, depth):
	#print('get_dist_with_lca', u, v, lca, depth[u] + depth[v] - 2 * depth[lca])
	return depth[u] + depth[v] - 2 * depth[lca]

def add_exp(cur, a, b, dist):
	delta = (a+1) * (b+1) % MOD
	delta = delta * dist % MOD
	#print('add_ext', a, b, delta)
	return (cur + delta) % MOD


def log_ceil(x):
	return math.ceil(math.log2(x))


def process_queries(k, queries, depth, ancestor):
	result = 0
	for i in range(k-1):
		for j in range(i+1, k):
			u = queries[i]
			v = queries[j]
			dist = get_dist(depth, ancestor, u, v)
			delta = (u+1) * (v+1) % MOD
			delta = delta * dist % MOD
			#print('process_queries', u, v, delta)
			result = (result + delta) % MOD
	return result


def process_queries2(k, queries, depth, anc):
	result = 0
	if k <= 1:
		return result
	
	u = queries[0]
	v = queries[1]
	dist, lca = get_dist2(depth, anc, u, v)
	result = (u+1) * (v+1) % MOD
	result = result * dist % MOD
	#print('process_queries2', u, v, result)
	processed = [u, v]

	for q in queries[2:]:
		delta, lca = get_delta2(q, processed, lca, depth, anc)
		result = (result + delta) % MOD
		processed.append(q)
	return result


def solution():
	n, q = map(int, input().split())
	if n <= 1:
		return

	tree = [False] * n
	children = [ [] for _ in range(n)]
	parent = [-1] * n

	a, b = map(lambda x: int(x)-1, input().split())
	root = a
	#print('root', root)
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

	#print('children', children)
	depth, max_depth = get_depth(n, children, root)
	#print('depth, max_depth', depth, max_depth)
	logn = log_ceil(max_depth)
	ancestor = get_ancestor(n, logn, parent)

	del tree
	del children
	del parent

	for _ in range(q):
		k = int(input())
		queries = [ int(x)-1 for x in input().split() ]
		result = process_queries2(k, queries, depth, ancestor)
		print(result)
	
solution()

	