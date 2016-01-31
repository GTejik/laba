rules = 'Правила для ввода:\nПервая строка - алфавит\nДалее строки состояний в виде:\nсостояние-переходы-финальное?(1 или 0)\nПереходы разделяются пробелами\nЕсли переходов из одного состояния несколько, они разделяются запятой\nНачальное состояние помечается \'-\' в начале строки'

def simplify(regexp, chars):
    try:
        flag = False
        for c in regexp:        
            if chars == [] or c == '|' and not flag:
                chars.append([])
            if c == '|' and not flag:
                continue
            if c == '(' and not flag:
                chars[-1].append(c)
                flag = True
            elif c == ')' and flag:
                chars[-1][-1] += c
                flag = False
            elif flag:
                chars[-1][-1] += c
            elif c == '+' or c == '*':
                chars[-1][-1] += c
            else:
                chars[-1].append(c)
    except:
        pass

def chars_to_matrix(chars, matrix, states, fstate, estate):
    try:
        try:
            freestate = int(states[-1].replace('z', '')) + 1
        except:
            freestate = 0

        #to remember where we should stop for a+|b+ case
        endstates = []
        nchars = [['(']]

        nallterm = 0
        nalliter = 0
        nallstar = 0
        for char in chars:
            nterm = 0
            nstar = 0
            for term in char:
                nterm += 1
                nallterm += 1
                if term[-1] == '*':
                    nstar += 1
                    nallstar += 1
                if term[-1] == '*' or term[-1] == '+':
                    nalliter += 1
            #if all are '*' => change it to '+'
            #if nterm == nstar:
               # for char in chars:
                    #for term in char:
                       # nchars[-1][-1] += term[:-1] + '|'
                        #print(term, 'asd', nchars)
                       #chars[chars.index(char)][char.index(term)] = term.replace('*', '+')
        
        #nchars[-1][-1] = nchars[-1][-1][:-1] + nchars[-1][-1][-1:].replace('|', ')+')  
        #chars = nchars  
        #print('nchars', nchars)
        #if nallstar == nallterm:
        #    print('ALL ******************************')
        #if nallterm == nalliter:
        #    print('yes', nalliter, nallterm)

        #print(chars)

        oldstate = None
        state = fstate

        for char in chars:
            #print('char', char, chars)
            for i, term in enumerate(char):
                #if all terminals with '*' => make it possible to get to the end by any char
                if nallstar == nallterm:
                     matrix[states.index(state)][states.index(estate)] += term.replace('+', '').replace('*', '').replace('(', '').replace(')', '')
                #print('term', term, char)
                #if we need to loop
                repet = False
                #state for loop
                rstate = None
                if term[-1] == '*':
                    repet = True
                    oldstate = state
                    rstate = state
                    if i == len(char) - 1 and 'z' not in state and state != 's':
                        states[states.index(state)] = 'z' + state
                        estate = 'z' + state
                        rstate = estate
                        state = 'z' + state
                else:
                    if term[-1] == '+':
                        repet = True
                    if i == len(char) - 1:
                        if estate.replace('z', '') == state:
                            state = estate
                        if estate.replace('z', '') == fstate: 
                            fstate = estate
                        #fill pass
                        if '(' not in term and '+' not in term and '*' not in term and '|' not in term or len(term) == 2:
                            matrix[states.index(state)][states.index(estate)] += term.replace('+', '').replace('(', '').replace(')', '')
                        oldstate = state
                        state = fstate
                        if repet:
                            rstate = estate
                    else:
                        #new state
                        states.append(str(freestate))
                        #extend rows
                        for row in matrix:
                            row.append('')
                        #new row
                        matrix.append([''] * len(states))
                        #fill pass
                        if '(' not in term and '+' not in term and '*' not in term and '|' not in term or len(term) == 2:
                            matrix[states.index(state)][states.index(str(freestate))] += term.replace('+', '').replace('(', '').replace(')', '')
                        oldstate = state
                        state = str(freestate)
                        freestate += 1
                        if repet:
                            rstate = state
                #print('TEST', term, i, chars, nallterm, nalliter)
                if repet:
                    if nallterm == nalliter and len(chars) != 1 or term[-1] == '*' and i == len(char) - 1:
                        #print('popal', term, nalliter, nallterm, chars)
                        #new state
                        states.append('z' + str(freestate))
                        #extend rows
                        for row in matrix:
                            row.append('')
                        #new row
                        matrix.append([''] * len(states))
                        #fill pass
                        #if term[-1] == '+':
                        matrix[states.index(state)][states.index('z' + str(freestate))] = term.replace('+', '').replace('*', '').replace('(', '').replace(')', '')
                        matrix[states.index('z' + str(freestate))][states.index('z' + str(freestate))] = term.replace('+', '').replace('*', '').replace('(', '').replace(')', '') 
      
                        oldstate = state
                        #state = 'z' + str(freestate)
                        freestate += 1

                        endstates.append(state)
                    else:
                        if rstate == 's' and len(term) == 2 and i == len(char) - 1:
                            matrix[states.index(state)][states.index(estate)] += term.replace('*', '').replace('+', '').replace('(', '').replace(')', '')
                        if '(' not in term and '+' not in term and '*' not in term and '|' not in term or len(term) == 2:
                            matrix[states.index(rstate)][states.index(rstate)] += term.replace('+', '').replace('*', '').replace('(', '').replace(')', '')
                
                #now we don't need anything from z0, z1 etc. lead to z
                if nallterm == nalliter and len(chars) != 1:
                    for state in endstates:
                        for i, row in enumerate(matrix):
                            if i == states.index(state):
                                matrix[i][1] = ''

                if '(' in term or '|' in term:
                    #simplify regexp
                    x = []
                    simplify(term[:-1].replace('(', '').replace(')', ''), x)
                    if oldstate.replace('z', '') != state.replace('z', '') or not repet:
                        if i == len(char) - 1:
                            chars_to_matrix(x, matrix, states, oldstate, estate)
                        else:
                            chars_to_matrix(x, matrix, states, oldstate, state)
                    #if loop
                    if repet:
                        if rstate == 's' and i == len(char) - 1:
                            chars_to_matrix(x, matrix, states, rstate, estate)
                        chars_to_matrix(x, matrix, states, rstate, rstate)

    except:
        pass

