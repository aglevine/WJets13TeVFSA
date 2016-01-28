from sys import argv
import re

#qcdPrior = argv[1]
qcdNew =  argv[1]

f = open('runDYJets.cc','r+')
#g = open('runDYJets_new.cc' ,'w')
qcdStr = "int doQCD        = "
text = f.read()
newqcdStr = qcdStr+str(qcdNew)+";"
text = re.sub("int doQCD        = \d;",newqcdStr,text)
f.seek(0)
f.write(text)
f.truncate
f.close()
