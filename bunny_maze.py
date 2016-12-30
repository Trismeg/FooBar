#FRESH START FOR GOOGLE MAZE CHALLENGE
#SAVE THE BUNNIES



def answer(maze):
    a=171
    c=30307
    X=30269
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
    
    topo={}
    for i in connects4:
        elem=set()
        for j in connects4[i]:
            if fills[j]==0:
                elem.add(j)
        topo[i]=elem
                
    
        
    bulk1={0:1}            
    for i in range(10000):        
        cell=0        
        while True:
            distance=bulk1[cell]
            unmapped_cells=[ j for j in topo[cell] if j not in bulk1 ]
            num_unmapped=len(unmapped_cells)
            if num_unmapped>0:
                X=(a*X+c)%num_unmapped
                cell=unmapped_cells[X]
                bulk1[cell]=distance+1
            else:
                low_mapped_cells=[ j for j in topo[cell] if (j in bulk1 and bulk1[j]>(distance+1 )) ]
                num_low_mapped=len(low_mapped_cells)
                if num_low_mapped > 0:
                    X=(a*X+c)%num_low_mapped
                    cell=low_mapped_cells[X]
                    bulk1[cell]=distance+1
                else:
                    even_mapped_cells=[ j for j in topo[cell] if (j in bulk1 and bulk1[j]==(distance+1 )) ]
                    num_even_mapped=len(even_mapped_cells)
                    if num_even_mapped > 0:
                        X=(a*X+c)%num_even_mapped
                        cell=even_mapped_cells[X]
                        distance +=1
                    else:
                        break
    
    #for i in bulk1:
    #    print(i,bulk1[i])
        
    
    bulk2={N-1:1}            
    for i in range(10000):        
        cell=N-1        
        while True:
            distance=bulk2[cell]
            unmapped_cells=[ j for j in topo[cell] if j not in bulk2 ]
            num_unmapped=len(unmapped_cells)
            if num_unmapped>0:
                cell=unmapped_cells[random.randint(0,num_unmapped-1)]
                bulk2[cell]=distance+1
            else:
                low_mapped_cells=[ j for j in topo[cell] if (j in bulk2 and bulk2[j]>(distance+1 )) ]
                num_low_mapped=len(low_mapped_cells)
                if num_low_mapped > 0:
                    cell=low_mapped_cells[random.randint(0,num_low_mapped-1)]
                    bulk2[cell]=distance+1
                else:
                    even_mapped_cells=[ j for j in topo[cell] if (j in bulk2 and bulk2[j]==(distance+1 )) ]
                    num_even_mapped=len(even_mapped_cells)
                    if num_even_mapped > 0:
                        cell=even_mapped_cells[random.randint(0,num_even_mapped-1)]
                        distance +=1
                    else:
                        break    
    
    #for i in bulk2:
    #    print(i,bulk2[i])
    #print(bulk2)
        
    ####### Two cases:  
    ####### Case 1: Exit is connected to entrance  
    #######       Case 1.1: Distance to exit is minimum
    #######       Case 1.2: Distance to exit could be minimized further
    ####### Case 2: Exit is connected
    
    is_unblocked = ( (N-1) in bulk1 )
    
    if is_unblocked:
        if bulk1[N-1]==MIN:
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
            print(neighbor4)
            
            
            minimum=N
            for i in ones:
                vals1=set()
                vals2=set()
                for j in connects4[i]:
                    if j in bulk1:
                        vals1.add(bulk1[j])
                    if j in bulk2:
                        vals2.add(bulk2[j])
                min1=min(vals1)
                min2=min(vals2)
                minimum=min(minimum,min1+min2+1)
            
            return minimum
        
    else: 
        #this is the case if split into two unconnected region
        #in this case find the shared border of the two connected components
        #and see what could happen from flipping these as above
        
        b1=set()
        for i in set(bulk1):
            for j in connects4[i]:
                if fills[j] == 1:
                    b1.add(j)
            
        b2=set()
        for i in set(bulk2):
            for j in connects4[i]:
                if fills[j] == 1:
                    b2.add(j)
                    
        ones = (b1 & b2)
        
        
        minimum=N
        for i in ones:
            vals1=set()
            vals2=set()
            for j in connects4[i]:
                if j in bulk1:
                    vals1.add(bulk1[j])
                if j in bulk2:
                    vals2.add(bulk2[j])
            min1=min(vals1)
            min2=min(vals2)
            minimum=min(minimum,min1+min2+1)
            
        return minimum
                    
                
    
maze=[[0,1,0,0,0,0,1,0,0,1],[0,0,0,1,0,0,0,0,1,1],[1,0,0,1,0,0,1,0,1,1],[0,1,0,1,0,0,1,0,0,1],[0,0,0,0,1,0,0,0,0,0],
      [0,1,0,0,1,0,0,0,0,0],[0,0,1,0,0,0,0,0,1,0],[0,0,0,1,0,0,0,1,1,1],[0,0,0,1,0,0,1,0,0,0],[0,0,1,0,0,0,1,0,0,0],
      [0,1,0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0,1,0],[1,1,1,0,0,0,1,0,0,0],[0,0,0,1,0,0,1,1,1,0],[0,0,0,1,0,0,0,1,0,0],
      [0,0,1,0,0,0,1,0,0,0],[0,0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1,1,1,1],[1,1,0,0,0,0,0,1,1,0],[0,0,0,0,0,0,0,0,0,0]]
print(answer(maze))
        
        
        
    
                
