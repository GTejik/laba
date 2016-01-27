rules = 'Правила для ввода:\nПервая строка - алфавит\nДалее строки состояний в виде:\nсостояние-переходы-финальное?(1 или 0)\nПереходы разделяются пробелами\nЕсли переходов из одного состояния несколько, они разделяются запятой\nНачальное состояние помечается \'-\' в начале строки'

def simplify(regexp, chars):
	#print(regexp, chars)
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

def regexp_to_nka(regexp):
	chars = []

	simplify(regexp, chars)

	matrix = {}
	matrix['s'] = ['0']
	matrix['e'] = ['0']
	matrix['z'] = ['1']

	print(chars)

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

		#empty states
		queue = list(result.keys())
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
				#removing done state
				queue.remove(states)
			#adding new states to queue
			for next_state in result[states]:
				if next_state not in result.keys():
					result[next_state] = []
					queue.append(next_state)

		#mark final states
		for state, values in result.items():
			for old_state, old_values in matrix.items():
				if old_values[-1] == '1' and old_state != 'chars' and old_state in state:
					if values[-1] != '1' and values[-1] != '0':
						values.append('1')
					else:
						values[-1] = '1'
				else:
					if values[-1] != '1' and values[-1] != '0':
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
	try:
		if ',' in matrix['fstate']:
			matrix = nka_to_dka(matrix)
			write_matrix(matrix)
			return dka(string, matrix)

		for row in matrix.values():
			for s in row:
				if ',' in s:
					matrix = nka_to_dka(matrix)
					write_matrix(matrix)
					return dka(string, matrix)
	except:
		return 'Не могу проверить на детерминированность, убедитесь в правильности ввода матрицы\n\n' + rules

	#if it is determinate
	return dka(string, matrix)

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