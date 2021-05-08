import heapq#priority queue library
from copy import deepcopy#stops udpating lists that are equal before
import math#to take ceiling

#comparitive class so that we can sort puzzle states according to f(n)
class gamestate(object):

    def __init__(self,matrix):#matrix is combination of puzzle and g(n) and h(n)
        #f(n) = g(n) + h(n)
        self.gn = matrix[-1][0]
        self.hn = matrix[-1][1]
        self.fn = self.gn + self.hn
        self.state = matrix
        #current state
        self.gamestate=matrix[:-1]

    #prints the current puzzle, g(n) and h(n)
    def get(self):
        for i in range(n):
            print(self.gamestate[i])
        print("f(n):",self.fn,"g(n):",self.gn,"h(n):",self.hn,"\n")

    #comparison operator for f(n) for priority queue
    def __lt__(self,other):
        return self.fn<other.fn

    #returns true if this state is the solution
    def check_solution(self):
        solution = []
        for i in range(n):
            temp=[]
            for j in range(n):
                temp.append(n*(i)+j+1)
            solution.append(temp)
        solution[-1][-1]=0
        if self.gamestate==solution:return True
        return False

    #returns all possible puzzles
    def possible_state(self):
        return move(self.state)
    
#returns all the posible puzzles from current state
def move(matrix):

    x=y=0#empty piece's position
    board=matrix#actual board

    #finding empty piece location (x,y)
    for i in range(n):
        for j in range(n):
            if board[i][j]==0:x,y=i,j
            
    posible_states=[]
    #swap all possible positions (x,y) and return them
    if x>0:#can be shifted upwards
        temp=deepcopy(board)
        temp[x][y]=board[x-1][y]
        temp[x-1][y]=0
        posible_states.append(temp)
    if x<n-1:#can be shifted downwards
        temp=deepcopy(board)
        temp[x][y]=board[x+1][y]
        temp[x+1][y]=0
        posible_states.append(temp)
    if y>0:#can be shifted left
        temp=deepcopy(board)
        temp[x][y]=board[x][y-1]
        temp[x][y-1]=0
        posible_states.append(temp)
    if y<n-1:#can be shifted right
        temp=deepcopy(board)
        temp[x][y]=board[x][y+1]
        temp[x][y+1]=0
        posible_states.append(temp)
        
    return posible_states#list

def UC(possible_states):#return f(n) uniform cost for a puzzle
    for i in range(len(possible_states)):
        possible_states[i][-1][0]+=1#increment g(n)
    return possible_states

def MTH(possible_states):#returns f(n) for misplace tile heuristic
    possible_states = UC(possible_states)#update g(n)
    l = len(possible_states)# min 2 to max 4
    for i in range(l):
        hn = -1#h(n) is -1 so that its not overcounted by 1
        for j in range(n):#row
            for k in range(n):#column
                if possible_states[i][j][k] != n*(j)+k+1:#checks if given tile is at correct position
                    hn+=1
        possible_states[i][-1][1]=hn
    return possible_states

def MDH(possible_states):#returns f(n) for manhattan distance heuristic
    possible_states = UC(possible_states)
    l=len(possible_states)
    for i in range(l):#to calculate each ele of possible states
        hn=0
        for j in range(n):#row
            for k in range(n):#col
                if possible_states[i][j][k] == 0:continue
                x_pos = math.ceil(possible_states[i][j][k]/n)-1#expected x position
                y_pos = possible_states[i][j][k] - n*(x_pos) - 1#expected y position
                temp = abs(j-x_pos)+abs(k-y_pos)#the manhattan distance of a tile
                hn+=temp#adding the distance into overall heuristic
        possible_states[i][-1][1]=hn
    return possible_states

def insert_states(all_states,possible_state,heuristic):#inserts states into the queue according to given heuristic
    if heuristic==1:#uniform cost
        possible_state = UC(possible_state)
    if heuristic==2:#MTH
        possible_state = MTH(possible_state)
    if heuristic==3:#MDH
        possible_state = MDH(possible_state)
    for i in range(len(possible_state)):#traverses current possible states after a move 
        heap_state = gamestate(possible_state[i])#converted puzzle into gamestate object
        heapq.heappush(all_states,heap_state)#pushing above in priority queue by f(n)
    return all_states

print("***Welcome Prof. to my program to solve 8-puzzle game***")
print("***choose n=3 for 8-puzzle, n=4 for 15 puzzle and so on...***")
n = int(input())
print("***choose heuristic:***\n1 = uniforrm cost\n2 = Misplaced tile heuristic\n3 = Manhattan distance heuristic")
heuristic = int(input())
print("***choose 1 for in-built puzzles or 2 for custom puzzle***")
puzzle = int(input())

###default puzzles, depth of 0,2,4,8,12,16,20,24 respectively
states=[[[1, 2, 3], [4, 5, 6], [7, 8, 0]], [[1, 2, 3], [4, 5, 6], [0, 7, 8]], [[1, 2, 3], [5, 0, 6], [4, 7, 8]], [[1, 3, 6], [5, 0, 2], [4, 7, 8]], [[1, 3, 6], [5, 0, 7], [4, 8, 2]], [[1, 6, 7], [5, 0, 3], [4, 8, 2]], [[7, 1, 2], [4, 8, 5], [6, 3, 0]], [[0, 7, 2], [4, 6, 1], [3, 5, 8]]]
depth_table = {0:0,2:1,4:2,8:3,12:4,16:5,20:6,24:7}

if puzzle==1:
    print("***specify what depth of puzzle you want***\n***the available depths are 0,2,4,8,12,16,20,24***")
    depth = int(input())
    initial_state=states[depth_table[depth]]
else:
    initial_state=[]
    for i in range(n):
        print("enter",n,"spaced numbers in row",i+1,":", end = '')
        row = list(map(int, input().split()))   
        initial_state.append(row)
    
    
#prints the starting puzzle
print("initial puzzle: \n")
for i in range(n):
    print(initial_state[i])
print("\n")

#Introduction of pseudo-code

initial_state.append([0,0])#g(n), h(n)

#initializing initial puzzle into gamestate object and adding it to priority queue
g1=gamestate(initial_state)
all_states=[g1]
heapq.heapify(all_states)

count = 0#nodes explored
max_q_length = 0#maximum states in a queue at time

while(True):
    max_q_length = max(max_q_length,len(all_states))
    if (len(all_states)==0):print("no solution found")
    current = heapq.heappop(all_states)#state with min f(n) is popped
    if count>0:
        print("next best state:")
        current.get()#print the puzzle
    if current.check_solution():#if given state is solution
        print("Solution found!!!!\n")
        print("the depth of this puzzle was:",current.gn)
        print("the number of nodes expanded were:",count)
        print("the max queue length was:",max_q_length)
        break
    possible_states = current.possible_state()#all possible puzzle from this puzzle
    all_states = insert_states(all_states,possible_states,heuristic)#inserting them all into the queue
    count+=1#nodes expanded

