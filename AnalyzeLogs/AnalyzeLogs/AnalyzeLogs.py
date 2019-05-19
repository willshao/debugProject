#fname='C:/test/testcontent.txt'
#array = []
#dictlist={}
#_columeName=['object','size','count','max_size','max_address']
#with open(fname,"r") as f:
#    content = f.readlines()
## you may also want to remove whitespace characters like `\n` at the end of each line
#for line in content:
#    if(line.startswith('00')):
#        _con=line.rstrip('\n').split();

#        if(_con[2] in dictlist.keys()):
#            dictlist[_con[2]]['size']+=int(_con[1])
#            dictlist[_con[2]]['count']+=1
#            if(dictlist[_con[2]]['max_size']<int(_con[1])):
#                dictlist[_con[2]]['max_size']=int(_con[1])
#                dictlist[_con[2]]['max_address']=_con[0]
#        else:
#            dictlist[_con[2]]={'object':_con[2],'size':int(_con[1]),'count':1,'max_size':int(_con[1]),'max_address':_con[0]}
            
##print(dictlist)
## export data to csv
#import csv
#with open(fname+'_.csv', 'w') as f1:
#    writer = csv.DictWriter(f1,lineterminator='\n', fieldnames=_columeName)
#    writer.writeheader()
#    for key, values in dictlist.items():
#        #row = [key] + [value for item in values.items() for value in item]
#        writer.writerow(values)

def exportCSVFile(filepath):
    array = []
    dictlist={}
    _columeName=['object','size','count','max_size','max_address']
    with open(filepath,"r") as f:
        #content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
        for line in f:
            if(line.startswith('0:')==False and line.startswith('Open')==False and line.endswith('objects found.\n')==False):
                line=line.replace('<','_');
                line=line.replace('>','_');
                _con=line.rstrip('\n').split();
                if(len(_con)==2):
                    _con.insert(2,'NO_Object');   
                if(len(_con)>3):
                    continue;
                if(_con[2] in dictlist.keys()):
                    dictlist[_con[2]]['size']+=int(_con[1])
                    dictlist[_con[2]]['count']+=1
                    if(dictlist[_con[2]]['max_size']<int(_con[1])):
                        dictlist[_con[2]]['max_size']=int(_con[1])
                        dictlist[_con[2]]['max_address']=_con[0]
                else:
                   dictlist[_con[2]]={'object':_con[2],'size':int(_con[1]),'count':1,'max_size':int(_con[1]),'max_address':_con[0]}
            
    #print(dictlist)
    # export data to csv
    ExportDictToCSV(filepath+'_new_.csv',dictlist,_columeName)    
    return dictlist 

def CompareDict( d1,d2):
    intersect_keys,b,c,d,e=dict_compare(d1, d2)
    dict_comp={}
    for key in intersect_keys:
            compare_size=int(d2[key]['size']-d1[key]['size'])
            compare_count=int(d2[key]['count']-d1[key]['count'])
            compare_max_size=int(d2[key]['max_size']-d1[key]['max_size'])
            dict_comp[key]={'object':key,'d1_size':d1[key]['size'],'d2_size':d2[key]['size'],'d1_count':d1[key]['count'],'d2_count':d2[key]['count'],'size_increase':compare_size,'count_increase':compare_count,'max_size_increase':compare_max_size,'max_addressfrom_d1':d1[key]['max_address'],'max_addressfrom_d2':d2[key]['max_address']}
    
    return dict_comp
def CompareDictForAdd( d1,d2):
    intersect_keys,b,c,d,e=dict_compare(d1, d2)
    dict_comp={}
    for key in b:
            compare_size=int(d2[key]['size'])
            compare_count=int(d2[key]['count'])
            compare_max_size=int(d2[key]['max_size'])
            dict_comp[key]={'object':key,'d1_size':0,'d2_size':d2[key]['size'],'d1_count':0,'d2_count':d2[key]['count'],'size_increase':compare_size,'count_increase':compare_count,'max_size_increase':compare_max_size,'max_addressfrom_d1':0,'max_addressfrom_d2':d2[key]['max_address']}
    
    return dict_comp   
def CompareDictForSame( d1,d2):
    intersect_keys,b,c,d,e=dict_compare(d1, d2)
    dict_comp={}
    for key in intersect_keys:
            compare_size=int(d2[key]['size']-d1[key]['size'])
            compare_count=int(d2[key]['count']-d1[key]['count'])
            compare_max_size=int(d2[key]['max_size']-d1[key]['max_size'])
            dict_comp[key]={'object':key,'d1_size':d1[key]['size'],'d2_size':d2[key]['size'],'d1_count':d1[key]['count'],'d2_count':d2[key]['count'],'size_increase':compare_size,'count_increase':compare_count,'max_size_increase':compare_max_size,'max_addressfrom_d1':d1[key]['max_address'],'max_addressfrom_d2':d2[key]['max_address']}
    
    return dict_comp   
def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    removed = d1_keys - d2_keys
    added = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return intersect_keys,added, removed, modified, same

def ExportDictToCSV(filename,dictlist,_columeName):
    import csv
    with open(filename, 'w') as f1:
        writer = csv.DictWriter(f1,lineterminator='\n', fieldnames=_columeName)
        writer.writeheader()
        for key, values in dictlist.items():
            #row = [key] + [value for item in values.items() for value in item]
            writer.writerow(values)


def AnalyzeLogs(f1,f2):
    if(f1!='' and f2!=''):
        dict1=exportCSVFile(f1)
        dict2=exportCSVFile(f2)
        #get add object list
        d_c=CompareDictForAdd(dict1,dict2)        
        ExportDictToCSV(f1+'_add_comp_dict.csv',d_c,_columeName=['object','d1_size','d2_size','d1_count','d2_count','size_increase','count_increase','max_size_increase','max_addressfrom_d1','max_addressfrom_d2'])
        d_c2=CompareDictForSame(dict1,dict2)
        ExportDictToCSV(f1+'_same_comp_dict.csv',d_c2,_columeName=['object','d1_size','d2_size','d1_count','d2_count','size_increase','count_increase','max_size_increase','max_addressfrom_d1','max_addressfrom_d2'])
    else:
        dict1=exportCSVFile(f1)
AnalyzeLogs('D:/WillCaseShare/problem/ambor/48.txt','D:/WillCaseShare/problem/ambor/10.txt')
#AnalyzeLogs('D:/WillCaseShare/119041526000221-OOM/log/gen2.log','')


import sys
def getParamter(para,paraname):
    para_name=para.split('=')
    if(paraname==para_name[0]):
        return para_name[1]
    else:
        return ''

def main():
    # print command line arguments
    _f1path=''
    _f2path=''
    
    for arg in sys.argv[1:]:
        para_name=arg.split('=')
        print(para_name)
        if("f1path"==para_name[0]):
            _f1path=para_name[1]
        if("f2path"==para_name[0]):
            _f2path=para_name[1]
    print(exportfilepath)
    AnalyzeLogs(_f1path,_f2path)
if __name__ == "__main__":
    main()