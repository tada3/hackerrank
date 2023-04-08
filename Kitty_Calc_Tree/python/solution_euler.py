import math
from collections import deque

MOD = 10**9 + 7

class SparseTable:
	def __init__(self, a):
		self.a = a
		size = len(self.a)
		self.logs = self.build_logs(size)
		log_size = self.logs[size] + 1
		self.st = self.build_st(size, log_size)

	# st[i][j]: index corresponding to the minimum value in [j, j + 2**i) of a.
	# Here we use half open interval.
	# It is possible to set the minimum value to st[i][j], but we set an index because sometimes 
	# we need to get other attributes such as node ID.
	def build_st(self, n, m):
		st = [ [0]*n for i in range(m) ]

		# st[0][j] is an index of a that has the minimum value in [j, j+1).
		for j in range(n):
			st[0][j] = j
		
		for i in range(1, m):
			for j in range(n):
				end = j + (1 << i)
				# Value is not needed if end is out of range.
				if end > n:
					break
				st[i][j] = self.min_a(st[i-1][j], st[i-1][j+(1<<(i-1))])
		return st
		
	def query(self, x, y):
		if x == y:
			return x
		if x > y:
			x, y = y, x
		# Make it half open interval.
		y += 1
		log_len = self.logs[y-x]
		return self.min_a(self.st[log_len][x], self.st[log_len][y-(1<<log_len)])
	
	def min_a(self, x, y):
		if self.a[x] < self.a[y]:
			return x
		else:
			return y
	
	@staticmethod
	def build_logs(n):
		# logs[n] is used.
		logs = [0] * (n + 1)
		for i in range(2, n + 1):
			logs[i] = logs[i >> 1] + 1
		return logs
	

	
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
	#print('get_delta2 lca1, lca', lca1, lca)
	if lca1 == lca:
		# q is inside of the subtree of the prcessed nodes.
		for p in processed:
			dist, _ = get_dist(depth, anc, q, p)
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

def euler_tour(n, ch, root):
	# Usually record node value, but we do not need it in this case.
	et_d = [0] * (2 * n - 1)
	f_v = [-1] * n

	# Depth-first
	stack = deque()

	stack.append(root)

	i = 0
	d = -1
	while True:
		if not stack:
			break
		v = stack.pop()

		if v >= 0:
			d += 1
			et_d[i] = d
			if f_v[v] < 0:
				f_v[v] = i

			for c in ch[v]:
				stack.append(~v)
				stack.append(c)
		else:
			d -= 1
			et_d[i] = d

		i += 1

	return et_d, f_v


def get_dist3(start, end, lca, depth):
	return depth[start] + depth[end] - 2 * depth[lca]

def process_queries2(k, q, st, depth, f_v):
	result = 0
	for i in range(k-1):
		for j in range(i+1, k):
			u = q[i]
			v = q[j]
			start = f_v[u]
			end = f_v[v]
			lca = st.query(start, end)
			dist = get_dist3(start, end, lca, depth)

			delta = (u+1) * (v+1) % MOD
			delta = delta * dist % MOD
			#print('process_queries', u, v, delta)
			result = (result + delta) % MOD
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

	# Euler Tour
	et_d, f_v = euler_tour(n, children, root)

	# Get LCA
	st = SparseTable(et_d)
	
	for _ in range(q):
		k = int(input())
		queries = [ int(x)-1 for x in input().split() ]
		
		result = process_queries2(k, queries, st, et_d, f_v)
		print(result)

solution()

	