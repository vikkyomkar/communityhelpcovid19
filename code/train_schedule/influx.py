import subprocess

def Post(db,postQuery):
	influxPost = 'curl -i -XPOST \"http://localhost:8086/write?db={0}\" --data-binary \'{1}\''.format(db,postQuery)
	#print(postData)
	ps = subprocess.Popen(influxPost,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	print(ps.communicate()[0])
