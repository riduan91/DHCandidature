import MySQLdb 

db = MySQLdb.connect("localhost","test","test","test" )
cursor = db.cursor()
cursor.execute("SELECT * FROM candidates")
data = cursor.fetchall()
#print "Database version : %s " % data
for line in data:
    print " ".join([str(col) for col in line]) 

print 'Success!'
db.close()
