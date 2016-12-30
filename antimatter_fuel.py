##In this problem we are given an integer and determine the fewest step to get to one by adding one, subtracting one, or dividing by two.

def answer(n):
    N=int(n)
    steps=0
    while(N>3):
        print (N)
        if N%2== 0:
            steps += 1
            N=int(N/2)
        else:
            if N%4 == 1:
                steps += 1
                N=N-1
            else:
                steps += 1
                N=N+1
    return N-1 + steps
    
for i in range(43,44):
    print(i,answer(i))
