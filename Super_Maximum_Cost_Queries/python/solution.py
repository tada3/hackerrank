#!/bin/python3

import math
import os
import random
import re
import sys
import bisect

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
	# 1. Build cost table 
	# cost_tab[U][V]: cost of the path {U, V}
	cost_tab = {}
	cost_rank = {}

	u, v, w = tree[0]
	cost_tab[u] = {v: w}
	cost_tab[v] = {u: w}
	cost_rank[w] = 1
	
	for i in range(1, N-1):
		u, v, w = tree[i]
		if u in cost_tab:
			# Make sure u is new node
			u, v = v, u
		cost_tab[u] = {v: w}
		cost_rank[w] = cost_rank.get(w, 0) + 1
		for x, c in cost_tab[v].items():
			c1 = max(c, w)
			cost_tab[u][x] = c1
			cost_tab[x][u] = c1
			cost_rank[c1] = cost_rank.get(c1, 0 ) + 1
		cost_tab[v][u] = w

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
