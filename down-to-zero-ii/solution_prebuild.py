import sys


# Pre-build a list of shortest move for all
# integers from 0 to n
def downToZero(n):
    sm = [n] * (n+1)
    if n == 0:
        return sm
    
    sm[0] = 0
    for i in range(1, n+1):
        if sm[i-1] + 1 < sm[i]:
            sm[i] = sm[i-1] + 1
        
        for j in range(2, i+1):
            if i * j > n:
                break
            if sm[i] + 1 < sm[i * j]:
                sm[i * j] = sm[i] + 1
    
    return sm


if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')
    fptr = sys.stdout

    q = int(input().strip())

    n_list = [0] * q
    n_max = 0
    i = 0
    for q_itr in range(q):
        n = int(input().strip())
        if n > n_max:
            n_max = n
        n_list[i] = n
        

        #result = downToZero(n)

        #fptr.write(str(result) + '\n')
        i += 1

    shortest_move = downToZero(n_max)

    for x in n_list:
        fptr.write(str(shortest_move[x]) + '\n')

    fptr.close()
