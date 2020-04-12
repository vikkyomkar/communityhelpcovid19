import subprocess

def Post(db,postQuery):
	influxPost = "curl -i -XPOST 'http://localhost:8086/write?db={0}' --data-binary ".format(db)
	postData = '{0} "{1}"'.format(influxPost,postQuery)
	#print(postData)
	ps = subprocess.Popen(postData,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	#print(ps.communicate()[0])
