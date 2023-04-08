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
	


def add_exp(cur, a, b, dist):
	delta = (a+1) * (b+1) % MOD
	delta = delta * dist % MOD
	#print('add_ext', a, b, delta)
	return (cur + delta) % MOD

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

def get_dist(start, end, lca, depth):
	return depth[start] + depth[end] - 2 * depth[lca]

def process_queries(k, q, st, depth, f_v):
	result = 0
	for i in range(k-1):
		for j in range(i+1, k):
			u = q[i]
			v = q[j]
			start = f_v[u]
			end = f_v[v]
			lca = st.query(start, end)
			dist = get_dist(start, end, lca, depth)

			#print('process_queries', u, v, delta)
			result = add_exp(result, u, v, dist)
	return result

def solution():
	n, q = map(int, input().split())
	if n <= 1:
		return

	tree = [False] * n
	children = [ [] for _ in range(n)]

	a, b = map(lambda x: int(x)-1, input().split())
	root = a
	#print('root', root)
	children[a].append(b)
	tree[a] = True
	tree[b] = True

	for _ in range(n-2):
		a, b = map(lambda x: int(x)-1, input().split())
		if not tree[a] and not tree[b]:
			raise ValueError(f'Both {a} and {b} are new nodes')
		if not tree[a]:
			children[b].append(a)
			tree[a] = True
			tree[b] = True
		else:
			children[a].append(b)
			tree[a] = True
			tree[b] = True

	# Euler Tour
	et_d, f_v = euler_tour(n, children, root)

	# Sparse Table for getting LCA
	st = SparseTable(et_d)
	
	# Process Queries with Sparse Table
	for _ in range(q):
		k = int(input())
		queries = [ int(x)-1 for x in input().split() ]
		
		result = process_queries(k, queries, st, et_d, f_v)
		print(result)

solution()

	