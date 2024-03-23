# Down to Zero II

## solution.py
Solution with the breadth first search.
Searching the shortest path can be described as a tree. So we can use the breadth first search.
Why not the depth first search? I have not tested it, but I guess it would be slower because the right (shortest) path is short and wrong paths are long. If you explore a wrong path first a long time is wasted.

## solution_prebuild.py
Pre-compute the answers for all cases between 0 and the maximum N. So you can find the shortest path for N by simply checking the pre-computed answers.

## Which is faster?
Of course it depends on the situation. If Q is 1, solution.py is faster On the ohter hand, if Q is large enough, solution_prebuild.py would be faster. However, solution.py shows better performance even with a relatively large Q. For example, in the case of testcase1.in (Q=94), the processing times are as follows.
 - solution.py: 0.25 seconds
 - solution_prebuild.py: 1.5 seconds


