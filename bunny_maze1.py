#FRESH START FOR GOOGLE MAZE CHALLENGE
#SAVE THE BUNNIES

def answer(maze):
    H=len(maze) #assign maze height
    W=len(maze[0]) #assign maze width
    N=H*W #number of cells
    LL=N-W #lower left index
    W2=2*W #useful calculation
    MIN=H+W-1#minimum possible path
    
    connects4={0:(1,W),W-1:(W-2,W2-1),LL:(LL-W,LL+1),N-1:(N-W-1,N-2)} #connectivity map for vectorized index of maze
    edges=[] #collect list of edge indices
    centers=[] #collect index of center indices
    corners=[W-1,LL] #collect index of corner indices (excluding beginning and end)
    
    
    for i in range(1,W-1): #count across
        connects4[i]=(i-1,i+1,i+W)
        connects4[LL+i]=(LL+i+1,LL+i-1,LL+i-W)        
        edges.append(i)
        edges.append(i+LL)

    for i in range(1,H-1):#count down
        Wi=W*i
        connects4[Wi]=(Wi+1,Wi+W,Wi-W)    
        connects4[Wi-1+W]=(Wi-2+W,Wi-1+W2,Wi-1)
        edges.append(Wi)
        edges.append(Wi-1+W)
        for j in range(1,W-1):
            connects4[Wi+j]=(Wi+j+1,Wi+j-1,Wi+j-W,Wi+j+W)
            centers.append(Wi+j)
            
    fills={}#values of maze at each vector index
    all_zeros=set()#set of indices with value 0
    all_ones=set()#set of indices with value 1
    
    for i in range(H):
        for j in range(W):
            index=W*i+j
            elem=maze[i][j]
            fills[index]=elem
            if elem:
                all_ones.add(index)
            else:
                all_zeros.add(index)
                
    '''cc1={0}
    

    while True:
        cc1_len=len(cc1)
        for i in set(cc1):
            for j in connects4[i]:
                if (j not in cc1) and (fills[j] == 0):
                    cc1.add(j)
        if cc1_len==len(cc1):
            break
    
    if N-1 in cc1:
        return MIN'''
                
                
    dm_bulk1={}#initialize minimum distance map from entrance (bulk)
    dm_edge1=[[0,1]]#initialize list of distance from entrance lists (edge)
    while len(dm_edge1)>0:
        print(len(dm_edge1))
        dm_edge1_temp=[]
        for i in dm_edge1:
            for j in connects4[i[0]]:
                if fills[j]==0:
                    if (j not in dm_bulk1) or ( (i[1]) <= dm_bulk1[j]):
                        dm_edge1_temp.append([j,i[1]+1])
        for i in dm_edge1:
            dm_bulk1[i[0]]=i[1]
        dm_edge1=dm_edge1_temp
    
    print(dm_bulk1)
        
    dm_bulk2={}#initialize minimum distance map from exit (bulk)
    dm_edge2=[[N-1,1]]#initialize list of distance from exit lists (edge)
    while len(dm_edge2)>0:
        dm_edge2_temp=[]
        for i in dm_edge2:
            for j in connects4[i[0]]:
                if fills[j]==0:
                    if (j not in dm_bulk2) or ( (i[1]) <= dm_bulk2[j]):
                        dm_edge2_temp.append([j,i[1]+1])
        for i in dm_edge2:
            dm_bulk2[i[0]]=i[1]
        dm_edge2=dm_edge2_temp
        
    maze_draw=list(maze)
    for i in range(H):
        for j in range(W):
            if maze[i][j]==1:
                maze_draw[i][j]='X'
            else:
                indeX=j+W*i
                if indeX in dm_bulk1:
                    maze_draw[i][j]=dm_bulk1[indeX]
                else:
                    if indeX in dm_bulk2:
                        maze_draw[i][j]=dm_bulk2[indeX]
    print(dm_bulk2)
    for i in maze_draw:
        print(i)
    #print(dm_bulk2)
        
    ####### Two cases:  
    ####### Case 1: Exit is connected to entrance  
    #######       Case 1.1: Distance to exit is minimum
    #######       Case 1.2: Distance to exit could be minimized further
    ####### Case 2: Exit is connected
    
    is_unblocked = ( (N-1) in dm_bulk1 )
    
    if is_unblocked:
        if dm_bulk1[N-1]==MIN:
            return MIN
        
        else:
        ### Identify all of the 1 cells that might improve exit path if flipped
        ### This is all of the 1 cells minus the ones that dont matter
        ### 1 cells in center surrounded by 3 or more 1 cells dont matter
        ### 1 cells on edge surrounded by 2 or more 1 cells dont matter
        ### 1 cells in corner surrounded by one or more 1 cells dont matter
            neighbor4={}
            for i in all_ones:
                neighbor4[i]=sum([ fills[j] for j in connects4[i]])
            print(neighbor4)
            possible_bad_ones=set()
            
            for i in centers:                
                if i in all_ones and neighbor4[i]>=3:
                    possible_bad_ones.add(i)                    
            for i in edges:
                if i in all_ones and neighbor4[i]>=2:
                    possible_bad_ones.add(i)                    
            for i in corners:
                if i in all_ones and neighbor4[i]>=1:
                    possible_bad_ones.add(i)
            
            ones = all_ones - possible_bad_ones
            print(ones)
            
            
            minimum=N
            for i in ones:
                vals1=set()
                vals2=set()
                for j in connects4[i]:
                    if j in dm_bulk1:
                        vals1.add(dm_bulk1[j])
                    if j in dm_bulk2:
                        vals2.add(dm_bulk2[j])
                min1=min(vals1)
                min2=min(vals2)
                minimum=min(minimum,min1+min2+1)
            
            return minimum
        
    else: 
        #this is the case if split into two unconnected region
        #in this case find the shared border of the two connected components
        #and see what could happen from flipping these as above
        
        b1=set()
        for i in set(dm_bulk1):
            for j in connects4[i]:
                if fills[j] == 1:
                    b1.add(j)
            
        b2=set()
        for i in set(dm_bulk2):
            for j in connects4[i]:
                if fills[j] == 1:
                    b2.add(j)
                    
        ones = (b1 & b2)
        print(ones)
        
        minimum=N
        for i in ones:
            vals1=set()
            vals2=set()
            for j in connects4[i]:
                if j in dm_bulk1:
                    vals1.add(dm_bulk1[j])
                if j in dm_bulk2:
                    vals2.add(dm_bulk2[j])
            min1=min(vals1)
            min2=min(vals2)
            minimum=min(minimum,min1+min2+1)
            
        return minimum
                    
                
    
maze=[[0,0,0,0,0,0,1,0,0,1],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,1,1],[1,1,1,0,1,0,1,0,0,0],
      [1,0,0,1,0,0,1,0,1,1],[0,1,0,1,0,0,1,0,0,1],[0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
      [0,1,0,0,1,0,0,0,0,0],[0,0,1,0,0,0,0,0,1,0],[1,1,1,1,1,1,1,1,1,1],[0,0,0,1,0,0,1,0,0,0],[0,0,1,0,0,0,1,0,0,0],
      [0,1,0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0,1,0],[1,1,1,0,0,0,1,0,0,0],[0,0,0,1,0,0,1,1,1,0],[0,0,0,1,0,0,0,1,0,0],
      [0,0,1,0,0,0,1,0,0,0],[0,0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1,1,1,1],[1,1,0,0,0,0,0,1,1,0],[0,0,0,0,0,0,0,0,0,0]]
print(answer(maze))
        
        
        
    
                
