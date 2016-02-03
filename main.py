rules = 'Правила для ввода:\nПервая строка - алфавит\nДалее строки состояний в виде:\nсостояние-переходы-финальное?(1 или 0)\nПереходы разделяются пробелами\nЕсли переходов из одного состояния несколько, они разделяются запятой\nНачальное состояние помечается \'-\' в начале строки'

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

#split by '|' outside of () // 'a|b' -> ['a', 'b']
def split_by_or(regexp):
    result = []
    #if no '|' -> done
    if regexp.find('|') == -1:
        return [regexp]
    #number of opened '(' if it is equals 0 -> we are outside of () now
    n = 0
    #position of '|' outside ()
    pos = 0
    for c in regexp:
        if n == 0 and c == '|':
            #appending result
            result.append(regexp[: pos])
            #deleting done string
            regexp = regexp[pos + 1 :]
            #now pos == 0
            pos = 0
        else:
            #counting ()
            if c == '(':
                n += 1
            elif c == ')':
                n -= 1
            pos += 1
    #appending result with rest
    result.append(regexp)
    return result

#split regexp by 'and' // 'a*b' -> ['a*', 'b'] 
def split_by_and(regexp):
    result = []
    #number of opened '(' if it is equals 0 -> we are outside of () now
    n = 0
    #position of the beggining of the part to add to result
    pos = 0
    for i, c in enumerate(regexp):  
        print('before', c, regexp, i, pos, result)
        #counting ()
        if c == '(':
            n += 1
        elif c == ')':
            n -= 1
        if c == '*' or c == '+' and n == 0:
            result[-1] += c
            pos = i + 1
            continue
        if n == 0:
            #appending result
            result.append(regexp[pos: i + 1])
            pos = i + 1
        print('after', c, regexp, i, pos, result)
    return result

def regexp_to_nka(regexp):

    print(split_by_and(regexp))
    

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