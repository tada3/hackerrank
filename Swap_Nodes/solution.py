import sys
from collections import deque

class Node:
    def __init__(self, idx, depth):
      self.index = idx
      self.depth = depth
      self.left = None
      self.right = None


    def add_left(self, l):
        self.left = Node(l, self.depth + 1)   
        return self.left     

    def add_right(self, r):
        self.right = Node(r, self.depth + 1)    
        return self.right

    def explore(self):
        path = []
        if self.left is not None:
            path.extend(self.left.explore())
        path.append(self.index)
        if self.right is not None:
            path.extend(self.right.explore())
        return path
    
    def query(self, q):
        ret = []
        d = q
        queue = deque()
        queue.append(self)       
        
        while queue:
            node = queue.popleft()

            if node.depth > d:
                d += q
        
            if node.depth == d:
                ret.append(node)
                
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        return ret
   
    def swap(self):
        self.left, self.right = self.right, self.left

       
    def print(self):
        l = -1
        if self.left is not None:
            l = self.left.index
        r = -1
        if self.right is not None:
            r = self.right.index
        print(f'{self.index}({l}, {r})')




# Complete the 'swapNodes' function below.
#
# The function is expected to return a 2D_INTEGER_ARRAY.
# The function accepts following parameters:
#  1. 2D_INTEGER_ARRAY indexes
#  2. INTEGER_ARRAY queries
#
def swapNodes(indexes, queries):
    # Write your code here

    N = len(indexes)

    # 1. Build Tree
    nodes = [0] * N
    nodes[0] = Node(1, 1)
    for i, ab in enumerate(indexes):
        a = ab[0]
        if a > 0:
            nodes[a-1] = nodes[i].add_left(a)
        b = ab[1]
        if b > 0:
            nodes[b-1] = nodes[i].add_right(b)
    
    # 2. Swap and Explore
    path_list = []
    for q in queries:
        targets = nodes[0].query(q)
        for t in targets:
            t.swap()
                    
        path = nodes[0].explore()
        path_list.append(path)

    return path_list

if __name__ == '__main__':
#    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    fptr = sys.stdout

    n = int(input().strip())

    indexes = []

    for _ in range(n):
        indexes.append(list(map(int, input().rstrip().split())))

    queries_count = int(input().strip())
    
    queries = []

    for _ in range(queries_count):
        queries_item = int(input().strip())
        queries.append(queries_item)

    result = swapNodes(indexes, queries)

    fptr.write('\n'.join([' '.join(map(str, x)) for x in result]))
    fptr.write('\n')

    fptr.close()
