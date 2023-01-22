def solution(l, r):
	ll = list(l)
	rr = list(r)
	path = shortestPath(ll, rr)
	n = len(path)
	print(n)
	for tc in path:
		t = tc[0]
		c = tc[1]
		print(f'{t} {c}')

def shortestPath(x, y):
	#print(f'000 {x}, {y}')
	decrement1MBI(x)
	decrement1MBI(y)
	#print(f'010 minus1: {x}, {y}')

	leftPath = []
	rightPath = []

	lv = 0
	xCurrentIdx = getCurrentDigitsLv0(x)
	yCurrentIdx = getCurrentDigitsLv0(y)
	while True:
		#print(f'level {lv}: {xCurrentIdx}, {yCurrentIdx}')
		if equalsMBI(x, y):
			# In the same parent node
			#print('AAA x == y')
			if largerMBI(xCurrentIdx, yCurrentIdx):
				# Do not need to count nodes in this level
				break
			if atLeftEnd(xCurrentIdx, lv) and atRightEnd(yCurrentIdx, lv):
				leftPath.append((lv + 1, 1))
				break
			delta, _ = minusMBI(yCurrentIdx, xCurrentIdx)
			numOfNodes = mbi2Int(delta) + 1
			leftPath.append((lv, numOfNodes))
			#print(f'leftPath={leftPath}')
			break
		elif largerMBI(x, y):
			# x > y
			#print('BBB y < x')
			break
		else:
			#print('CCC x < y')
			xParentIdx, passingNodes = moveToNextParentNode(xCurrentIdx, x, lv)
			if passingNodes is not None:
				leftPath.append(passingNodes)
			#print(f'CCC 100 {xParentIdx}')
			yParentIdx, passingNodes = moveToPrevParentNode(yCurrentIdx, y, lv)
			if passingNodes is not None:
				rightPath.append(passingNodes)
			#print(f'CCC 999 {xParentIdx}, {yParentIdx}')

		xCurrentIdx = xParentIdx
		yCurrentIdx = yParentIdx
		lv += 1

	#print(f'999 {leftPath}, {rightPath}')
	return mergePath(leftPath, rightPath)
	

def mergePath(lp, rp):
	if len(rp) == 0:
		return lp
	firstRpElem = rp.pop()
	if lp[-1][0] == firstRpElem[0]:
		lp[-1] = (lp[-1][0], lp[-1][1] + firstRpElem[1])
	else:
		lp.append(firstRpElem)
	lp.extend(reversed(rp))
	return lp



def getCurrentDigitsLv0(a):
	d = list(a.pop())
	return d

def getCurrentDigits(a, lv):
	interval = getInterval(lv)
	result = []
	for i in range(interval):
		d = a.pop() if len(a) > 0 else '0'
		result.insert(0, d)
	return result

def atLeftEnd(idx, lv):
	return equalsMBI(idx, leftEndIdx(lv))

def atRightEnd(idx, lv):
	return equalsMBI(idx, rightEndIdx(lv))

def leftEndIdx(lv):
	width = getInterval(lv)
	return ['0' for _ in range(width)]

def rightEndIdx(lv):
	width = getInterval(lv)
	return ['9' for _ in range(width)]
		
def movToRightEnd(idx, a, lv):
	reIdx = rightEndIdx(lv)
	delta, _ = minusMBI(reIdx, idx)
	numOfNodes = mbi2Int(delta) + 1
	pathElem = (lv, numOfNodes)
	return reIdx, pathElem

def movToLeftEnd(idx, a, lv):
	leftEnd = leftEndIdx(lv)
	delta, _ = minusMBI(idx, leftEnd)
	numOfNodes = mbi2Int(delta) + 1
	pathElem = (lv, numOfNodes)
	return leftEnd, pathElem

def moveToNextParentNode(idx, a, lv):
	if atLeftEnd(idx, lv):
		pIdx = getCurrentDigits(a, lv+1)
		return pIdx, None
	else:
		reIdx, pathElem = movToRightEnd(idx, a, lv)	
		increment1MBI(a)
		pIdx = getCurrentDigits(a, lv+1)
		return pIdx, pathElem

def moveToPrevParentNode(idx, a, lv):
	if atRightEnd(idx, lv):
		pIdx = getCurrentDigits(a, lv+1)
		return pIdx, None
	else:
		reIdx, pathElem = movToLeftEnd(idx, a, lv)	
		decrement1MBI(a)
		pIdx = getCurrentDigits(a, lv+1)
		return pIdx, pathElem

