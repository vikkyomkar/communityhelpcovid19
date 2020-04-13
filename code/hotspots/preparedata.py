FH = open('/mnt/covid/hotspots/hotspotArea.txt','r')
FH2 = open('/mnt/covid/hotspots/influxdata','w')
for line in FH:
	state,district,area,link=line.split('\t')
	statename = '_'.join(state.split(' '))
	districtname='_'.join(district.split(' '))
	FH2.write("hotspots,state={0},district={1} area=\"{2}\"\n".format(statename,districtname,area))
	print("hotspots,state={0},district={1} area=\"{2}\"").format(statename,districtname,area)
	#print(line.split('\t'))

FH.close()
FH2.close()
