import time

class Timer:
	def __init__(self, start_now):
		self.running = False
		self.start_time = 0
		self.elaplsed_time = 0.0
		if start_now:
			self.start()
        
	def start(self):
		self.reset()
		self.resume()
	
	def stop(self):
		self.pause()
		self.print()
		self.reset()

	def pause(self):
		if not self.running:
			return
		
		t = time.perf_counter_ns()
		self.elaplsed_time += t - self.start_time
		self.running = False

	def resume(self):
		self.running = True
		self.start_time = time.perf_counter_ns()

	def reset(self):
		self.elaplsed_time = 0.0

	def print(self):
		t_ms = self.elaplsed_time / 1_000_000
		print(f'time(ms): {t_ms:,.2f}')

def test1(): 	   
	t = Timer(False)
	t.start()
	time.sleep(0.5)
	t.stop()

def test2():
	t = Timer(False)
	t.start()
	time.sleep(0.1)
	t.pause()
	time.sleep(0.5)
	t.resume()
	time.sleep(0.1)
	t.stop()

if __name__ == '__main__':
	test1()
	#test2()


