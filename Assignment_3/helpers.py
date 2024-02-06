import gmpy2

portNumbers = {'A':9999, 'C':9998, 'B':9997}
# Helper Functions
def convertToNum(s):

    """This function helps to convert a string to a number by taking ASCII values of each character"""
    toRet = ""
    for i in range(len(s)):
        currChar = ord(s[i])
        strForm = str (currChar)
        if(len(strForm) < 3 ):
            strForm = ("0" * (3 - len(strForm))) + strForm
        toRet = toRet + strForm

    return int(toRet)

def convertToStr(n):
    """This function takes in the number that the above function generates and converts it back to a string"""
    toRet = ""
    n = str (n)
    remainder = len(n) % 3
    if(remainder != 0):
        remainder = 3 - remainder
        n = ("0"*remainder) +n
    for i in range(len(n)-3, -1, -3):
        currNum = n[i:i+3]
        currNum = int(currNum)
        currChar = chr(currNum)
        toRet = currChar + toRet

    return toRet

def getStringFormatOfKey(key):
    toRet = str(key[0])+","+str(key[1])
    return toRet

def get_e_and_z_loops(z):
    e = 2
    for i in range(2, z+1):
        if(gmpy2.gcd(i, z) == 1):
            e = i
            break
    d = gmpy2.invert(e, z)
    d = int(d)
    return [e, d]

def get_e_and_d(z):
    """This function uses the concenpt of Fermat numbers to generate
    the values of e and d for the RSA algorithm"""

    fermat1 = 3
    fermat2 = 5
    fermat3 = 17
    fermat4 = 257
    fermat5 = 65537
    e = -1
    if(z > fermat5):
        e = fermat5
        d = gmpy2.invert(e, z)
        d = int(d)        
        if(gmpy2.gcd(d, z) == 1):
            if(not (e==d)):
                return [e, d]

    if (z > fermat4):
        e = fermat4
        d = gmpy2.invert(e, z)
        d = int(d)
        if (gmpy2.gcd(d, z) == 1):
            if (not (e == d)):
                return [e, d]
    if (z > fermat3):
        e = fermat3
        d = gmpy2.invert(e, z)
        d = int(d)
        if (gmpy2.gcd(d, z) == 1):
            if (not (e == d)):
                return [e, d]

    if (z > fermat2):
        e = fermat2
        d = gmpy2.invert(e, z)
        d = int(d)
        if (gmpy2.gcd(d, z) == 1):
            if (not (e == d)):
                return [e, d]
    if (z > fermat1):
        e = fermat1
        d = gmpy2.invert(e, z)
        d = int(d)
        if (gmpy2.gcd(d, z) == 1):
            if (not (e == d)):
                return [e, d]

def generates_asymmetric_keys(p ,q):

    n = p * q
    z = (p - 1) * (q - 1)
    e_and_d = get_e_and_d(z)
    if(e_and_d == None):
        print("Could not find e and d")
        return
    e = e_and_d[0]
    d = e_and_d[1]
    if (d == -1):
        return None
    publicKey = (e, n)
    privateKey = (d, n)
    return (publicKey, privateKey)

def encrypt(m, key):
    "Takes in string m and encodes it to give integer C"
    M = m
    e = key[0]
    n = key[1]
    return pow(M, e, n)

def decrypt(c, key):
    "Takes in integer c and decodes to give integer M"
    c = int(c)
    d = key[0]
    n = key[1]
    m = pow(c, d, n)
    return m

def EncryptMessageForSending(Message, key):
    #Takes in string Message and encrypts it to give encode utf-8 string
    Message = convertToNum(Message)
    Message = encrypt(Message,key)
    Message = str(Message).encode()
    return Message

def DecryptReceivedMessage(Message , key):
    Message = int(Message.decode())
    Message = decrypt(Message,key)
    Message = convertToStr(Message)
    return Message


#Testing stuff
#

# a = "Hellodfsf,, World"
# print(convertToNum(a))
# print(convertToStr(convertToNum(a)))
# num1 = 319705304701141539155720137200974664666792526059405792539680974929469783512821793995613718943171723765238853752439032835985158829038528214925658918372196742089464683960239919950882355844766055365179937610326127675178857306260955550407044463370239890187189750909036833976197804646589380690779463976173
# num2 = 250556952327646214427246777488032351712139094643988394726193347352092526616305469220133287929222242315761834129196430398011844978805263868522770723615504744438638381670321613949280530254014602887707960375752016807510602846590492724216092721283154099469988532068424757856392563537802339735359978831013
# assymKey = generates_asymmetric_keys(num1, num2)
# e = assymKey[0][0]
# d = assymKey[1][0]
# n = assymKey[0][1]
# print("e =", e, "d = ", d, "n =", n)



# print(encrypt(132123, e, n))
# print(decrypt(encrypt("klsfjlkfldsfj",((40503837526893205364908372369806368921372659718937394143766116850023650762164883958679829714512412835497505226055510627584417962372400323481392190670918717670933976227169385232769275371164380426324061217327616460930466759235241161481300639333506263637334635396798754901811190625143049057865785739353351945649022689473122053191327036635793521217022445336222286647237438393579199536139890443566229763339792788806323145703953491920594473350931534858171719791873292949021163617498512290767047621954010711506477257121931122877153363748722095915284495781009200909409951630376733753452248348283273), 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000231000000000000023700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000054747)), (65537, 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000231000000000000023700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000054747)))


