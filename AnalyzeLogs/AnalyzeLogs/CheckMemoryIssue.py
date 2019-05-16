# step 1, check memory inforamtion 
import os
from pykd import *
from colorama import Fore, Back, Style 


import sys

#def main():
#    # print command line arguments
#    for arg in sys.argv[1:]:
#        print(arg)

#if __name__ == "__main__":
#    main()
#print(Fore.RED+"Every Gen size Ratio 100:10:1")
result=pykd.dbgCommand("!ClrPerfCounters ")

if(result):    
    for line in result.split("\n"):
        if('GEN 0 Collections' in line):
            _g0_c=line.rstrip('\n').split();
            _g0_c_itmes=_g0_c[-1].replace(',','')
            #print(line)
            print("Gen 0 Collection times {}".format(_g0_c_itmes))
        if('GEN 1 Collections' in line):
            _g1_c=line.rstrip('\n').split();
            _g1_c_itmes=_g1_c[-1].replace(',','')
            #print(line)
            print("Gen 1 Collection times {}".format(_g1_c_itmes))
        if('GEN 2 Collections' in line):
            _g2_c=line.rstrip('\n').split();
            _g2_c_itmes=_g2_c[-1].replace(',','')
            #print(line)
            print("Gen 2 Collection times {}".format(_g2_c_itmes))
        if('GEN 0 Heap Size' in line):
            _g0_h=line.rstrip('\n').split();
            _g0_h_size=_g0_h[-1].replace(',','')
            #print(line)
            print("Gen 0 Heap Size {}".format(_g0_h_size))
        if('GEN 1 Heap Size' in line):
            _g1_h=line.rstrip('\n').split();
            _g1_h_size=_g1_h[-1].replace(',','')
            #print(line)
            print("Gen 1 Heap Size {}".format(_g1_h_size))
        if('GEN 2 Heap Size' in line):
            _g2_h=line.rstrip('\n').split();
            _g2_h_size=_g2_h[-1].replace(',','')
            #print(line)
            print("Gen 2 Heap Size {}".format(_g2_h_size))
        if('LOH Size' in line):
            _LOH_h=line.rstrip('\n').split();
            _LOH_h_size=_LOH_h[-1].replace(',','')
            #print(line)
            print("LOH Heap Size {}".format(_LOH_h_size))
        if('% Time in GC' in line):
            _GC_Time=line.rstrip('\n').split();
            print(line)
            _GC_Time_value=_GC_Time[-1].replace('%','')
     # Judgement whether MemoryLeak       
    gc1_heap_ratio=int(_g1_h_size)/int(_g2_h_size)
    gc0_heap_ratio=int(_g0_h_size)/int(_g2_h_size)
    _LOH_h_size_ratio=int(_g2_h_size)/int(_LOH_h_size)
    if(float(_GC_Time_value)>50):
        print("GC take lots of time, please check LOH and Pined Object. THe Application may have memory leak issue")
    else:
        print("GC time is OK")

    if(gc1_heap_ratio<=1 and gc0_heap_ratio<10):
        print("Please focus on Gen 2 , application memory leak!")
    if(_LOH_h_size_ratio<0.2):
        print("Please focus on LOH, application memory leak!")

else:
    result2=pykd.dbgCommand("!gcheapinfo ")
    #print(result2)
    for line2 in result2.split("\n"):
        if('Total ' in line2):
            heaps=line2.rstrip('\n').replace(',','').split()
            _g0_h_size=heaps[1].replace(',','')
            _g1_h_size=heaps[2].replace(',','')
            _g2_h_size=heaps[3].replace(',','')
            _LOH_h_size=heaps[-1].replace(',','')
            #print(line2)
            print("Gen 0 Heap Size {}".format(_g0_h_size))
            print("Gen 1 Heap Size {}".format(_g1_h_size))
            print("Gen 2 Heap Size {}".format(_g2_h_size))
            print("LOH Heap Size {}".format())
            gc1_heap_ratio=int(_g1_h_size)/int(_g2_h_size)
            gc0_heap_ratio=int(_g0_h_size)/int(_g2_h_size)
            _LOH_h_size_ratio=int(_g2_h_size)/int(_LOH_h_size)
            if(gc1_heap_ratio<=1 and gc0_heap_ratio<10):
                print("Please focus on Gen 2, application memory leak!")
            if(_LOH_h_size_ratio<0.2):
                print("Please focus on LOH, application memory leak!")