# interval
# 0: X
# 1: 1  2-1 = 1
# 2: 2  4-2 = 2
# 3: 4
# 4: 8
def getInterval(lv):
	if lv == 0:
		return 1
	return 2**(lv-1)

def getEffectiveLenMBI(x):
	for i in range(len(x)):
		if x[i] != '0':
			return len(x) - i
	return 0

def allZerosMBI(x):
	for i in range(len(x)):
		if x[i] != '0':
			return False
	return True

# MyBigInt operation
# Check x == y or not
def equalsMBI(x, y):
	lenX = getEffectiveLenMBI(x)
	lenY = getEffectiveLenMBI(y)
	if lenX != lenY:
		return False

	if x == y:
		return True

	delta, carry = minusMBI(x, y)
	if carry:
		return False
	return allZerosMBI(delta)

# Check x > y or not
def largerMBI(x, y):
	lenX = getEffectiveLenMBI(x)
	lenY = getEffectiveLenMBI(y)

	if lenX > lenY:
		return True
	if lenX < lenY:
		return False

	if equalsMBI(x, y):
		return False
	delta, carry = minusMBI(x, y)
	if carry:
		return False
	return True

def plus1D(c):
	if c == '9':
		return '0', True	
	u = ord(c) + 1
	return chr(u), False

def minus1D(c):
	if c == '0':
		return '9', True	
	u = ord(c) - 1
	return chr(u), False

# Modify the input list
def decrement1MBI(x):
	carry = False
	for i in range(len(x)-1, -1, -1):
		x[i], carry = minus1D(x[i])
		if not carry:
			break
	return x, carry

# Mutable
def increment1MBI(x):
	if len(x) == 0:
		return x.append('1')

	carry = False
	for i in range(len(x)-1, -1, -1):
		x[i], carry = plus1D(x[i])
		if not carry:
			break
	if carry:
		x.insert(0, '1')
	return x

# Immutable
def minusMBIOld(x, y): # x - y (x > y)
	z = []
	carry = False
	for i in range(len(x)-1, -1, -1):
		tmp = x[i]
		if carry:
			tmp, carry = minus1D(tmp)
		tmp, carry1 = minusD(tmp, y[i])
		carry = carry or carry1
		z.append(tmp)
	return list(reversed(z)), carry

def minusMBI(x, y): # x - y (x >= y)
	BLOCK_SIZE = 10
	CARRY_VALUE = 10 ** BLOCK_SIZE
	xx = ''.join(x)
	yy = ''.join(y)

	length = (max(len(xx), len(yy)) // BLOCK_SIZE + 1) * BLOCK_SIZE

	xx = '0' * (length - len(xx)) + xx
	yy = '0' * (length - len(yy)) + yy

	result = ""
	carry = 0
	for i in range(length, 0, -BLOCK_SIZE):
		tmpX = int(xx[i - BLOCK_SIZE:i])
		tmpY = int(yy[i - BLOCK_SIZE:i])
		delta = tmpX - tmpY - carry
		if delta < 0:
			delta += CARRY_VALUE
			carry = 1
		else:
			carry = 0
		deltaS = str(delta)
		result = '0' * (BLOCK_SIZE - len(deltaS)) + deltaS + result

	result = trimZero(result)
	return list(result), carry > 0

def trimZero(x):
	for i in range(len(x)):
		if x[i] == '0':
			continue
		else:
			return x[i:]
	return ''


def mbi2Int(x):
	y = 0
	f = 1
	for i in range(len(x)-1, -1, -1):
		y += int(x[i]) * f
		f *= 10
	return y

def minusD(x, y):
	if x == y:
		return '0', False
	if x > y:
		z = ord(x) - ord(y) + ord('0')
		return chr(z), False
	# x < y
	z = 10 + ord(x) - ord(y) + ord('0')
	return chr(z), True


# Case 0: sample
l = "1"
r = "10"

# Case 1: same node
#l = "2"
#r = "4"

# Case 2: next node
#l = "2"
#r = "13"

# Case 3: next node AND parent is also next node
#l = "95"
#r = "106"

# Case 4-1: different nodes
#l = "3"
#r = "100"

# Case 4-2: different nodes
#l = "1"
#r = "95"

# Case 4-3: different nodes
#l = "2"
#r = "95"

# Case 4-4: different nodes
#l = "1"
#r = "100"

#l = "12345667"
#r = "2343526222"
#print(f'input: {l}, {r}')

l = input()
r = input()
solution(l, r)

