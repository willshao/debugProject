#step 2 formatic the heap object inforamtion 
import os
import sys
import csv
from pykd import *
_columeName=['object','size','count','max_size','max_address']
_columeName2=['object','size','address']

paras={}
def readcsvtoDict(filePath):
    f_data=[]
    with open(filePath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            f_data.append(row)
    return f_data

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

def findGCRootDict(dict):
    stacklist=[]
    for k,v in dict.items():
        stack=pykd.dbgCommand("!gcroot {}".format(str(v['address'])))
        stacklist.append(stack)
    return stacklist
def findGCRootaddress(address):    
        stack=pykd.dbgCommand("!gcroot {}".format(str(address)))
        return stack;   
def findGCRootlist(list):
    stacklist=[]
    for k in list:
        stack=pykd.dbgCommand("!gcroot {}".format(str(['address'])))
        stacklist.append(stack)
    return stacklist

def most_frequent(List): 
    counter = 0
    num = List[0]       
    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency> counter): 
            counter = curr_frequency 
            num = i   
    return num 

def getParamter(para,paraname):
    para_name=para.split('=')
    print(para_name)
    if(paraname==para_name[0]):
        return para_name[1]
    

def getObjects(exportpath,allfilepath):
    step=0
    picked=5000
    b=pykd.dbgCommand("!mex.feo -gen 2 -skip {} -first {}".format(step,picked))
    array = []
    dictlist={}
    objectInfoList={}
    needcheckedList=[]
    while(len(b.split("\n"))>2):
        
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
        step=step+5000
        
        #print("export count:{} step".format(step))
        #print("handled count:{}".format(len(objectInfoList)))
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
            if(len(addresslist)>60):
                print('\n'.join(map(str, addresslist[:20])))
            else:
                print('\n'.join(map(str, addresslist)))
     
    if(exportpath!=''):
        print("================Start Export....")  
        ExportDictToCSV(exportpath+'_all_data.csv',dictlist,_columeName)
        ExportListToCSV(exportpath+'_key_data.csv',addresslistall,_columeName2)
        print("================End Export")  
    key_f1_list=[]
    add=[]
    same=[]
    reduce=[]
    
    all_f1_list=[] 
    summary_dict={}
    if(allfilepath!=''):
        key_f1_list=readcsvtoDict(allfilepath+'_all_data.csv')
        
        for key1 in key_f1_list:
            if(dictlist.get(key1['object'])):
                compare_size=int(key1['size'])-int(dictlist[key1["object"]]['size'])
                compare_count=int(key1['count'])-int(dictlist[key1["object"]]['count'])
                compare_max_size=int(key1['max_size'])-int(dictlist[key1["object"]]['max_size'])                
                summary_dict[key1["object"]]={'object':key1["object"],'d1_size':dictlist[key1["object"]]['size'],'d2_size':key1['size'],'d1_count':dictlist[key1["object"]]['count'],'d2_count':key1['count'],'size_increase':compare_size,'count_increase':compare_count,'max_size_increase':compare_max_size,'max_addressfrom_d1':dictlist[key1["object"]]['max_address'],'max_addressfrom_d2':key1['max_address']}
        summary_dict =sorted(summary_dict.values(), key=lambda x: (x['count_increase'], x['size_increase']),reverse=True)
        #print(summary_dict)
        for v in summary_dict:
            print("object name:  {} |increse Count:  {} |Incease Size:  {} | Address_d1:    {} | address_d2: {}".format(v['object'],v['count_increase'], v['size_increase'],v['max_addressfrom_d1'],v['max_addressfrom_d2']))
        print("================End compare....")
    if(allfilepath!=''):
        print("================Start compare....")  
        key_f1_list=readcsvtoDict(allfilepath+'_key_data.csv')
        set1 = set((str(x["address"]),str(x["object"]),int(x["size"])) for x in addresslistall)
        set2 = set((str(x["address"]),str(x["object"]),int(x["size"])) for x in key_f1_list)
        add=[ x for x in key_f1_list if (str(x["address"]),str(x["object"]),int(x["size"])) not in set1 ]
        same=[ x for x in key_f1_list if (str(x["address"]),str(x["object"]),int(x["size"])) in set1 ]
        reduce=[ x for x in addresslistall if (str(x["address"]),str(x["object"]),int(x["size"])) not in set2 ]
        print("================Existed two dumps================")
        print('\n'.join(map(str, same)))
        print("================New dumps objects================")
        print('\n'.join(map(str, add)))
        print("================Old dumps objects================")
        print('\n'.join(map(str, reduce)))
        print("================Key Stacks======================")
        
        if(add):
            addstack=findGCRootlist(add)
            if(addstack):
                print(most_frequent(addstack))
        if(same):
            samestack=findGCRootlist(same)
            if(samestack):
                print(most_frequent(addstack))

        #test function
        #stack=findGCRootaddress('0275b0f4')
        #print(stack)
        #print('---------------')
        #stack=findGCRootaddress('032353a8')
        #print(stack)
        

def main():
    exportfilepath=''
    fallpath=''
    _f2path=''
    for arg in sys.argv[1:]:
        para_name=arg.split('=')
        if("exportpath"==para_name[0]):
            exportfilepath=para_name[1]
        
        if("fpath"==para_name[0]):
            fallpath=para_name[1]       
    getObjects(exportfilepath,fallpath)


if __name__ == "__main__":
    main()