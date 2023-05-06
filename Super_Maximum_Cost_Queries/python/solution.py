#!/bin/python3

import math
import os
import random
import re
import sys
import bisect
from operator import itemgetter
from itertools import groupby

def build_path_counts(t):
	t1 = sorted(t, key=itemgetter(2))

	roots = [0] * (len(t1) + 2)
	sizes = {}
	path_counts = {}
	count = 0
	key_idx = []
	for k, g in groupby(t1, key=itemgetter(2)):
		for u, v, _ in g:
			count += add_path(u, v, roots, sizes)
		path_counts[k] = count	
		key_idx.append(k)

	return key_idx, path_counts

def add_path(u, v, rs, ss):
	added = 0
	if rs[u] == 0:
		if rs[v] == 0:
			# case 1: both new nodes
			added = add_new_new(u, v, rs, ss)
		else:
			# case 2: new node + existing node
			added = add_new_existing(u, v, rs, ss)
	else:
		if rs[v] == 0:
			# case 2 new node + existing node
			added = add_new_existing(v, u, rs, ss)
		else:
			# case 3: both existing nodes
			added = add_existing_existing2(u, v, rs, ss)
	return added



def get_root(x, rs):
	current = x
	while True:
		#print('LOOP', current)
		r = rs[current]
		if r == current:
			return r
		current = r	

def get_size(x, rs, ss):
	r = get_root(x, rs)
	return ss[r]	



def add_new_new(u, v, rs, ss):
	if u > v:
		u, v = v, u
	rs[u] = u
	rs[v] = u
	ss[u] = 2
	return 1


def add_new_existing(u, v, rs, ss):
	nodes_in_v = get_size(v, rs, ss)
	new_leader = get_root(v, rs)
	if u < new_leader:
		rs[new_leader] = u
		new_leader = u
	rs[u] = new_leader
	
	ss[new_leader] = nodes_in_v + 1	
	return nodes_in_v
	

def add_existing_existing2(u, v, rs, ss):
	# path(x, y)
	nodes_in_u = get_size(u, rs, ss)
	nodes_in_v = get_size(v, rs, ss)

	lu = get_root(u, rs)
	#lv = get_root(v, rs)
	#new_leader = lv
	new_leader = get_root(v, rs)

	if lu < new_leader:
		rs[new_leader] = lu
		new_leader = lu
	else:
		rs[lu] = new_leader

	ss[new_leader] = nodes_in_u + nodes_in_v
	return nodes_in_u * nodes_in_v


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
	# 1. Build path_counts
	# path_counts[c]: number of paths of cost c
	key_idx, path_counts = build_path_counts(tree)
		
	# 2. Process queries 
	Q = len(queries)
	result = [0] * Q
	for i in range(Q):
		l, r = queries[i]
		left = bisect.bisect_left(key_idx, l)
		right = bisect.bisect_left(key_idx, r, lo=left)
		if right >= len(key_idx) or key_idx[right] > r:
			right -= 1
		left -= 1
		left_val = path_counts[key_idx[left]] if left >= 0 else 0
		right_val = path_counts[key_idx[right]]
		result[i] = right_val - left_val
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
