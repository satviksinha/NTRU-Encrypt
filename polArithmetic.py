import inverse as inverse

def polAdd(pol1,pol2,mod):
    [pol1,pol2] = inverse.resize(pol1,pol2)
    answer = []
    i = 0
    while(i < len(pol1)):
        answer.append((pol1[i] + pol2[i])% mod)
        i = i + 1
    
    return answer

def polSub(pol1,pol2,mod):
    [pol1,pol2] = inverse.resize(pol1,pol2)
    answer = []
    i = 0
    while(i < len(pol1)):
        answer.append((pol1[i] - pol2[i])% mod)
        i = i + 1
    
    return answer

def star_multiply(p1, p2, q):
    """Multiply two polynomials in Z_q[X]/(X**n - 1)"""
    [p1,p2] = inverse.resize(p1,p2)
    out = [0] * len(p1)
    for k in range(len(p1)):
        for i in range(len(p1)):
            if k >= i:
                out[k] += p1[i] * p2[k - i]
            else:
                out[k] += p1[i] * p2[len(p1) + k - i]
    return [x % q for x in out]