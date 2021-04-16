username: kyrant
password: 1q2w

port 80 = nginx
port 81 = gunicorn

===CHMOD===
OCTAL: 
	owner	group	others
	r w x	r w x	r w x
	4 2 1	4 2 1	4 2 1

IP: ip a
MYSQL_ROOT_PASS: rootsql

mysql-user: tom@%
pass: Redhat@123456

===APACHE===
restart: /etc/init.d/apache2 restart
stop: /etc/init.d/apache2 stop
start: /etc/init.d/apache2 start

192.168.0.158 = API
192.168.0.111 = socket
