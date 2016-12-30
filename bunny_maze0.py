import time
import numpy as np
A=np.zeros((20,20)).astype(int)
A[4][4]=1
A[1][1]=1
A[2][2]=1
A[3][3]=1
#A[0][1]=1
A[1][1]=1
A[1][0]=1
A[18][19]=1
A[19][15]=1
A[15][19]=1
A[3][0]=1
A[0][3]=1
A[7][9]=1
A[15][13]=1
A[5][5]=1
A[5][4]=1
A[5][3]=1
A[5][2]=1
A[5][1]=1
A[5][5]=1
A[4][5]=1
A[3][5]=1
A[2][5]=1
A[1][5]=1
A[0][2]=1
#A[0][1]=1
A[12][2]=1
A[2][12]=1
A[9][17]=1
A[15][5]=1
A[4][13]=1
A[4][5]=1
maze=A.tolist()
#maze=[[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]
#maze=[[0, 0, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]
#maze=[[0,1,0,1,0,0,0],[0,1,0,1,0,1,0],[0,0,0,0,0,1,0],[1,1,1,1,1,0,0]]
def answer(maze):
    shortest={0:1}
    
    H=len(maze)
    W=len(maze[0])
    N=H*W
    LL=N-W
    W2=2*W
    nexts={}
    connects4={}
    connects8={}
    edge=[]
    centers=[]
    corners=[]
    for i in range(1,W-1):
        nexts[i]=(i+1,i+W)    
        nexts[LL+i]=(LL+i+1,LL+i-W)
        connects4[i]=(i-1,i+1,i+W)
        connects4[LL+i]=(LL+i+1,LL+i-1,LL+i-W)
        connects8[i]=(i-1,i+1,i+W,i-1+W,i+1+W)
        connects8[LL+i]=(LL+i+1,LL+i-1,LL+i-W,LL+i-W+1,LL+i-W-1)
        edge.append(i)
        edge.append(i+LL)
    for i in range(1,H-1):
        Wi=W*i
        nexts[Wi]=(Wi+1,Wi+W)
        nexts[Wi-1+W]=(Wi-2+W,Wi-1+W2)
        connects4[Wi]=(Wi+1,Wi+W,Wi-W)    
        connects4[Wi-1+W]=(Wi-2+W,Wi-1+W2,Wi-1)
        connects8[Wi]=(Wi+1,Wi+W,Wi-W,Wi+W+1,Wi-W+1)    
        connects8[Wi-1+W]=(Wi-2+W,Wi-1+W2,Wi-1,Wi-2+W2,Wi-2)
        edge.append(Wi)
        edge.append(Wi-1+W)
        for j in range(1,W-1):
            nexts[Wi+j]=(Wi+j+1,Wi+j-1,Wi+j-W,Wi+j+W)
            connects4[Wi+j]=(Wi+j+1,Wi+j-1,Wi+j-W,Wi+j+W)
            connects8[Wi+j]=(Wi+j+1,Wi+j-1,Wi+j-W,Wi+j+W,Wi+j+1+W,Wi+j-1-W,Wi+j-W+1,Wi+j+W-1)
            centers.append(Wi+j)
    nexts[0]=(1,W)
    nexts[W-1]=(W2-1,)
    nexts[LL]=(LL+1,)
    #corners.append(0)
    corners.append(W-1)
    corners.append(LL)
    #corners.append(N-1)
    connects4[0]=(1,W)
    connects4[W-1]=(W-2,W2-1)
    connects4[LL]=(LL-W,LL+1)
    connects4[N-1]=(N-W-1,N-2)
    connects8[0]=(1,W,1+W)
    connects8[W-1]=(W-2,W2-1,W2-2)
    connects8[LL]=(LL-W,LL+1,LL-W+1)
    connects8[N-1]=(N-1-W,N-2,N-W-2)
    #print(nexts)
    fills={}
    all_zeros={-1}
    all_ones={-1}
    for i in range(H):
        for j in range(W):
            index=W*i+j
            elem=maze[i][j]
            fills[index]=elem
            if elem:
                all_ones.add(index)
            else:
                all_zeros.add(index)
        
    cc1={0}
    cc2={N-1}

    while True:
        cc1_len=len(cc1)
        for i in set(cc1):
            for j in connects4[i]:
                if (j not in cc1) and (fills[j] == 0):
                    cc1.add(j)
        if cc1_len==len(cc1):
            break
    
    while True:
        cc2_len=len(cc2)
        for i in set(cc2):
            for j in connects4[i]:
                    cc2.add(j)
        if cc2_len==len(cc2):
            break            
    
    b1={0}
    for i in set(cc1):
        for j in connects4[i]:
            if fills[j] == 1:
                b1.add(j)
        
    b2={N-1}
    for i in set(cc2):
        for j in connects4[i]:
            if fills[j] == 1:
                b2.add(j)   
    
                
    fills2=dict(fills)
    neighbor8={}
    neighbor4={}
    for i in range(1,N):
        neighbor8[i]=sum([ fills[j] for j in connects8[i]])
        neighbor4[i]=sum([ fills[j] for j in connects4[i]])
    
    #print("neigh4[1]",neighbor4[1])
    blancos={-1}
    blocked0={-1}
    blocked1={-1}
    for i in centers:
        if neighbor8[i]==0:
            fills2[i]=0
            blancos.add(i)
        if neighbor4[i]>2:
            if neighbor4[i]>3:
                blocked1.add(i)
                blocked0.add(i)
            else:
                blocked1.add(i)
    
    for i in centers:  #DONT DO THIS BECAUSE COURTYARD CENTER PATH
        neighbor8[i]=sum([ fills2[j] for j in connects8[i]])
        if neighbor8[i]==0:
            blancos.add(i)
        
    for i in edge:
        if neighbor4[i]>1:
            if neighbor4[i]>2:
                blocked1.add(i)
                blocked0.add(i)
            else:
                blocked1.add(i)
        
    for i in corners:
        if neighbor4[i]>0:
            if neighbor4[i]>1:
                blocked1.add(i)
                blocked0.add(i)
            else:
                blocked1.add(i)
       
    #zeros=list(all_zeros-blancos-blocked0) cant do this because COURTYARD CENTER PATH
    
    #zeros=list((all_zeros & (cc1|cc2))-blocked0 - blancos)
    zeros=list((all_zeros & (cc1|cc2))-blocked0 -blancos)
    ones=list((b1 & b2)-blocked1)
    print(zeros)
    print(ones)
    
    #print(b1)
    #print(b2)
    #print(zeros)
    #print(ones)
    #ones=list(all_ones-blocked1-blancos) can only do this for  
    
    #print("ones",ones)
    #print("zeros",zeros)
       
    Zeros=[zeros] #list of variations of open cell indices
    for k in ones:
        newzeros=list(zeros)
        newzeros.append(k)
        Zeros.append(newzeros)
    #Zeros=[zeros]
    #print("Z",Zeros)
    mini=H*W
    muni=H+W-1

    for i in range(len(Zeros)):
    #for i in [2]:
        #print("i",i,Zeros[i])
        path_stack=[[Zeros[i].pop(0),Zeros[i],1]]
        #print("path_stack",path_stack)
    
        while(len(path_stack)>0):
            possible=[]#empty list of possible paths
            while True:
                current=path_stack.pop()#pop path and remaining cells off stack
                head=current[0]#set path of interest           
                cells_left=current[1]#set cells left of interest
                length=current[2]
                if length <= shortest[head] or len(path_stack)==0:
                    break
             
            #print("head",head,"length",length)
            for i in range(len(cells_left)):#query remaining cells to see if possible next
                if cells_left[i] in nexts[head]:
                    possible.append(i) #if yes add index to possible list
            #print("next cells",[cells_left[i] for i in possible])
            for i in possible:#go through list of possible nexts
                #flag=False
                if cells_left[i]==N-1: #if its the end add to list of winning paths
                    new_length= length + 1
                    
                    if new_length==(muni):
                        #print("hi")
                        return new_length
                    else:
                        mini=min(new_length,mini)
                        #print("mini",mini)                        
                    #flag=True
                    break
                else:
                    save_left=list(cells_left)
                    save_head=save_left.pop(i)
                    path_stack.append([save_head,save_left,length+1])
                    if save_head in shortest:
                        shortest[save_head]=min(shortest[save_head],length+1)
                    else:
                        shortest[save_head]=length+1
                
    return mini
    
    

start_time=time.time()    
ans=answer(maze)
elapsed=time.time()-start_time
print(ans,elapsed)

