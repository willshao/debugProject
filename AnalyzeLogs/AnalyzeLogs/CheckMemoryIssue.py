# step 1, check memory inforamtion 
import os
import sys
from pykd import *
from colorama import Fore, Back, Style 
def GetPerformanceCounter():
    result=pykd.dbgCommand("!ClrPerfCounters ")

    if(result):    
        for line in result.split("\n"):
            if('GEN 0 Collections' in line):
                _g0_c=line.rstrip('\n').split();
                _g0_c_itmes=_g0_c[-1].replace(',','')
                print("Gen 0 Collection times: {}".format(_g0_c_itmes))
            if('GEN 1 Collections' in line):
                _g1_c=line.rstrip('\n').split();
                _g1_c_itmes=_g1_c[-1].replace(',','')
                print("Gen 1 Collection times: {}".format(_g1_c_itmes))
            if('GEN 2 Collections' in line):
                _g2_c=line.rstrip('\n').split();
                _g2_c_itmes=_g2_c[-1].replace(',','')
                print("Gen 2 Collection times: {}".format(_g2_c_itmes))
            if('GEN 0 Heap Size' in line):
                _g0_h=line.rstrip('\n').split();
                _g0_h_size=_g0_h[-1].replace(',','')
                print("Gen 0 Heap Size: {}".format(_g0_h_size))
            if('GEN 1 Heap Size' in line):
                _g1_h=line.rstrip('\n').split();
                _g1_h_size=_g1_h[-1].replace(',','')
                print("Gen 1 Heap Size: {}".format(_g1_h_size))
            if('GEN 2 Heap Size' in line):
                _g2_h=line.rstrip('\n').split();
                _g2_h_size=_g2_h[-1].replace(',','')
                print("Gen 2 Heap Size: {}".format(_g2_h_size))
            if('LOH Size' in line):
                _LOH_h=line.rstrip('\n').split();
                _LOH_h_size=_LOH_h[-1].replace(',','')
                print("LOH Heap Size: {}".format(_LOH_h_size))
            if('% Time in GC' in line):
                _GC_Time=line.rstrip('\n').split();
                #print("Time in GC: {}".format(_GC_Time))
                _GC_Time_value=_GC_Time[-1].replace('%','')
                print("Time in GC: {}%".format(_GC_Time_value))
        gc1_heap_ratio=int(_g1_h_size)/int(_g2_h_size)
        gc0_heap_ratio=int(_g0_h_size)/int(_g2_h_size)
        _LOH_h_size_ratio=int(_g2_h_size)/int(_LOH_h_size)
        _GC_Time_Ratio0=int(_g0_c_itmes)/int(_g2_c_itmes)
        _GC_Time_Ratio1=int(_g1_c_itmes)/int(_g2_c_itmes)
        print("==============Debuging Suggestion================")
        if(float(_GC_Time_value)>50 ):
            print("GC take lots of time, please check LOH ,Pined Object and call stack. THe Application may have memory leak issue")
        if(_GC_Time_Ratio1<2):
            print("Gen2 GC ratio high, please check LOH and Pined Object. THe Application may have memory leak issue")
        if(gc1_heap_ratio<=1 and gc0_heap_ratio<10):
            print("Please focus on Gen 2 , application memory leak!")
        if(_LOH_h_size_ratio>0.7):
            print("Please focus on LOH, application memory leak!")
    else:
        result2=pykd.dbgCommand("!mex.gcheapinfo ")
        for line2 in result2.split("\n"):
            if('Total ' in line2):
                heaps=line2.rstrip('\n').replace(',','').split()
                _g0_h_size=heaps[1].replace(',','')
                _g1_h_size=heaps[2].replace(',','')
                _g2_h_size=heaps[3].replace(',','')
                _LOH_h_size=heaps[-1].replace(',','')
                print("Gen 0 Heap Size: {}".format(_g0_h_size))
                print("Gen 1 Heap Size: {}".format(_g1_h_size))
                print("Gen 2 Heap Size: {}".format(_g2_h_size))
                print("LOH Heap Size: {}".format(_LOH_h_size))
                gc1_heap_ratio=int(_g1_h_size)/int(_g2_h_size)
                gc0_heap_ratio=int(_g0_h_size)/int(_g2_h_size)
                _LOH_h_size_ratio=int(_g2_h_size)/int(_LOH_h_size)
                #_GC_Time_Ratio0=int(_g0_c_itmes)/int(_g2_c_itmes)
                #_GC_Time_Ratio1=int(_g1_c_itmes)/int(_g2_c_itmes)
                print("==============Debuging Suggestion================")
                if(gc1_heap_ratio<=1 and gc0_heap_ratio<10):
                    print("Please focus on Gen 2, application memory leak!")
                if(_LOH_h_size_ratio>0.7):
                    print("Please focus on LOH, application memory leak!")
                #if(_GC_Time_Ratio1<2):
                 #   print("Gen2 GC ratio high, please check LOH and Pined Object. THe Application may have memory leak issue")
def main():
    # print command line arguments
    #for arg in sys.argv[1:]:
    #    print(arg)
    GetPerformanceCounter()

if __name__ == "__main__":
    main()