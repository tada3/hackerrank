#!/bin/python3

import math
import os
import random
import re
import sys
from collections import deque

#
# Complete the 'isBalanced' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#

def is_left(c):
    if c in ['(', '{', '[']:
        return True
    return False

def isBalanced(s):
    # Write your code here
    # Use stak
    stack = deque()
    for c in s:
        if is_left(c):
            stack.append(c)
            continue
        if not stack:
            return 'NO'
        top = stack.pop()
        if (c == ')' and top == '(') or (c == '}' and top == '{') or (c == ']' and top == '['):
            continue
        return 'NO'
    if stack:
        return 'NO'
    return 'YES'

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')
    fptr = sys.stdout

    t = int(input().strip())

    for t_itr in range(t):
        s = input()

        result = isBalanced(s)

        fptr.write(result + '\n')

    fptr.close()
