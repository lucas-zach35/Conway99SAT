##########
from pysat.card import *

graphOrder=9

nativeEdges={}
count=1
for i in range(0, graphOrder):
    for j in range(i+1, graphOrder):
        nativeEdges[str(i)+','+str(j)]=count
        nativeEdges[str(j)+','+str(i)]=count
        count+=1


#### start: common neighbor variables
#### (u, v, commonNeighborVertex)

commonNeighborVariables={}
for i in range(0, graphOrder):
    for j in range(i+1, graphOrder):
        for k in range(0, graphOrder):
            if i==k or j==k:
                continue
            commonNeighborVariables[str(i)+','+str(j)+','+str(k)]=count
            count+=1


reversedNativeEdges={}
for k in nativeEdges.keys():
    reversedNativeEdges[nativeEdges[k]]=k

reversedNeighborVariables={}
for k in commonNeighborVariables.keys():
    reversedNeighborVariables[commonNeighborVariables[k]]=k



### neighbor constraints
clauses=[]
### (-Q1 v e1 v e2) ^ (-Q1 v -e1 v e2) ^ (-Q1 v e1 v -e2) ^ (Q1 v -e1 v -e2)
for q in commonNeighborVariables.keys():
    #int(i),int(j),int(k)=q.split(',')
    u,v,commonNeighborVertex=[ele for ele in q.split(',')]
    # between u and commonNeighborVertex
    
    e1=nativeEdges[u+','+commonNeighborVertex]
    # between v and commonNeighborVertex
    e2=nativeEdges[v+','+commonNeighborVertex]
    qVar=commonNeighborVariables[q]


    #-Q1 v e1 v e2 
    clauses.append([-qVar,e1,e2])
    #-Q1 v -e1 v e2
    clauses.append([-qVar,-e1,e2])
    #-Q1 v e1 v -e2
    clauses.append([-qVar,e1,-e2])
    #Q1 v -e1 v -e2
    clauses.append([qVar,-e1,-e2])









from pysat.solvers import Solver, Minisat22

s = Solver(name='g4')
for c in clauses:
    s.add_clause(c)



naiveClausesIndices=list(range(1,graphOrder-1))
for b in range(1, 3):
    cnf = CardEnc.equals(lits=naiveClausesIndices,bound=b, encoding=1)
    ### convert the clauses
    ## for every pair of vertices
    for i in range(0, graphOrder):
        for j in range(i+1, graphOrder):
            newClausesDictionary={}
            newClauses=[]
            edgeVariable=nativeEdges[str(i)+','+str(j)]
            # if not connected 2 common neighbors
            # so either connected, or two common neighbors
            sharedNeighbors=[]
            for q in range(0, graphOrder):
                if q !=i and q!=j:
                    sharedNeighborVar=commonNeighborVariables[str(i)+','+str(j)+','+str(q)]
                    sharedNeighbors.append(sharedNeighborVar)
            assert(len(sharedNeighbors)==graphOrder-2)
            for z in range(1, graphOrder-1):
                newClausesDictionary[z]=sharedNeighbors[z-1]
            assert(len(newClausesDictionary.keys())==graphOrder-2)
            for c in cnf:
                if b==1:
                    newClause=[-edgeVariable]
                else:
                    newClause=[edgeVariable]
                #newClause=[]
                for var in c:
                    positive=var>0
                    try:
                        newClausesDictionary[abs(var)]
                    except KeyError:
                        newClausesDictionary[abs(var)]=count
                        count+=1
                    if positive:
                        newClause.append(newClausesDictionary[abs(var)])
                    else:
                        newClause.append(-newClausesDictionary[abs(var)])
                newClauses.append(newClause)
            assert(len(newClauses)==len(cnf.clauses))
            for c in newClauses:
                s.add_clause(c)
#sumsTo1Template=c

#assumptions=[ele for ele in range(1,60)]
print('Solving', flush=True)
s.solve()

## common neighbors variables make sense
for k in commonNeighborVariables.keys():
    u,v,commonNeighborVertex=k.split(',')
    result=s.get_model()[commonNeighborVariables[k]-1]
    # they are common neighbors
    edge1Variable=nativeEdges[u+','+commonNeighborVertex]
    edge2Variable=nativeEdges[v+','+commonNeighborVertex]
    edge1Result=s.get_model()[edge1Variable-1]>0
    edge2Result=s.get_model()[edge2Variable-1]>0
    if result>0:
        assert(edge1Result)
        assert(edge2Result)
    else:
        assert((not edge1Result) or (not edge2Result))

for k in nativeEdges.keys():
    u,v=k.split(',')
    edgeVariable=nativeEdges[k]


    commonNeighborsForTheseTwo=[]
    u,v=sorted([u,v])

    for j in range(0, graphOrder):
        if j==int(u) or j==int(v):
            continue
        commonNeighborsForTheseTwo.append(commonNeighborVariables[str(u)+','+str(v)+','+str(j)])
    assert(len(commonNeighborsForTheseTwo)==graphOrder-2)
    varResults=[]
    for neighborVar in commonNeighborsForTheseTwo:
        res=s.get_model()[neighborVar-1]
        if res>0:
            varResults.append(1)
        else:
            varResults.append(0)


    # 2 neighbors
    if s.get_model()[edgeVariable-1]<0:

        assert(sum(varResults)==2)
    # 1 neighbor
    else:
        assert(sum(varResults)==1)
print('Solution:')
print(s.get_model()[0:len(nativeEdges.keys())])


s.delete()