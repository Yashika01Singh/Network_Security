import hashlib
import Helper
numericMappingOfCombinations = {
    1: "AA",
    2: "AB",
    3: "AC",
    4: "BA",
    5: "BB",
    6: "BC",
    7: "CA",
    8: "CB",
    9: "CC"
}

allKeys = []

def findKeys(a, size):
 
    if size == 1:
        
        current_key = {}
        for i in range(len(a)):
            current_key[numericMappingOfCombinations[a[i]]] = numericMappingOfCombinations[i+1]
        #print(current_key)
        allKeys.append(current_key)
        return a
 
    for i in range(size):
        findKeys(a, size-1)
 
        if size % 2 == 1:
            temp = a[0]
            a[0] = a[size-1]
            a[size-1] = temp
          
        else:
            temp = a[i]
            a[i] = a[size-1]
            a[size-1] = temp
 
 
def attack(encrptedText, proposedKey):
    
    
    decryptedText = decrypt(encrptedText , proposedKey) 
    return(Helper.is_recognizable(decryptedText))
           
def decrypt(Plaintext, ReverseKey):
    Seperated = Plaintext.split(".")
    Ciphertext = Seperated[0]
    Hash = Seperated[1].split("\n")[0]
    n=len(Ciphertext)
    Decryptedtext=""
   
    
    for i in range(0,n,2):
        try:
         org=Ciphertext[i:i+2]
         Decryptedtext+=ReverseKey.get(org)
        except:
            Decryptedtext+=Ciphertext[i]
        
    Decryptedtext+="."
    for i in range (0,len(Hash),2):
        try:
            org=Hash[i:i+2]
            Decryptedtext+=ReverseKey.get(org)
        except:
            Decryptedtext+=Hash[i]
     
    return Decryptedtext
    
    

def Bruteforce():
    isFound = False
    result = None
    
    f = open("Encrypted_text","r")
    Data = f.readlines()
    f.close()
    
    
           
    i=0 
    for key in allKeys:
        i=0
        for line in Data:
            i+=1
            if attack(line, key):
                
                
                if(i==len(Data)-1):
                    result = key
                    #print(key)
                    isFound = True
                    break
            else:
                break
        if isFound:
            # the key we have is the reversed key used for decryption
            # we have to reverse it to get the original encryption key
            KEYY={}
            for j in key:
                KEYY[key[j]]=j
            print("THIS IS THE FINAL")
            print(KEYY)
            return result
    return result

# Driver code
a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
n = len(a)
findKeys(a, n)
Bruteforce()