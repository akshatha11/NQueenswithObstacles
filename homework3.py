import collections,random,math,_pickle as cPickle
import time
timeout = time.time() + 60*4.8

class Node:
    def __init__(self, state,rows, sums, diffs, num_lizards, row, col):
        self.state = state
        self.sums = sums
        self.diffs = diffs
        self.rows = rows
        self.num_lizards = num_lizards
        self.row = row
        self.col = col
        self.hashCode = 0
        self.setHashCode()

    def setHashCode(self):
        self.hashCode = hash(((str(self.state))))


class SANode:
    def __init__(self, state,rows, sums, diffs, num_lizards, row, col):
        self.state = state
        self.sums = sums
        self.diffs = diffs
        self.rows = rows
        self.num_lizards = num_lizards
        self.row = row
        self.col = col




def SA():
    state = collections.defaultdict(list)
    rows = collections.defaultdict(list)
    sums = collections.defaultdict(list)
    diffs = collections.defaultdict(list)
    temp = 50000000
    if num_trees:
        for i in range(num_lizards):
            while True:
                column = random.choice(range(n))
                row = random.choice(range(n))
                if (row in Trows and column in Trows.get(row,[])[0]) or (row in state.get(column,[])):
                    continue
                break
            state[column].append(row)
            rows[row].append(column)
            sums[row+column].append((row,column))
            diffs[row-column].append((row,column))
    else:
        for column in range(n):
            if len(state) == num_lizards:
                break
            while True:
                row = random.choice(range(n))
                if (row in Trows and column in Trows.get(row,[])[0]) or (row in state.get(column,[])):
                    continue
                break
            state[column].append(row)
            rows[row].append(column)
            sums[row+column].append((row,column))
            diffs[row-column].append((row,column))


    current = SANode(state,rows,sums,diffs,num_lizards,None,None)
    while temp > 0:
        if time.time() >= timeout:
            break
        currentConflicts = countConflicts(current)
        if(currentConflicts == 0):
            return current.state
        nextState = moveLizard(current)
        newConflicts = countConflicts(nextState)
        if newConflicts < currentConflicts:
            current = nextState
        else:
            val = math.exp(-(newConflicts - currentConflicts)/temp)
            if MakeMove(val):
                current = nextState
        temp = temp - temp/math.log2(n+num_lizards)

    return False

def moveLizard(node):
    col = random.choice(list(node.state.keys()))
    row = random.choice(node.state.get(col))
    while True:
        c = random.choice(range(n))
        r = random.choice(range(n))
        if (r==row and c==col) or(r in Trows and c in Trows.get(r,[])[0]) or (r in node.state.get(c,[])) :
            continue
        break
    newNode = cPickle.loads(cPickle.dumps(node, -1))
    newNode.state[col].remove(row)
    if len(newNode.state[col]) == 0:
        del newNode.state[col]
    newNode.state[c].append(r)

    newNode.rows[row].remove(col)
    if len(newNode.rows[row]) == 0:
        del newNode.rows[row]
    newNode.rows[r].append(c)

    newNode.sums[row+col].remove((row,col))
    if len(newNode.sums[row+col]) == 0:
        del newNode.sums[row+col]
    newNode.sums[r+c].append((r,c))

    newNode.diffs[row-col].remove((row,col))
    if len(newNode.diffs[row-col]) == 0:
        del newNode.diffs[row-col]
    newNode.diffs[r-c].append((r,c))

    return newNode

def MakeMove(threshold):
    num = random.uniform(0, 1)
    if num <= threshold:
        return True
    else:
        return False


