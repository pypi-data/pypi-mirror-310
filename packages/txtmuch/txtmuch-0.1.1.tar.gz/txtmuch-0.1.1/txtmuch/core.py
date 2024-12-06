#txtmuch 

def much(txt):
    #字串長度
    return len(txt)

def cut(txt):
    #分割成幾個
    k=txt.split()
    return len(k)
    
def onlytxt(txt):
    #純計算單詞
    k = len(re.findall(r'\w+', txt))
    return k

def big(txt):
    #全部轉換為大寫
    return str.upper(txt)

def headbig(txt):
    #字首大寫
    return str.capitalize(txt)

def bigsmall(txt):
    #大小寫對調
    return str.swapcase(txt)
