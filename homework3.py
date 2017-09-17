import queue, numpy,collections,copy,random,math

class Node:
    #newid = itertools.count(start=1)
    def __init__(self, state,rows, sums, diffs,num_lizards,row,col):
        #self.id = next(Node.newid)
        self.state = state
        #self.filled_rows = filled_rows
        self.sums = sums
        self.diffs = diffs
        self.rows = rows
        self.num_lizards = num_lizards
        self.row = row
        self.col = col
        #self.parent = parent
        #self.depth = depth
        #self.cost = cost


def SA():
    state = collections.defaultdict(list)
    rows = collections.defaultdict(list)
    sums = collections.defaultdict(list)
    diffs = collections.defaultdict(list)
    temp = 2000000
    if n*n -num_trees < num_lizards:
        return False
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
            while True:
                row = random.choice(range(n))
                if (row in Trows and column in Trows.get(row,[])[0]) or (row in state.get(column,[])):
                    continue
                break
            state[column].append(row)
            rows[row].append(column)
            sums[row+column].append((row,column))
            diffs[row-column].append((row,column))

    current = Node(state,rows,sums,diffs,num_lizards,None,None)
    '''print(state)
    print(rows)
    print(sums)
    print(diffs)
    print()
    print(Tcols)
    print(Trows)
    print(Tsums)
    print(Tdiffs)'''
    while temp > 0:

        currentConflicts = countConflicts(current)
        #print(current.state,currentConflicts)
        if(currentConflicts == 0):
            #print("Success in life")
            return current.state
        #print(countConflicts(state, rows, sums, diffs))
        #count = countConflicts(state,rows, sums, diffs)

        nextState = moveLizard(current)
        newConflicts = countConflicts(nextState)
        if newConflicts < currentConflicts:
            current = nextState
        else:
            val = math.exp(-(newConflicts - currentConflicts)/temp)
            if MakeMove(val):
                current = nextState
        temp = temp - 20

    return False

def moveLizard(node):
    col = random.choice(list(node.state.keys()))
    #print(col,node.state.get(col))
    row = random.choice(node.state.get(col))
    while True:
        c = random.choice(range(n))
        r = random.choice(range(n))
        if (r==row and c==col) or(r in Trows and c in Trows.get(r,[])[0]) or (r in node.state.get(c,[])) :
            continue
        break
    newNode = copy.deepcopy(node)
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
                #print(r,c)
            if next_hor_queen is not None and next_hor_tree is None and next_hor_queen > c:
                conflicts = conflicts +1
                #print(r,c)
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
                #print(r,c)
            if next_ver_queen is not None and next_ver_tree is None and next_ver_queen > r:
                conflicts = conflicts +1
                #print(r,c)
            #sum diagonal
            try:
                next_sum_tree =  next(x[1] for x in enumerate(sorted(Tsums.get(r+c,[]))) if (x[1][0] < r and x[1][1] > c))
            except StopIteration:
                next_sum_tree = None
            try:
                next_sum_queen = next(x[1] for x in enumerate(sorted(node.sums.get(r+c,[]))) if (x[1][0] < r and x[1][1] > c))
            except StopIteration:
                next_sum_queen = None
            if next_sum_queen is not None and next_sum_tree is not None and next_sum_queen[0] > next_sum_tree[0] and next_sum_queen[1]< next_sum_tree[1]:
                conflicts = conflicts + 1
                #print(r,c)
            if next_sum_queen is not None and next_sum_tree is None and next_sum_queen[0] < r  and next_sum_queen[1]> c:
                conflicts = conflicts + 1
                #print(r,c)
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
                #print(r,c)
            if next_diff_queen is not None and next_diff_tree is None and next_diff_queen[0] > r  and next_diff_queen[1] > c :
                conflicts = conflicts + 1
                #print(r,c)
    return conflicts

def Search():
    while True:
        if not nodes:
            return False
        node = nodes.popleft()
        if node.num_lizards > num_lizards:
            return False
        if goalTest(node):
            return node.state
        else:
            expand(node)
            # list(map(nodes.put, expand(node)))


def goalTest(node):
    if node.num_lizards < num_lizards:
        return False
    if node.num_lizards == num_lizards:
        return True

