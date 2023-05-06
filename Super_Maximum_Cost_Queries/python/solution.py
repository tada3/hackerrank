#!/bin/python3

import math
import os
import random
import re
import sys
import bisect



def build_cost_rank(t):
	cost_tab = {}
	cost_rank = {}
	
	for u, v, w in t:
		print('uvw', u, v, w)
		if u not in cost_tab:
			if v not in cost_tab:
				# case 1: both new nodes
				add_new_new(u, v, w, cost_tab, cost_rank)
			else:
				# case 2: new node + existing node
				add_new_existing(u, v, w, cost_tab, cost_rank)
		else:
			if v not in cost_tab:
				# case 2 new node + existing node
				add_new_existing(v, u, w, cost_tab, cost_rank)
			else:
				# case 3: both existing nodes
				add_existing_existing(u, v, w, cost_tab, cost_rank)
		print('TTT', cost_tab)
		
	print('tab', cost_tab)
	print('rank', cost_rank)
	return cost_rank
	

def add_new_new(u, v, w, tab, rank):
	print('add_new_new 000', u, v, w)
	tab[u] = {v: w}
	tab[v] = {u: w}
	rank[w] = rank.get(w, 0) + 1

def add_new_existing(u, v, w, tab, rank):
	print('add_new_existing 000', u, v, w)
	tab[u] = {}
	for x, c in tab[v].items():
		c1 = max(c, w)
		tab[u][x] = c1
		tab[x][u] = c1
		rank[c1] = rank.get(c1, 0 ) + 1

	tab[u][v] = w
	tab[v][u] = w
	rank[w] = rank.get(w, 0) + 1
	

def add_existing_existing(u, v, w, tab, rank):
	print('add_existing_existing 000', u, v, w)		
	xkeys = list(tab[u].keys())
	ykeys = list(tab[v].keys())

	# path(x, y)
	for x, cx in tab[u].items():
		print('LOOP1', x)
		for y, cy in tab[v].items():
			print('LOOP2', y)
			c1 = max(cx, w, cy)
			print('1111111', x, y, c1)
			tab[x][y] = c1
			tab[y][x] = c1
			rank[c1] = rank.get(c1, 0) + 1

	# path(x, v)
	for x, cx in tab[u].items():
		c1 = max(cx, w)
		print('222222', x, v, c1)
		tab[x][v] = c1
		#tab[v][x] = c1
		rank[c1] = rank.get(c1, 0) + 1
	
	print('add_existing_existing 100', u, v, w)

	# path(u, y)
	for y, cy in tab[v].items():
		# path(u, y)
		c1 = max(w, cy)
		print('33333333', u, y, c1)
		#tab[u][y] = c1
		tab[y][u] = c1
		rank[c1] = rank.get(c1, 0) + 1
	
	for x in xkeys:
		tab[v][x] = tab[x][v]

	for y in ykeys:
		tab[u][y] = tab[y][u]

	tab[u][v] = w
	tab[v][u] = w
	rank[w] = rank.get(w, 0) + 1

#
# Complete the 'solve' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. 2D_INTEGER_ARRAY tree
#  2. 2D_INTEGER_ARRAY queries
#

def solve(tree, queries):
    # Write your code here
	N = len(tree) + 1
	# 1. Build cost rank
	# cost_rank[c]: number of paths of cost c
	cost_rank = build_cost_rank(tree)

#	print('cost_tab', cost_tab)
#	print('cost_rank', cost_rank)

	# 2. Sort it
	key_idx = sorted(cost_rank.keys())
		
	# 3. Process queries 
	Q = len(queries)
	result = [0] * Q
	for i in range(Q):
		l, r = queries[i]
		left = bisect.bisect_left(key_idx, l)
		right = bisect.bisect_left(key_idx, r, lo=left)
		if right >= len(key_idx) or key_idx[right] > r:
			right -= 1
		count = 0
		for j in range(left, right + 1):
			idx = key_idx[j]
			count += cost_rank[key_idx[j]]
		result[i] = count
	return result


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    q = int(first_multiple_input[1])

    tree = []

    for _ in range(n - 1):
        tree.append(list(map(int, input().rstrip().split())))

    queries = []

    for _ in range(q):
        queries.append(list(map(int, input().rstrip().split())))

    result = solve(tree, queries)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