def matrix_to_nka(matrix, states):
    try:
        result = {}

        result['fstate'] = 's'
        result['chars'] = ''

        #filling chars
        for from_, row in enumerate(matrix):
            for to_, elem in enumerate(row):
                for char in elem:
                    if char not in result['chars']:
                        result['chars'] += char
        #filling nka with 'e' // adding states
        for state in states:
            result[state] = ['e'] * len(result['chars'])
        #filling nka
        for from_, row in enumerate(matrix):
            for to_, elem in enumerate(row):
                for char in elem:
                    result[states[from_]][result['chars'].find(char)] += states[to_] + ','
        #deleting extra symbols 
        for key, states in result.items():
            for state in states:
                if state != 'e' and key != 'chars' and key != 'fstate':
                    result[key][result[key].index(state)] = state[1:-1]
        #marking final states
        for key in result.keys():
            if key != 'chars' and key != 'fstate':
                if 'z' in key:
                    result[key].append('1')
                else:
                    result[key].append('0')
        #addind 'e'-state
        result['e'] = ['e'] * len(result['chars'])
        result['e'].append('0')

        return result
    except:
        pass

def regexp_to_nka(regexp):
    try:
        chars = []
        
        simplify(regexp, chars)
        states = ['s', 'z']
        matrix = [['', ''], ['', '']]

        chars_to_matrix(chars, matrix, states, 's', 'z')

        return matrix_to_nka(matrix, states)
    except:
        pass

#read matrix from input.txt
def read_matrix():
    try:
        #read matrix
        matrix = {}
        #reading
        f = open('input.txt', 'r')
        #set of chars
        matrix['chars'] = f.readline().replace(' ', '').replace('\n', '')
        #first state
        matrix['fstate'] = ''
        #matrix
        for line in f:
            #matrix.append(line.split())
            a = line.split()
            #remember if first state
            if a[0][0] == '-':
                matrix['fstate'] += a[0][1:] + ','
                a[0] = a[0][1:]
            #remember row
            matrix[a[0]] = a[1:]
        #delete extra ','
        matrix['fstate'] = matrix['fstate'][:-1]
        f.close()
        return matrix
    except:
        return 'Не могу считать матриу, проверьте правильность ввода\n\n' + rules

#check string according to determinated state machine
def dka(string, matrix):
    try:
        state = matrix['fstate']
        chars = matrix['chars']
        for c in string:
            #if forbidden symbols, return false
            if c not in chars:
                return False
            state = matrix[state][chars.find(c)]
        #if it is final state - return true
        if matrix[state][-1] == '1':
            return True
        return False
    except:
        return 'Не могу проверить строку по детерминированной матрице, проверьете правильность ввода\n\n' + rules

