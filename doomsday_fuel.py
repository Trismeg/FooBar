'''Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function answer(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].'''


def answer(matrix):
    H=len(matrix)
    W=len(matrix[0])
    mat=list(matrix)
    for i,elem in enumerate(mat):
        elem[i]=0
    sums=[sum(i) for i in mat]
    terms=[i for i,item in enumerate(sums) if item==0]
    not_terms=list((set(range(H)) - set(terms)))
    #print(mat)
    #print("dims",H,W)
    #print("sums",sums)
    #print("terminal indices",terms)
    #print("not terminal indices",not_terms)
    L=len(not_terms)
    
    for i in range(0,L-1):
        indB=not_terms[L-i-1]
        for j in range(0,L-1):
            indA=not_terms[j]        
            mat[indA]=fuse(mat[indA],indA,mat[indB],indB)
    output=[]
    for i in terms:
        output.append(mat[0][i])
    tot=sum(output)
    output.append(tot)
    if tot == 0:
        output=[1 for i in terms]
        output.append(len(terms))
    #print(mat)
    return output
        
    #others=(not_terms - {0})
    #print(others)
    
    

    
def fuse(v1,i1,v2,i2):
    #method to back propagate distribution
    lenV=len(v1)
    indices=(set(range(lenV))-{i1,i2})
    sum2=sum(v2)
    out = [0 for i in v1]
    for i in indices:
        out[i]= sum2*v1[i]+v1[i2]*v2[i]
    gc=gcd_list(out)
    output = [int( i / gc ) for i in out ]
    return output
    

def gcd (a,b):
    if (b == 0):
        return a
    else:
        return gcd (b, a % b)
         
def gcd_list(lst):
    L=len(lst)
    out=0
    for i in range(0,L):
        out=gcd(out,lst[i])
    return out
    
mat=[
  [1,1,1,3,4,1,1,2],  
  [4,1,3,3,2,3,0,4], 
  [0,0,0,1,0,0,8,9], 
  [0,0,3,0,0,0,0,0],
  [0,0,0,0,0,0,0,0], #terminal
  [0,0,0,0,0,0,0,0],  # terminal
  [0,0,0,0,0,0,0,0],  # terminal
  [0,0,0,0,0,0,0,0],  # terminal
]


print(answer(mat))
