class MBI:
	block_size = 300
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
			if sum >= cls.block_val:
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
		width = self.getInterval(lv)
		start = self.len() - width
		if start < 0:
			return '0' * (width - self.len()) + self.val
		return self.val[start:]

	def moveToUpper(self, lv):
		removed = self.getInterval(lv)
		self.val = self.val[:-removed]

	

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

#		print(f'{lv}: {xCurrentIdx}, {yCurrentIdx}')
#		print(f'{lv}: {x.val}, {y.val}')

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

def leftEndIdx(lv):
	width = MBI.getInterval(lv)
	return '0' * width

def rightEndIdx(lv):
	width = MBI.getInterval(lv)
	return '9' * width

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
		a.add('1')
		return pathElem

def moveToPrevParentNode(idx, a, lv):
	if atRightEnd(idx, lv):
		return None
	else:
		_, pathElem = moveToLeftEnd(idx, lv)	
		a.subtract('1')
		return pathElem


#l = input()
#r = input()
l = '800003083030000000000000050500090000000000000000000078000001000000100000180150002050000000000000' 
r = '523830000000480000000090020070900300098000000000003000002000000190007000000000004200400020000000008'
solution(l, r)