def countConflicts(node):
    conflicts = 0
    for c,row_list in node.state.items():
        for r in sorted(row_list):
            #horizontal
            try:
                next_hor_tree = next(x[1] for x in enumerate(sorted(Trows.get(r,[]))[0]) if x[1] > c)
            except StopIteration:
                next_hor_tree = None
            except IndexError:
                next_hor_tree = None
            try:
                next_hor_queen = next(x[1] for x in enumerate(sorted(node.rows.get(r,[]))) if x[1] > c)
            except StopIteration:
                next_hor_queen = None
            if next_hor_queen is not None and next_hor_tree is not None and next_hor_queen < next_hor_tree:
                conflicts = conflicts + 1
            if next_hor_queen is not None and next_hor_tree is None and next_hor_queen > c:
                conflicts = conflicts +1

            #vertical
            try:
                next_ver_tree =  next(x[1] for x in enumerate(sorted(Tcols.get(c,[]))) if x[1] > r)
            except StopIteration:
                next_ver_tree = None
            try:
                next_ver_queen = next(x[1] for x in enumerate(sorted(row_list)) if x[1] > r)
            except StopIteration:
                next_ver_queen = None
            if next_ver_queen is not None and next_ver_tree is not None and next_ver_queen < next_ver_tree:
                conflicts = conflicts + 1
            if next_ver_queen is not None and next_ver_tree is None and next_ver_queen > r:
                conflicts = conflicts +1

            #sum diagonal
            try:
                next_sum_tree = next(x[1] for x in enumerate(sorted(Tsums.get(r+c,[]),reverse=True)) if (x[1][0] < r and x[1][1] > c))
            except StopIteration:
                next_sum_tree = None
            try:
                next_sum_queen = next(x[1] for x in enumerate(sorted(node.sums.get(r+c,[]),reverse=True)) if (x[1][0] < r and x[1][1] > c))
            except StopIteration:
                next_sum_queen = None
            if next_sum_queen is not None and next_sum_tree is not None and next_sum_queen[0] > next_sum_tree[0] and next_sum_queen[1]< next_sum_tree[1]:
                conflicts = conflicts + 1
            if next_sum_queen is not None and next_sum_tree is None and next_sum_queen[0] < r and next_sum_queen[1]> c:
                conflicts = conflicts + 1

            #diff diagonal
            try:
                next_diff_tree =  next(x[1] for x in enumerate(sorted(Tdiffs.get(r-c,[]))) if (x[1][0] > r and x[1][1] > c))
            except StopIteration:
                next_diff_tree = None
            try:
                next_diff_queen = next(x[1] for x in enumerate(sorted(node.diffs.get(r-c,[]))) if (x[1][0] > r and x[1][1] > c))
            except StopIteration:
                next_diff_queen = None
            if next_diff_queen is not None and next_diff_tree is not None and next_diff_queen[0] < next_diff_tree[0] and next_diff_queen[1]< next_diff_tree[1]:
                conflicts = conflicts + 1
            if next_diff_queen is not None and next_diff_tree is None and next_diff_queen[0] > r  and next_diff_queen[1] > c :
                conflicts = conflicts + 1
    return conflicts

def Search():
    while True:
        if not nodes:
            return False
        if time.time() >= timeout:
            return False
        node = nodes.popleft()
        if goalTest(node):
            return node.state
        else:
            expand(node)

def goalTest(node):
    if node.num_lizards < num_lizards:
        return False
    if node.num_lizards == num_lizards:
        return True

def expand(node):
    if len(node.state) == 0:
        column = 0
    else:
        column = list(node.state.keys())[-1]+1
    if algo == "DFS":
        nextColExpansion(node,column)
        sameColExpansion(node)


    if algo == "BFS":
        sameColExpansion(node)
        nextColExpansion(node,column)



def nextColExpansion(node,column):
    next_possible_rows =[]
    for col in range(column,n):
        if len(Tcols.get(col,[])) == n:
            continue
        for row in range(n):
            if row in Tcols.get(col,[]):
                continue
            if len(node.rows.get(row,[])) and len(Trows.get(row,[]))==0 :
                continue
            if len(node.sums.get(row+col,[])) and len(Tsums.get(row+col,[]))==0 :
                continue
            if len(node.diffs.get(row-col,[])) and len(Tdiffs.get(row-col,[]))==0 :
                continue
            if len(node.rows.get(row,[])) and (any((t > node.rows.get(row,[])[-1] and t < col) for t in Trows.get(row,[])[0]) == False):
                continue
            if len(node.sums.get(row+col,[])) and (any((t[1] > node.sums.get(row+col,[])[-1][1] and t[1] < col) for t in Tsums.get(row+col,[])) == False):
                continue
            if len(node.diffs.get(row-col,[])) and (any((t[1] > node.diffs.get(row-col,[])[-1][1] and t[1] < col)  for t in Tdiffs.get(row-col,[])) == False):
                continue
            next_possible_rows.append(row)
        if next_possible_rows:
            column = col
            break


    for row in reversed(next_possible_rows):
        temp = cPickle.loads(cPickle.dumps(node, -1))
        temp.state[column].append(row)
        temp.rows[row].append(column)
        temp.sums[row+column].append((row,column))
        temp.diffs[row-column].append((row,column))
        temp.row = row
        temp.col = column
        temp.num_lizards = node.num_lizards + 1
        temp.setHashCode()
        if algo == "DFS":
            if temp.hashCode not in visited:
                nodes.appendleft(temp)
                visited[temp.hashCode] = 1
        elif algo == "BFS":
            if temp.hashCode not in visited:
                nodes.append(temp)
                visited[temp.hashCode] = 1


