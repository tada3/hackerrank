
class MBI:
	block_size = 10
	block_val = 10 ** block_size
	
	def __init__(self, v):
		self.val = v
		self.pos = 0

	@staticmethod
	def trimZero(x):
		for i in range(len(x)):
			if x[i] == '0':
				continue
			else:
				return x[i:]
		return '0'

	@classmethod
	def plus(cls, x, y):
		length = (max(len(x), len(y)) // cls.block_size + 1) * cls.block_size

		x = '0' * (length - len(x)) + x
		y = '0' * (length - len(y)) + y

		result = ""
		carry = 0
		for i in range(length, 0, -cls.block_size):
			tmpX = int(x[i - cls.block_size:i])
			tmpY = int(y[i - cls.block_size:i])
			sum = tmpX + tmpY + carry
			delta = tmpX - tmpY - carry
			if sum > cls.block_val:
				carry = 1
				sum -= cls.block_val
			else:
				carry = 0
			sumS = str(sum)
			result = '0' * (cls.block_size - len(sumS)) + sumS + result

		if carry > 0:
			result = '1' + result
		result = cls.trimZero(result)
		return result


	@classmethod
	def minus(cls, xx, yy): # x - y (x >= y)

		length = (max(len(xx), len(yy)) // cls.block_size + 1) * cls.block_size

		xx = '0' * (length - len(xx)) + xx
		yy = '0' * (length - len(yy)) + yy

		result = ""
		carry = 0
		for i in range(length, 0, -cls.block_size):
			tmpX = int(xx[i - cls.block_size:i])
			tmpY = int(yy[i - cls.block_size:i])
			delta = tmpX - tmpY - carry
			if delta < 0:
				delta += cls.block_val
				carry = 1
			else:
				carry = 0
			deltaS = str(delta)
			result = '0' * (cls.block_size - len(deltaS)) + deltaS + result

		result = cls.trimZero(result)
		return result, carry > 0

	@classmethod
	def equals(cls, x, y):
		lenX = len(x)
		lenY = len(y)
		if lenX != lenY:
			return False

		if x == y:
			return True

		delta, carry = cls.minus(x, y)
		if carry:
			return False
		return delta == '0'

	# Check x > y or not
	@classmethod
	def larger(cls, x, y):
		lenX = len(x)
		lenY = len(y)

		if lenX > lenY:
			return True
		if lenX < lenY:
			return False

		if x == y:
			return False

		delta, carry = cls.minus(x, y)
		if carry:
			return False
		return delta != '0'

	@classmethod
	def getInterval(cls, lv):
		if lv == 0:
			return 1
		return 2**(lv-1)

	@classmethod
	def getWidth(cls, lv):
		return 2**lv

	def len(self):
		return len(self.val)

	def add(self, x):
		y = self.plus(self.val, x)
		self.val = y

	def subtract(self, x):
		# Assume selv.val >= x, so ignore the second return val of minus()
		y, _ = self.minus(self.val, x)
		self.val = y

	def getCurrentDigits(self, lv):
		width = self.getWidth(lv)
		prevWidth = self.getWidth(lv - 1) if lv >= 1 else 0
		len = width - prevWidth

		end = self.len() - prevWidth
		if end < 0:
			return '0' * len
		start = self.len() - width
		if start < 0:
			return '0' * (len - end) + self.val[:end]
		return self.val[start:end]

	def moveToUpper(self, lv):
		width = self.getWidth(lv)
		self.val = self.val[:-width] + '0' * width

	

def solution(l, r):
	path = shortestPath(l, r)
	n = len(path)
	print(n)
	for tc in path:
		t = tc[0]
		c = tc[1]
		print(f'{t} {c}')

def shortestPath(l, r):
	x = MBI(l)
	x.subtract('1')
	y = MBI(r)
	y.subtract('1')
	leftPath = []
	rightPath = []
	lv = 0
	while True:
		xCurrentIdx = x.getCurrentDigits(lv)
		x.moveToUpper(lv)
		yCurrentIdx = y.getCurrentDigits(lv)
		y.moveToUpper(lv)

		if MBI.equals(x.val, y.val):
			# In the same parent node
			if MBI.larger(xCurrentIdx, yCurrentIdx):
				# Do not need to count nodes in this level
				break
			if atLeftEnd(xCurrentIdx, lv) and atRightEnd(yCurrentIdx, lv):
				leftPath.append((lv + 1, 1))
				break
			delta, _ = MBI.minus(yCurrentIdx, xCurrentIdx)
			numOfNodes = MBI.plus(delta, '1')
			leftPath.append((lv, numOfNodes))
			break
		elif MBI.larger(x.val, y.val):
			# x > y
			break

		passingNodes = moveToNextParentNode(xCurrentIdx, x, lv)
		if passingNodes is not None:
			leftPath.append(passingNodes)
		passingNodes = moveToPrevParentNode(yCurrentIdx, y, lv)
		if passingNodes is not None:
			rightPath.append(passingNodes)		
		lv += 1

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

def atLeftEnd(idx, lv):
	return MBI.equals(idx, leftEndIdx(lv))

def atRightEnd(idx, lv):
	return MBI.equals(idx, rightEndIdx(lv))

def rightEndIdx(lv):
	width = MBI.getInterval(lv)
	return '9' * width

def leftEndIdx(lv):
	width = MBI.getInterval(lv)
	return '0' * width

def moveToRightEnd(idx, lv):
	reIdx = rightEndIdx(lv)
	delta, _ = MBI.minus(reIdx, idx)
	numOfNodes = MBI.plus(delta, '1')
	pathElem = (lv, numOfNodes)	
	return reIdx, pathElem

def moveToLeftEnd(idx, lv):
	leftEnd = leftEndIdx(lv)
	delta, _ = MBI.minus(idx, leftEnd)
	numOfNodes = MBI.plus(delta, '1')
	pathElem = (lv, numOfNodes)
	return leftEnd, pathElem

def moveToNextParentNode(idx, a, lv):
	if atLeftEnd(idx, lv):
		return None
	else:
		_, pathElem = moveToRightEnd(idx, lv)	
		one = '1' + '0' * MBI.getWidth(lv)
		a.add(one)
		return pathElem

def moveToPrevParentNode(idx, a, lv):
	if atRightEnd(idx, lv):
		return None
	else:
		_, pathElem = moveToLeftEnd(idx, lv)	
		one = '1' + '0' * MBI.getWidth(lv)
		a.subtract(one)
		return pathElem



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

