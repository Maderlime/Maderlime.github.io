# connect to user Maddie
import pexpect 
# what is expected in prompt after submit
PROMPT =['# ','>>> ','> ','\$ ']

# function sends command with expected Prompt
# returns result of command
def send_command(child, cmd):
	child.sendline(cmd)
	child.expect(PROMPT)
	print child.before

# sends command with expecting login
# print result of login
def send_command2(child, cmd):
	child.sendline(cmd)
	child.expect('Maddie: ')
	send_command(child, 'rajawali')
	print child.before

# connect to host
def connect(user, host, password):
	ssh_newkey = 'are you sure you want to continue connecting'
	connStr ='ssh ' + user + '@' + host
    child = pexpect.spawn(connStr) # create new connection
    
    
	retV = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    
    # if timeout connection failed
	if retV == 0:
		print ('[-] Error connecting')
		return
    # if connecting asks question
	if retV ==1:
        child.sendline('yes') # return y
		retV = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
    
    # if error
	if retV ==0:
		print'[-] Error Connecting'
		return
    
    # if success to ask for password send pswrd
	child.sendline(password)
	child.expect(PROMPT)
	return child

# main method attempts to connect
def main():
	host = 'localhost'
	user ='Maddie'
	password = 'rajawali'
	child = connect(user, host, password)
	send_command2(child, 'sudo cat /etc/shadow | grep root')
if __name__ == '__main__':
	main()
