import sys

from collections import deque
from math import sqrt, floor



# Searching the shortest path can be described
# as a tree like this.
#       10
#      /  \
#     5    9
#     |   / \
#     4   3  8
#    / \    / \
#   2   3  4   7
#   |   |      |
#   1   2      6
#   |          |
#   0          5
# So, you can find the shortest path with the breadth first search.
def downToZero(n):
    if n <= 3:
        return n

    check = set()
    queue = deque()
    move = 0
    queue.append((n, move))

    while True:
        k, move = queue.popleft()
        if k == 2:
            move += 2
            break

        # Case 1: k=axb -> b (a < b)
        sr = floor(sqrt(k))
        for a in range(sr, 1, -1):
            if k%a != 0:
                continue
            b = k//a
            if b in check:
                continue
            queue.append((b, move+1))
            check.add(b)

        # Case 2: k -> k-1
        if k-1 in check:
            continue
        queue.append((k-1, move+1))
        check.add(k-1)

    return move
                
if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')
    fptr = sys.stdout
    

    q = int(input().strip())
    
    for q_itr in range(q):
        n = int(input().strip())

        result = downToZero(n)

        fptr.write(str(result) + '\n')
       

    fptr.close()
