
def correspondance(a, b):
    ret=0
    for i,j in enumerate(a):
        k=b[i]
        if i!=0:
            if j[0]==k[0]:
                if j[0]=='h':
                    for m in range(1,5):
                        if j[m]==k[m]:
                            ret+=0.25
                        elif m>0:
                            if j[m-1]==k[m]:
                                ret+=0.2
                            elif j[m]==k[m-1]:
                                ret+=0.2
                if j[0]=='n':
                    c=un_base_4(j)
                    d=un_base_4(k)
                    moy =(c+d)/2
                    equart = abs(moy-d)
                    if equart==0:
                        ret+=1
                    else:
                        equart= equart/moy
                        ret += 1-equart
    ret=ret/(len(a)-1)
    return ret

def base_4(x):
    x=int(x)
    if x>=255:
        return('3333')
    else:
        ret =''
        for i in range(4):
            ret+=str(x%4)
            x=x//4
        return(ret)

def un_base_4(x):
    ret = 0
    for i in [3,2,1,0]:
        ret+=int(x[i+1])*4**i
    return ret
