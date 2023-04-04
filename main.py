import Main.inverse as inverse
import  rand as rand
import polArithmetic as polArithmetic

def key_gen(df,dg,deg,q,p):
    f = rand.randpol(df, df - 1, deg + 1)
    # print("f is:",f)
    g = rand.randpol(dg, dg, deg + 1)
    # print("g is:",g)
    N = len(f)
    D = [0]*(N+1)
    D[0] = -1
    D[N] = 1
    [gcd_f,s_f,t_f] = inverse.extEuclidPoly(f,D)
    finvp = inverse.modPoly(s_f,p)
    # print("finvp is:",finvp)
    finvq = inverse.modPoly(s_f,q)
    # print("finvq is:",finvq)
    while finvp is None or finvq is None:
        f = rand.randpol(df, df - 1, deg + 1)
        [gcd_f,s_f,t_f] = inverse.extEuclidPoly(f,D)
        finvp = inverse.modPoly(s_f,p)
        finvq = inverse.modPoly(s_f,q)
    for i in range(len(g)):
        g[i] = g[i]*p
    h = polArithmetic.star_multiply(g,finvq,q)
    pk = [f,finvp]
    return h,pk

# h is the public key
# m - message
def encrypt(h,dr,msg,q,deg):
    r = rand.randpol(dr, dr, deg + 1)
    temp = polArithmetic.star_multiply(h,r,q)
    [msg,temp] = inverse.resize(msg,temp)
    e = polArithmetic.polAdd(msg,temp,q)
    return e

def decrypt(pk, e, p,q):
    a = polArithmetic.star_multiply(e,pk[0],q)
    r = q/2
    for i in range(len(a)):
        if a[i] < -1*r:
            a[i] = a[i] + q
        elif a[i] > r:
            a[i] = a[i] - q
    for i in range(len(a)):
        a[i] = a[i]%p
    c = polArithmetic.star_multiply(a,pk[1],p)
    return c

N = int(input("Enter N:"))
p = int(input("Enter p:"))
q = int(input("Enter q:"))
dr = int(input("Enter dr:"))
df = int(input("Enter df:"))
dg = int(input("Enter dg:"))
# N = 17,dg = 5,df = 5,q = 6,p = 3,dr = 6 for testing

[pub,priv] = key_gen(df,dg,N - 1,q,p)
n = int(input("Enter the length of message:"))
msg = []
for i in range(n):
    msg.append(int(input()))
blocks = []
ciphertext = []
if(len(msg)<N):
    inverse.resize(msg,pub)
    blocks.append(msg)
else:
    for i in range(0,len(msg),N):
        if(i+N <= len(msg)):
            blocks.append(msg[i:i+N])
    if(len(msg) % N):
        inverse.resize(msg[i:len(msg)],pub)
        blocks.append(msg[i:i+N])


for i in range (0,len(blocks)):
    ciphertext.append(encrypt(pub,dr,blocks[i],q,N - 1))
    print("Original message: ",blocks[i])
    print("ciphertext[" ,i,"] : ",ciphertext[i])
    if(len(blocks[i]) < len(ciphertext[i])):
        print("Decrypted message: ",decrypt(priv,ciphertext[i],p,q)[0:len(blocks[i])])
    else:
        print("Decrypted message: ",decrypt(priv,ciphertext[i],p,q))

