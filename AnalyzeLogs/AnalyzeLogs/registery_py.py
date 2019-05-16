import os
print("Hello")
from pykd import *
dprintln("Hello")
#a=pykd.dbgCommand("r")
b=pykd.dbgCommand("!mex.feo -gen 2")
array = []
dictlist={}
_columeName=['object','size','count','max_size','max_address']

for line in b.split("\n"):
    #dprintln(line)
    if(line.startswith('0:')==False and line.startswith('Open')==False and line.endswith('objects found.\n')==False):
        #line=line.replace('<','_');
        #line=line.replace('>','_');
        _con=line.rstrip('\n').split();
        if(len(_con)<3):
            continue;   
        if(len(_con)>3):
            continue;
        if(_con[1]=='objects'):
            continue;
        #if(_con[1].gettype()!=int):
        #    continue;
        if(_con[2] in dictlist.keys()):
            dictlist[_con[2]]['size']+=int(_con[1])
            dictlist[_con[2]]['count']+=1
            if(dictlist[_con[2]]['max_size']<int(_con[1])):
                dictlist[_con[2]]['max_size']=int(_con[1])
                dictlist[_con[2]]['max_address']=_con[0]
        else:
            dictlist[_con[2]]={'object':_con[2],'size':int(_con[1]),'count':1,'max_size':int(_con[1]),'max_address':_con[0]}
itemList =sorted(dictlist.items(), key=lambda x: (dictlist[x]['count'], your_dict[x]['size']))

for key, obj in itemList.items():
    print(key)
    for attribute, value in obj.items():
        print('{} : {}'.format(attribute, value))