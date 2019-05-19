#step 2 export to CSV function module
import os
import sys
import csv
from pykd import *
_columeName=['object','size','count','max_size','max_address']
_columeName2=['object','size','address']


def ExportDictToCSV(filename,dictlist,columeName):    
    with open(filename, 'w') as f1:
        writer = csv.DictWriter(f1,lineterminator='\n', fieldnames=columeName)
        writer.writeheader()
        for key, values in dictlist.items():
            writer.writerow(values)


def ExportListToCSV(filename,list,columeName):    
    with open(filename, 'w') as f1:
        writer = csv.DictWriter(f1,lineterminator='\n', fieldnames=columeName)
        writer.writeheader()
        for values in list:
            writer.writerow(values)


def getObjects(exportpath,allfilepath):
    step=0
    picked=1000
    b=pykd.dbgCommand("!mex.feo -gen 2 -skip {} -first {}".format(step,picked))
    
    array = []
    dictlist={}
    objectInfoList={}
    needcheckedList=[] 
    while(len(b.split("\n"))>1):
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
                    objectInfoList[_con[2]].append({'object':_con[2],'size':int(_con[1]),'address':_con[0]})
                else:
                    dictlist[_con[2]]={'object':_con[2],'size':int(_con[1]),'count':1,'max_size':int(_con[1]),'max_address':_con[0]}
                    objectInfoList.setdefault(_con[2], []);
                    objectInfoList[_con[2]].append({'object':_con[2],'size':int(_con[1]),'address':_con[0]})
        step=step+1000
        print(step)
        b=pykd.dbgCommand("!mex.feo -gen 2 -skip {} -first {}".format(step,picked))
    
    itemList =sorted(dictlist.values(), key=lambda x: (x['count'], x['size']),reverse=True)
    addresslistall=[]
    for obj in itemList[:60]:
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
            addresslistall.extend(addresslist)
            if(len(addresslist)>40):
                print('\n'.join(map(str, addresslist[:40])))
            else:
                print('\n'.join(map(str, addresslist)))
     
    if(exportpath!=''):
        print("Start Export....")  
        ExportDictToCSV(exportpath+'_all_data.csv',dictlist,_columeName)
        ExportListToCSV(exportpath+'_key_data.csv',addresslistall,_columeName2)
        print("End Export")  

def main():
    exportfilepath=''
    fallpath=''
    for arg in sys.argv[1:]:
        para_name=arg.split('=')
        if("exportpath"==para_name[0]):
            exportfilepath=para_name[1]
        if("fpath"==para_name[0]):
            fallpath=para_name[1]       
    getObjects(exportfilepath,fallpath)
if __name__ == "__main__":
    main()