#transform nka to dka
def nka_to_dka(matrix):
    try:
        result = {}

        chars = matrix['chars']
        fstate = matrix['fstate'].replace(',', '')

        result[fstate] = []

        #substitutuin 'z0' to '0'
        for key in matrix.keys():
            if key[0] == 'z' and len(key) == 2:
                for key1, states in matrix.items():
                    for state in states:
                        if key in state:
                            matrix[key1][matrix[key1].index(state)] = state.replace(key, key.replace('z', ''))
                matrix[key.replace('z', '')] = matrix.pop(key)
        #empty states
        queue = list(result.keys())
        #while all states are not filled
        values = []
        while queue != []:
            for states in queue:
                for state in states:
                    for char in chars:
                        if len(result[states]) > chars.find(char) and matrix[state][chars.find(char)].replace(',', '') not in result[states][chars.find(char)]:
                            result[states][chars.find(char)] += matrix[state][chars.find(char)].replace(',', '')
                        elif len(result[states]) <= chars.find(char):
                            result[states].append(matrix[state][chars.find(char)].replace(',', ''))
                        #deleting repetitions and 'e' in state if it is not equals 'e'
                        if result[states][chars.find(char)] != 'e':
                            ns = ''
                            for c in result[states][chars.find(char)].replace('e', ''):
                                if c not in ns:
                                    ns += c
                            result[states][chars.find(char)] = ''.join(sorted(ns))
                #remember all values
                values += result[states]
                #removing done state
                queue.remove(states)
            #adding new states to queue
            for next_state in result[states]:
                #print('                          ', next_state)
                #if '1' in states and we have new state '1z' => add '1' to states // make '1' = '1z'
                #if next_state[:-1] in values:
                #    result[next_state[:-1]] = []
                 #   queue.append(next_state[:-1])
                if next_state not in result.keys():
                    result[next_state] = []
                    queue.append(next_state)

        #mark final states
        for state, values in result.items():
            for old_state, old_values in matrix.items():
                if old_values[-1] == '1' and old_state != 'chars' and old_state != 'fstate' and old_state in state:
                    if len(values) <= len(chars):
                        values.append('1')
                    else:
                        values[-1] = '1'
                else:
                    if len(values) <= len(chars):
                        values.append('0')

        result['chars'] = chars
        result['fstate'] = fstate

        return result
    except:
        return 'не могу перевести матрицу к детерминированной, проверьте правильность ввода\n\n' + rules

#write matrix to file
def write_matrix(result):
    try:
        #write to file
        buff = [[c for c in result['chars']]]
        buff[-1] += ['\n']
        states = [result['fstate']]
        for state in result.keys():
            if state not in states and state != 'chars' and state != 'fstate':
                states.append(state)
        for state in states:
            buff.append([state])
            buff[-1] += result[state] + ['\n']
            if state == result['fstate']:
                buff[-1][0] = '-' + buff[-1][0]
        buff[-1].pop()

        f = open('input.txt', 'w')
        string = ''
        for arr in buff:
            f.write(' '.join(arr))
            string += ' '.join(arr)
        f.close()
    except:
        pass

#function to check if it is determinate 
def check(string, matrix):
    #try:
    if ',' in matrix['fstate']:
        matrix = nka_to_dka(matrix)
        write_matrix(matrix)
        return dka(string, matrix)

    for key, row in matrix.items():
        for s in row:
            if ',' in s and key != 'chars':
                matrix = nka_to_dka(matrix)
                write_matrix(matrix)
                return dka(string, matrix)
    #if it is determinate
    return dka(string, matrix)
    #except:
      #  return 'Не могу проверить на детерминированность, убедитесь в правильности ввода матрицы\n\n' + rules

#get right gramma
def rightGramma(matrix):
    try:
        result = ''
        chars = matrix['chars']
        keys = list(matrix.keys())
        keys.remove('fstate')
        keys.remove('chars')
        keys.sort()
        for key in keys:
            result += key + '::='
            for i in range(len(chars)):
                result += chars[i] + matrix[key][i] + '|'
            result = result[:-1]
            if matrix[key][-1] == '1':
                result += '|eps'
            result += '\n'
        return result
    except:
        return 'Не могу построить грамматику, убедитесь в правильности ввода матрицы\n\n' + rules