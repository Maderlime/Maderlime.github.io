# give target host and port, returns the open and closed ports
import optparse
from socket import*
from threading import*

screenLock = Semaphore(value =1)
# function scans individual target host's port
# prints whether open or close
def connScan(tgtHost, tgtPort):
	try:
		connSkt = socket(AF_INET, SOCK_STREAM)
		connSkt.connect((tgtHost, tgtPort))
		connSkt.send('Test\r\n')
		results = connSkt.recv(100)
		screenLock.acquire()
		print ('[+] %d/tcp open' %tgtPort)
		print ('[+] ' + str(results))
	except:
		screenLock.acquire()
		print ('[-] %d/tcp closed' %tgtPort)
	finally:
		screenLock.release()
		connSkt.close()

# returns scan results for all ports in the one host
def portScan(tgtHost, tgtPorts):
	try:
		tgtIP = gethostbyname(tgtHost)
	except:
		print ("[-] Cannot resolve '%s': Unknown Host" %tgtHost)
		return
	try:
		tgtName = gethostbyaddr(tgtIP)
		print ('\n[+] Scan Results for: ' + tgtName[0])
	except:
		print ('\n[+]Scan results for:' + tgtIP)
	setdefaulttimeout(1)
	for tgtPort in tgtPorts:
		t = Thread(target =connScan, args=(tgtHost, int(tgtPort)))
		t.start()

def main():
    # user defines files and targets
	parser = optparse.OptionParser('usage %prog -H <target host> -p <target port>')
	parser.add_option('-H', dest = 'tgtHost', type = 'string', help = 'specify target host')
	parser.add_option('-p',dest ='tgtPort', type ='string', help = 'specify target port')
	parser.add_option('-D', dest = 'tgtDebug', default =False,action ='store_true',help='debugger')

	(options,args) = parser.parse_args()

	tgtHost = options.tgtHost
	tgtPorts = str(options.tgtPort).split(',')

	tgtDebug = options.tgtDebug

	if(tgtHost ==None)|(tgtPorts[0] == None):
		print ('You must specity a target host and port[s]')
		exit(0)
    
    # run port scan
	portScan(tgtHost,tgtPorts)

if __name__ == '__main__':
	main()

