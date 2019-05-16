#step 2 formatic the heap object inforamtion 
import os
from pykd import *
#a=pykd.dbgCommand("r")
b=pykd.dbgCommand("!mex.feo -gen 2")
array = []
dictlist={}
#need stor address and size for every object, need use gcroot and objsize find content 
_columeName=['object','size','count','max_size','max_address']
objectInfoList={}
needcheckedList=[] 
for line in b.split("\n"):
    if(line.startswith('0:')==False and line.startswith('Open')==False and line.endswith('objects found.\n')==False):
        _con=line.rstrip('\n').split();
        if(len(_con)<3):
            continue;   
        if(len(_con)>3):
            continue;
        if(_con[1]=='objects'):
            continue;
        if(_con[2] in dictlist.keys()):
            dictlist[_con[2]]['size']+=int(_con[1])
            dictlist[_con[2]]['count']+=1
            if(dictlist[_con[2]]['max_size']<int(_con[1])):
                dictlist[_con[2]]['max_size']=int(_con[1])
                dictlist[_con[2]]['max_address']=_con[0]
            objectInfoList[_con[2]].append({'size':int(_con[1]),'address':_con[0]})
        else:
            dictlist[_con[2]]={'object':_con[2],'size':int(_con[1]),'count':1,'max_size':int(_con[1]),'max_address':_con[0]}
            objectInfoList.setdefault(_con[2], []);
            objectInfoList[_con[2]].append({'size':int(_con[1]),'address':_con[0]})
itemList =sorted(dictlist.values(), key=lambda x: (x['count'], x['size']),reverse=True)
for obj in itemList[:50]:
    print('=======================================================')
    print('Type:{}'.format(obj['object']))
    print('Size:{}'.format(obj['size']))
    print('Count:{}'.format(obj['count']))
    print('MaxSize:{}'.format(obj['max_size']))    
    print('address List')
    print('...................................')
    if(objectInfoList[obj['object']]):
        print('{} address List:'.format(obj['object']))
        addresslist=objectInfoList[obj['object']];
        addresslist=sorted(addresslist, key=lambda x: x['size'],reverse=True)
        if(len(addresslist)>10):
            print(addresslist[:10])
        else:
            print(addresslist)   