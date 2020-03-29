# simple port scanner
import socket
import threading
from queue import Queue

print_lock = threading.Lock()

server ='98.174.157.112'

def pscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # make socket stream
	try:
		con = s.connect((server,port))
		with print_lock:
			print('port',port,'is open')
		con.close()
       # return True
	except:
		pass

# to run multiple at once
def threader():
	while True:
		worker= q.get()
		pscan(worker)
		q.task_done()

q = Queue()

for x in range (30):
	t = threading.Thread(target = threader)
	t.daemon = True
	t.start()

for worker in range(1,101):
	q.put(worker)

q.join()
