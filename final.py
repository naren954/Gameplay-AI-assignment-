import time
import sys
import signal
def splaadd(ap):
    global availS
    date=ap[13:20]
    for j in range(7):
            if date[j]=='1':
                availS[j]=availS[j]+1;
                
def lahsaadd(ap):
    global availL
    date=ap[13:20]
    for j in range(7):
            if date[j]=='1':
                availL[j]=availL[j]+1;
                
def splacheck(ap):
    global availS,sdays
    if ap[10:13]=="NYY":
        temp1=availS[:]
        temp2=sdays[:]
        date=ap[13:20]
        for j in range(7):
            if date[j]=='1':
                if availS[j]==0:
                    sdays=temp2[:]
                    availS=temp1[:]
                    return 0
                sdays[j]=sdays[j]+1
                availS[j]=availS[j]-1;
    else:
        return 0
    return 1

def lahsacheck(ap):
    global availL,ldays
    if int(ap[6:9])>17 and ap[5]=="F" and ap[9]=="N":
        temp1=availL[:]
        temp2=ldays[:]
        date=ap[13:20]
        for j in range(7):
            if date[j]=='1':
                if availL[j]==0:
                    ldays=temp2[:]
                    availL=temp1[:]
                    return 0
                ldays[j]=ldays[j]+1
                availL[j]=availL[j]-1
    else:
        return 0
    return 1

def evaluate(spicked,lpicked):
    s=0
    l=0
    for i in spicked:
        s=s+int(i[20])
    for i in lpicked:
        l=l+int(i[20])
    return s,l
    
def splapick(splalist,lahsalist,avails,availl,first):
    global BEST,spicked,lpicked,neededs,potans,start
    if len(splalist)==0 and len(lahsalist)==0:
        return evaluate(spicked,lpicked)
    maxs=0
    bestfirst=''
    L=0
    for i in splalist:
        temp1=splalist[:]
        temp1.remove(i)
        tempr=temp1[:]
        temp2=lahsalist[:]
        spicked.append(i)
        temp5=avails[:]
        temp6=availl[:]
        date=i[13:20]
        if neededs==1:
            for j in range(7):
                if date[j]=='1':
                    temp5[j]=temp5[j]-1
        if neededs==1:
            for j in tempr:
                date=j[13:20]
                for k in range(7):
                    if temp5[k]==0 and date[k]=='1':
                        temp1.remove(j)
                        break
        if i in lahsalist:
            temp2.remove(i)
        if len(temp2)!=0:
            [s,l]=lahsapick(temp1,temp2,temp5,temp6)
        else:
            [s,l]=splapick(temp1,temp2,temp5,temp6,0)
        spicked.remove(i)
        if s>maxs:
            bestfirst=i[:5]
            maxs=s
            L=l
        elif s==maxs:
            if int(bestfirst)>int(i[:5]):
                bestfirst=i[:5]
                L=l
    if first==1:
        BEST=bestfirst
    return maxs,L

def lahsapick(splalist,lahsalist,avails,availl):
    global spicked,lpicked,neededl,potans,start
    if len(splalist)==0 and len(lahsalist)==0:
        return evaluate(spicked,lpicked)
    maxl=0
    S=0
    for i in lahsalist:
        temp1=splalist[:]
        temp2=lahsalist[:]
        temp2.remove(i)
        tempr=temp2[:]
        lpicked.append(i)
        temp5=avails[:]
        temp6=availl[:]
        date=i[13:20]
        if neededl==1:
            for j in range(7):
                if date[j]=='1':
                    temp6[j]=temp6[j]-1
        if neededl==1:
            for j in tempr:
                date=j[13:20]
                for k in range(7):
                    if temp6[k]==0 and date[k]=='1':
                        temp2.remove(j)
                        break
        if i in splalist:
            temp1.remove(i)
        if len(temp1)!=0:
            [s,l]=splapick(temp1,temp2,temp5,temp6,0)
        else:
            [s,l]=lahsapick(temp1,temp2,temp5,temp6)
        lpicked.remove(i)
        if l>maxl:
            bestfirst=i[:5]
            maxl=l
            S=s
        elif l==maxl:
            if int(bestfirst)>int(i[:5]):
                bestfirst=i[:5]
                S=s
    return S,maxl

def timeout(a,b):
    global potans
    print time.time()-start
    print(potans)
    o.write(potans)
    sys.exit()
def endprog(a,b):
    pass

start=time.time()
signal.signal(signal.SIGALRM,timeout)
signal.alarm(175)
f=open("input.txt")
o=open('output.txt','w')
b=int(f.readline())
p=int(f.readline())
availL=[b,b,b,b,b,b,b]
availS=[p,p,p,p,p,p,p]
L=int(f.readline())
lahsa=[]
spla=[]
splalist=[]
lahsalist=[]
applicants=[]
potans=''
maxn=0
maxsp=0
odd=0
neededs=0
neededl=0
sdays=[0,0,0,0,0,0,0]
ldays=[0,0,0,0,0,0,0]
comeff=[0,0,0,0,0,0,0]
potans1=''
comcheck=0
for i in range(L):
    lahsa.append(f.readline().rstrip())
S=int(f.readline())
for i in range(S):
    spla.append(f.readline().rstrip())
A=int(f.readline())
for i in range(A):
    ap=f.readline().rstrip()
    id=ap[0:5]
    dates=ap[13:20]
    if id in lahsa:
        for j in range(7):
            if dates[j]=='1':
                availL[j]=availL[j]-1;
    elif id in spla:
        for j in range(7):
            if dates[j]=='1':
                availS[j]=availS[j]-1;
    else:
        applicants.append(ap)
        
for ap in applicants:
    check1=0
    check2=0
    dates=ap[13:20]
    numdays=dates.count('1')
    ap=ap+str(numdays)
    if(splacheck(ap)==1):
        check1=1
        splalist.append(ap)
        splaadd(ap)
        if numdays>maxsp:
            maxsp=numdays
            potans1=ap[:5]
        elif numdays==maxn:
            if int(potans1)>int(ap[:5]):
               potans1=ap[:5]
    if(lahsacheck(ap)==1):
        check2=1
        lahsalist.append(ap)
        lahsaadd(ap)
    if check1 and check2==1:
        odd=not odd
        comeff[numdays-1]+=1
        if numdays>maxn:
            maxn=numdays
            potans=ap[:5]
        elif numdays==maxn:
            if int(potans)>int(ap[:5]):
               potans=ap[:5]
               
if sum([int(i<=j) for i,j in zip(sdays,availS)])!=7:
    neededs=1
if sum([int(i<=j) for i,j in zip(ldays,availL)])!=7:
    neededl=1
for i in comeff:
    if i%2!=0:
        comcheck=1
spicked=[]
lpicked=[]
BEST=''
bestfirst=""
first=""
maxins=0
S=0
L=0
if comcheck==0:
    potans=potans1
    if neededs==0:
        ap=applicants[0]
[smax,lmax]=splapick(splalist,lahsalist,availS,availL,1)
end=time.time()
print BEST
print [smax,lmax]
o.write(BEST)
print(end-start)
signal.signal(signal.SIGALRM,endprog)
signal.alarm(0)