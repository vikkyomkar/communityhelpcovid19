FH = open('/mnt/covid/hotspots/hotspotArea.txt','r')
FH2 = open('/mnt/covid/hotspots/influxdata','w')
for line in FH:
	try:
		state,district,area,link=line.split('\t')
		statename = '_'.join(state.split(' '))
		districtname = '_'.join(district.split(' ')).strip()
		areaname = area.strip()
		FH2.write("hotspots,state={0},district={1} area=\"{2}\"\n".format(statename,districtname,areaname))
		print("hotspots,state={0},district={1} area=\"{2}\"").format(statename,districtname,areaname)
		#print(areaname)
	except Exception as e:
		print(e)
FH.close()
FH2.close()
