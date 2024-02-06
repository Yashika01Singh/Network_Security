

import Helper

ReverseKey = {
    "AA":"BA",
    "AB":"BB",
    "AC":"BC",
    "BA":"AB",
    "BB":"AC",
    "BC":"CC",
    "CA":"CB",
    "CB":"CA",
    "CC":"AA"
}

def decrypt(Plaintext):
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
    
    
def main():
    
    f = open("Encrypted_text","r")
    Data = f.readlines()
    f.close()
    
    fd = open("AfterDecryption.txt","w")
    for line in Data:   
           
        Decryp=decrypt(line)
        Decryp=Decryp.split("\n")[0]
        
        if(Helper.is_recognizable(Decryp)!=True):
            fd.write("Decryption Failed ABORT")
            return
             
        fd.write(Decryp)
        fd.write("\n")
    fd.write("\n\nALL TEXT SUCCESSFULLY DECIPHERED")
    fd.close()
    

if __name__=="__main__":
    main()