def expand(node):
    '''col = len(node.state)
    empty_rows_index = [x for x in range(n) if x not in node.state.values()]#list(set(range(n)) - set(list(node.filled_rows.keys())))
    empty_rows_index = [x for x in empty_rows_index if x+col not in node.sums.keys()]
    empty_rows_index = [x for x in empty_rows_index if x-col not in node.diffs.keys()]
    for row in empty_rows_index:
        temp_state = node.state.copy()
        temp_state.setdefault(col,row)
        #temp_filled_rows = node.filled_rows.copy()
        #temp_filled_rows.setdefault(row)
        temp_sums = node.sums.copy()
        temp_sums.setdefault(row+col,(row,col))
        temp_diffs = node.diffs.copy()
        temp_diffs.setdefault(row-col,(row,col))
        nodes.appendleft(Node(temp_state,temp_sums,temp_diffs))'''
    if len(node.state) == 0:
        column = 0
    else:
        column = list(node.state.keys())[-1]+1
    if algo == "DFS":
        next_possible_rows =[]
        for col in range(column,n):
            if len(Tcols.get(col,[])) == n:
                continue
            '''next_possible_rows = [x for x in range(n) if x not in Tcols.get(col,{})] # remove trees
            next_possible_rows = [x for x in next_possible_rows if next(y[1] for y in enumerate(Trows.get(x,{})) if y[1] > node.rows.get(x,{})[-1] and y[1] < col) ]
            next_possible_rows = [x for x in next_possible_rows if next(y[1] for y in enumerate(Tsums.get(x+col,{})) if y[1][1] > node.rows.get(x,{})[-1] and y[1][1] < col)]
            next_possible_rows = [x for x in next_possible_rows if next(y[1] for y in enumerate(Tdiffs.get(x-col,{})) if y[1][1] > node.rows.get(x,{})[-1] and y[1][1] < col)]'''
            for row in range(n):
                if row in Tcols.get(col,[]):
                    continue
                if len(node.rows.get(row,[])) and (any((t[0] > node.rows.get(row,[])[-1] and t[0] < col) for t in Trows.get(row,[])) == False):
                    continue
                if len(node.sums.get(row+col,[])) and (any((t[1] > node.sums.get(row+col,[])[-1][1] and t[1] < col) for t in Tsums.get(row+col,[])) == False):
                    continue
                if len(node.diffs.get(row-col,[])) and (any((t[1] > node.diffs.get(row-col,[])[-1][1] and t[1] < col)  for t in Tdiffs.get(row-col,[])) == False):
                    continue
                next_possible_rows.append(row)
            if next_possible_rows:
                column = col
                break


        for row in next_possible_rows:
            #state,rows, sums, diffs,num_lizards,row,col
            '''temp_state = copy.deepcopy(node.state.copy)
            temp_state[column].append(row)
            temp_rows = copy.deepcopy(node.rows.copy)
            temp_rows[row].append(column)
            temp_sums = copy.deepcopy(node.sums.copy)
            temp_sums[row+column].append((row,column))
            temp_diffs = copy.deepcopy(node.diffs.copy)
            temp_diffs[row-column].append((row,column))'''
            temp = copy.deepcopy(node)
            temp.state[column].append(row)
            temp.rows[row].append(column)
            temp.sums[row+column].append((row,column))
            temp.diffs[row-column].append((row,column))
            temp.row = row
            temp.col = column
            temp.num_lizards = node.num_lizards + 1
            if algo == "DFS":
                nodes.appendleft(temp)
            elif algo == "BFS":
                nodes.append(temp)
                #nodes.appendleft(temp)#Node(temp_state,temp_rows,temp_sums,temp_diffs,node.num_lizards+1,row,column))

        if node.row is not None and node.col is not None:
            try:
                first_tree_row =  next(x[1] for x in enumerate(Tcols.get(node.col,[])) if x[1] > node.row)
                if first_tree_row:
                    '''possible_rows = [x for x in range(first_tree_row+1,n) if x not in Tcols.get(node.col,{})] # remove trees
                    possible_rows = [x for x in possible_rows if next(y[1] for y in enumerate(Trows.get(x)) if y[1] > node.rows.get(x)[-1] and y[1] < node.col) ]
                    possible_rows = [x for x in possible_rows if next(y[1] for y in enumerate(Tsums.get(x+node.col)) if y[1][1] > node.rows.get(x)[-1] and y[1][1] < node.col)]
                    possible_rows = [x for x in possible_rows if next(y[1] for y in enumerate(Tdiffs.get(x-node.col)) if y[1][1] > node.rows.get(x)[-1] and y[1][1] < node.col)]'''

                    for row in range(first_tree_row+1,n):
                        #add check to see all are trees below
                        if row in Tcols.get(node.col,[]):
                            continue
                        if len(node.rows.get(row,[])) and (any((t[0] > node.rows.get(row,[])[-1] and t[0] < node.col) for t in Trows.get(row,[])) == False):
                            continue
                        if len(node.sums.get(row+node.col,[])) and (any((t[1] > node.sums.get(row+node.col,[])[-1][1] and t[1] < node.col)  for t in Tsums.get(row+node.col,[])) == False):
                            continue
                        if len(node.diffs.get(row-node.col,[])) and (any((t[1] > node.diffs.get(row-node.col,[])[-1][1] and t[1] < node.col) for t in Tdiffs.get(row-node.col,[])) == False):
                            continue
                        #state,rows, sums, diffs,num_lizards,row,col
                        '''temp_state = copy.deepcopy(node.state.copy)
                        temp_state[node.col].append(row)
                        temp_rows = copy.deepcopy(node.rows.copy)
                        temp_rows[row].append(node.col)
                        temp_sums = copy.deepcopy(node.sums.copy)
                        temp_sums[row+node.col].append((row,node.col))
                        temp_diffs = copy.deepcopy(node.diffs.copy)
                        temp_diffs[row-node.col].append((row,node.col))'''
                        temp = copy.deepcopy(node)
                        temp.state[node.col].append(row)
                        temp.rows[row].append(node.col)
                        temp.sums[row+node.col].append((row,node.col))
                        temp.diffs[row-node.col].append((row,node.col))
                        temp.row = row
                        temp.col = node.col
                        temp.num_lizards = node.num_lizards + 1
                        if algo == "DFS":
                            nodes.appendleft(temp)
                        elif algo == "BFS":
                            nodes.append(temp)
                            #nodes.appendleft(temp)#Node(temp_state,temp_rows,temp_sums,temp_diffs,node.num_lizards+1,row,node.col))
            except StopIteration:
                first_tree_row = False


    if algo == "BFS":
        if node.row is not None and node.col is not None:
            try:
                first_tree_row =  next(x[1] for x in enumerate(Tcols.get(node.col,[])) if x[1] > node.row)
                if first_tree_row:
                    '''possible_rows = [x for x in range(first_tree_row+1,n) if x not in Tcols.get(node.col,{})] # remove trees
                    possible_rows = [x for x in possible_rows if next(y[1] for y in enumerate(Trows.get(x)) if y[1] > node.rows.get(x)[-1] and y[1] < node.col) ]
                    possible_rows = [x for x in possible_rows if next(y[1] for y in enumerate(Tsums.get(x+node.col)) if y[1][1] > node.rows.get(x)[-1] and y[1][1] < node.col)]
                    possible_rows = [x for x in possible_rows if next(y[1] for y in enumerate(Tdiffs.get(x-node.col)) if y[1][1] > node.rows.get(x)[-1] and y[1][1] < node.col)]'''

                    for row in range(first_tree_row+1,n):
                        #add check to see all are trees below
                        if row in Tcols.get(node.col,[]):
                            continue
                        if len(node.rows.get(row,[])) and (any((t[0] > node.rows.get(row,[])[-1] and t[0] < node.col) for t in Trows.get(row,[])) == False):
                            continue
                        if len(node.sums.get(row+node.col,[])) and (any((t[1] > node.sums.get(row+node.col,[])[-1][1] and t[1] < node.col)  for t in Tsums.get(row+node.col,[])) == False):
                            continue
                        if len(node.diffs.get(row-node.col,[])) and (any((t[1] > node.diffs.get(row-node.col,[])[-1][1] and t[1] < node.col) for t in Tdiffs.get(row-node.col,[])) == False):
                            continue
                        #state,rows, sums, diffs,num_lizards,row,col
                        '''temp_state = copy.deepcopy(node.state.copy)
                        temp_state[node.col].append(row)
                        temp_rows = copy.deepcopy(node.rows.copy)
                        temp_rows[row].append(node.col)
                        temp_sums = copy.deepcopy(node.sums.copy)
                        temp_sums[row+node.col].append((row,node.col))
                        temp_diffs = copy.deepcopy(node.diffs.copy)
                        temp_diffs[row-node.col].append((row,node.col))'''
                        temp = copy.deepcopy(node)
                        temp.state[node.col].append(row)
                        temp.rows[row].append(node.col)
                        temp.sums[row+node.col].append((row,node.col))
                        temp.diffs[row-node.col].append((row,node.col))
                        temp.row = row
                        temp.col = node.col
                        temp.num_lizards = node.num_lizards + 1
                        if algo == "DFS":
                            nodes.appendleft(temp)
                        elif algo == "BFS":
                            nodes.append(temp)
                            #nodes.appendleft(temp)#Node(temp_state,temp_rows,temp_sums,temp_diffs,node.num_lizards+1,row,node.col))
            except StopIteration:
                first_tree_row = False

        next_possible_rows =[]
        for col in range(column,n):
            if len(Tcols.get(col,[])) == n:
                continue
            '''next_possible_rows = [x for x in range(n) if x not in Tcols.get(col,{})] # remove trees
            next_possible_rows = [x for x in next_possible_rows if next(y[1] for y in enumerate(Trows.get(x,{})) if y[1] > node.rows.get(x,{})[-1] and y[1] < col) ]
            next_possible_rows = [x for x in next_possible_rows if next(y[1] for y in enumerate(Tsums.get(x+col,{})) if y[1][1] > node.rows.get(x,{})[-1] and y[1][1] < col)]
            next_possible_rows = [x for x in next_possible_rows if next(y[1] for y in enumerate(Tdiffs.get(x-col,{})) if y[1][1] > node.rows.get(x,{})[-1] and y[1][1] < col)]'''
            for row in range(n):
                if row in Tcols.get(col,[]):
                    continue
                if len(node.rows.get(row,[])) and (any((t[0] > node.rows.get(row,[])[-1] and t[0] < col) for t in Trows.get(row,[])) == False):
                    continue
                if len(node.sums.get(row+col,[])) and (any((t[1] > node.sums.get(row+col,[])[-1][1] and t[1] < col) for t in Tsums.get(row+col,[])) == False):
                    continue
                if len(node.diffs.get(row-col,[])) and (any((t[1] > node.diffs.get(row-col,[])[-1][1] and t[1] < col)  for t in Tdiffs.get(row-col,[])) == False):
                    continue
                next_possible_rows.append(row)
            if next_possible_rows:
                column = col
                break


        for row in next_possible_rows:
            #state,rows, sums, diffs,num_lizards,row,col
            '''temp_state = copy.deepcopy(node.state.copy)
            temp_state[column].append(row)
            temp_rows = copy.deepcopy(node.rows.copy)
            temp_rows[row].append(column)
            temp_sums = copy.deepcopy(node.sums.copy)
            temp_sums[row+column].append((row,column))
            temp_diffs = copy.deepcopy(node.diffs.copy)
            temp_diffs[row-column].append((row,column))'''
            temp = copy.deepcopy(node)
            temp.state[column].append(row)
            temp.rows[row].append(column)
            temp.sums[row+column].append((row,column))
            temp.diffs[row-column].append((row,column))
            temp.row = row
            temp.col = column
            temp.num_lizards = node.num_lizards + 1
            if algo == "DFS":
                nodes.appendleft(temp)
            elif algo == "BFS":
                nodes.append(temp)
                #nodes.appendleft(temp)#Node(temp_state,temp_rows,temp_sums,temp_diffs,node.num_lizards+1,row,column))


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

nodes = collections.deque()
start = Node(collections.defaultdict(list),collections.defaultdict(list),collections.defaultdict(list),collections.defaultdict(list),0,None,None)
if algo == "DFS":
    nodes.appendleft(start)
elif algo == "BFS":
    nodes.append(start)

#already_present = collections.defaultdict(queue)
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
            output_file.write(''.join(map(str,line))+'\n')