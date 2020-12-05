# Storing text data in a list variable
# import necessary module
# Created by FFE
import numpy as np
import re
#______________________________________________________________________________
# import .txt file
filename="amprion_bw4_wvrstat_unpluggedom_psi.lst"
mylines = []
with open(filename, "r") as myfile:
        for myline in myfile:
            mylines.append(myline)
#______________________________________________________________________________
# finding the right section in the listing file
num_lines = sum(1 for line in open(filename))
INDEX=np.arange((num_lines), dtype='i')
key = ("                                       FINAL PILE HEAD FORCES (KN   AND KN-M    ) FOR LOAD CASE")
key2 = ("                                                    STRUCTURAL COORDINATES\n")
for i in range(0,num_lines):
    if key == mylines[i][:95] and key2 == mylines[i+4]: 
        INDEX[i] =i
    else:
        INDEX[i] =0
NUMBER = np.count_nonzero(INDEX)
INDEXlist=INDEX.nonzero()
#______________________________________________________________________________
ALL_LOADCASE=[]
FX =[];FY =[];FZ =[];MX =[];MY =[];MZ =[];FR =[];MR =[]
MAX = []
#
for i in range (0,len(INDEXlist[0])):
        a=INDEXlist[0][i]
        ALL_LOADCASE.append(mylines[a][-5:-1])
# Loop for 16 Piles
for b in range (0,16):
# Loop for 171 Load Combinations
    for i in range (0,len(INDEXlist[0])):
        a=INDEXlist[0][i]
        ASU=re.split(' +',mylines[a+9+b])
        FX.append(float(ASU[3]))
        FY.append(float(ASU[4])) 
        FZ.append(float(ASU[5])) 
        MX.append(float(ASU[6])) 
        MY.append(float(ASU[7])) 
        MZ.append(float(ASU[8])) 
        # Max Horizontal Force and Moment
        FR.append((float(ASU[3])**2+float(ASU[4])**2)**0.5)
        MR.append((float(ASU[6])**2+float(ASU[7])**2)**0.5)
        #   
    MAX.append(round(int(max(FZ))))
    MAX.append(round(int(min(FZ))))
    MAX.append(round(int(max(FR))))
    MAX.append(round(int(max(MR))))
    #    
    indexMaxFZ = FZ.index(max(FZ))
    indexMinFZ = FZ.index(min(FZ))
    indexMaxFR = FR.index(max(FR))
    indexMaxMR = MR.index(max(MR))
    #
    MAX.append(ALL_LOADCASE[indexMaxFZ])    
    MAX.append(ALL_LOADCASE[indexMinFZ])
    MAX.append(ALL_LOADCASE[indexMaxFR])    
    MAX.append(ALL_LOADCASE[indexMaxMR])
    #
    FX =[];FY =[];FZ =[];MX =[];MY =[];MZ =[];FR =[];MR =[]
#______________________________________________________________________________
# Storing The Maximum FR, MR, LoadCase for Max FR and Load Case for Max MR
MAXFZ=[]
LC_MAXFZ=[]
MINFZ=[]
LC_MINFZ=[]
MAXFR=[]
LC_MAXFR=[]
MAXMR=[]
LC_MAXMR=[]
x=0
while x<len(MAX):
    MAXFZ.append(MAX[x])
    x=x+1
    MINFZ.append(MAX[x])
    x=x+1
    MAXFR.append(MAX[x])
    x=x+1
    MAXMR.append(MAX[x])
    x=x+1
    LC_MAXFZ.append(MAX[x])
    x=x+1
    LC_MINFZ.append(MAX[x])
    x=x+1
    LC_MAXFR.append(MAX[x])
    x=x+1
    LC_MAXMR.append(MAX[x])
    x=x+1