def sameColExpansion(node):
    if node.row is not None and node.col is not None:
        try:
            first_tree_row =  next(x[1] for x in enumerate(Tcols.get(node.col,[])) if x[1] > node.row)
            if first_tree_row:
                for row in range(first_tree_row+1,n):
                    #add check to see all are trees below
                    if row in Tcols.get(node.col,[]):
                        continue
                    if len(node.rows.get(row,[])) and len(Trows.get(row,[]))==0 :
                        continue
                    if len(node.sums.get(row+node.col,[])) and len(Tsums.get(row+node.col,[]))==0 :
                        continue
                    if len(node.diffs.get(row-node.col,[])) and len(Tdiffs.get(row-node.col,[]))==0 :
                        continue
                    if len(node.rows.get(row,[])) and (any((t > node.rows.get(row,[])[-1] and t < node.col) for t in Trows.get(row,[])[0]) == False):
                        continue
                    if len(node.sums.get(row+node.col,[])) and (any((t[1] > node.sums.get(row+node.col,[])[-1][1] and t[1] < node.col)  for t in Tsums.get(row+node.col,[])) == False):
                        continue
                    if len(node.diffs.get(row-node.col,[])) and (any((t[1] > node.diffs.get(row-node.col,[])[-1][1] and t[1] < node.col) for t in Tdiffs.get(row-node.col,[])) == False):
                        continue
                    #state,rows, sums, diffs,num_lizards,row,col
                    temp = cPickle.loads(cPickle.dumps(node, -1))
                    temp.state[node.col].append(row)
                    temp.rows[row].append(node.col)
                    temp.sums[row+node.col].append((row,node.col))
                    temp.diffs[row-node.col].append((row,node.col))
                    temp.row = row
                    temp.col = node.col
                    temp.num_lizards = node.num_lizards + 1
                    temp.setHashCode()
                    if algo == "DFS":
                        if temp.hashCode not in visited:
                            nodes.appendleft(temp)
                            visited[temp.hashCode] = 1
                    elif algo == "BFS":
                        if temp.hashCode not in visited:
                            nodes.append(temp)
                            visited[temp.hashCode] = 1
        except StopIteration:
            first_tree_row = None



# main
num_trees = 0
Trows = collections.defaultdict(list)
Tcols = collections.defaultdict(list)
Tsums = collections.defaultdict(list)
Tdiffs = collections.defaultdict(list)
with open('input.txt') as input_file:
    algo = input_file.readline().rstrip('\n')
    n = int(input_file.readline().rstrip('\n'))
    num_lizards = int(input_file.readline().rstrip('\n'))
    array = []
    for line in input_file:
        line = line.rstrip('\n')
        line = list(map(int, line))
        array.append(line)
        indices = [i for i, x in enumerate(line) if x == 2]
        if indices:
            num_trees = num_trees + len(indices)
            row = len(array)-1
            Trows[row].append(indices)
            for i in indices:
                Tcols[i].append(row)
                Tsums[i+row].append((row,i))
                Tdiffs[row -i].append((row,i))



if n*n -num_trees < num_lizards:
    result = False
elif num_trees == 0 and num_lizards>n:
    result = False
else:
    nodes = collections.deque()
    visited = {}
    start = Node(collections.defaultdict(list),collections.defaultdict(list),collections.defaultdict(list),collections.defaultdict(list),0,None,None)
    if algo == "DFS":
        nodes.appendleft(start)
        visited[start.hashCode] = 1
    elif algo == "BFS":
        nodes.append(start)
        visited[start.hashCode] = 1

    if algo == "SA":
        result = SA()
    else:
        result = Search()

with open('output.txt', 'w') as output_file:
    if(result == False):
        output_file.write("FAIL")
    else:
        output_file.write("OK\n")
        for c,v in result.items():
            for r in v:
                array[r][c] = 1
        for line in array:
            output_file.write(''.join(map(str,line))+'\r\n')
