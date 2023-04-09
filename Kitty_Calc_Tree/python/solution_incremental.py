import time
import sys
from collections import deque
import itertools

MOD = 10**9 + 7

def mul(x, y):
    return (x * y) % MOD

def add(x, y):
	return (x + y) % MOD

def add3(x, y, z):
	return (x + y + z) % MOD

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
		stll = self.st[log_len]
		return self.min_a(stll[x], stll[y-(1<<log_len)])


		
	def min_a(self, x, y):
		return x if self.a[x] < self.a[y] else y
	
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


def add_exp3(cur, a, b, dist):
	#print('add_ext', a, b, delta)
	return ((a+1)*(b+1)%MOD * dist % MOD + cur) % MOD

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


def etime(t0):
	t1 = time.perf_counter_ns()
	delta = (t1 - t0) / 1000000 
	print(f'time: {delta}')
	return t1

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

def solution():
	t0 = time.perf_counter_ns()
	n, q = map(int, sys.stdin.readline().split())
	if n <= 1:
		return
	
	print('n, q', n, q)

	tree = [False] * n
	children = [ [] for _ in range(n)]

	a, b = map(lambda x: int(x)-1, sys.stdin.readline().split())
	root = a
	#print('root', root)
	children[a].append(b)
	tree[a] = True
	tree[b] = True

	for _ in range(n-2):
		a, b = map(lambda x: int(x)-1, sys.stdin.readline().split())
#		if not tree[a] and not tree[b]:
#			raise ValueError(f'Both {a} and {b} are new nodes')
		if not tree[a]:
			children[b].append(a)
			tree[a] = True
		else:
			children[a].append(b)
			tree[b] = True

	depth, path = get_depth(n, children, root)

	print('DEPTH', depth)
	print('PATH', path)

	qset = [ [] for x in range(n) ]

	for qset_id in range(q):
		# k = int(sys.stdin.readline())
		sys.stdin.readline() # k is not used
		queries =  [ int(x)-1 for x in sys.stdin.readline().split() ]
		for node in queries:
			qset[node].append(qset_id)

	print('QSET', qset)

	node_entries = {}
	S = [0] * q
	print('SSSS before', S, q)

	for node in reversed(path):
		print('    NODE', node)


		node_entry = {}
		for qset_id in qset[node]:
			node_entry[qset_id] = (depth[node], node+1, 0)

		workplace = {}
		for c in children[node]:
			print('        children loop', c)
			entry = node_entries.get(c)
			if not entry:
				continue
			
			print('        entry', entry)
			for qset_id, node_info in entry.items():
				print('            aaa.items loop', qset_id, node_info)
				if qset_id in workplace:
					workplace[qset_id].append(node_info)
				else:
					workplace[qset_id] = [node_info]

		for qset_id, entries in workplace.items():
			# assume len(entries) >= 1
			print('        zzz loop', qset_id, entries)
		
			if qset_id in node_entry:
				entries.append(node_entry.pop(qset_id))

			
			if len(entries) == 1:
				# carry over to the parent node
				node_entry[qset_id] = entries[0]
				continue

			v_total = 0
			t_total = 0
			for d, v, t in entries:
				print('             entries loop', depth, v, t)
				v_total = add(v_total, v)
				t_entry = add(t, mul(d - depth[node], v))
				t_total = add(t_total, t_entry)

			print('        111', v_total, t_total)

			s_delta_total = 0
			for d, v, t in entries:
				t_entry = add(t, mul(d - depth[node], v))
				s_delta_entry = mul((t_total - t_entry), v)
				s_delta_total = add(s_delta_total, s_delta_entry)

			print('        222', s_delta_total)

			S[qset_id] = add(S[qset_id], s_delta_total)
			node_entry[qset_id] = (depth[node], v_total, t_total)


		
		

		print('ZZZZ', workplace)

		node_entries[node] = node_entry

	print('XXX', node_entries)

	print(*S, sep='\n')





solution()

	