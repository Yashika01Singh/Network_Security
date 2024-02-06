from Helper import *
Key = {
    "AA":"CC",
    "AB":"BA",
    "AC":"BB",
    "BA":"AA",
    "BB":"AB",
    "BC":"AC",
    "CA":"CB",
    "CB":"CA",
    "CC":"BC"
}

def encrypt(Plaintext,key):
   
    Seperated = Plaintext.split(".")
    originalText = Seperated[0]
    hashedText = Seperated[1].split("\n")[0]
    Encrypedtext=""
    

    for i in range(0, len(originalText), 2):
        try:
            toFind = originalText[i:i+2]
            Encrypedtext+= key[toFind]
        except:
            Encrypedtext+=originalText[i]+"_"
            
    Encrypedtext+="."
    
    for i in range(0, len(hashedText), 2):
        try:
            toFind = hashedText[i:i+2]
            Encrypedtext+=key[toFind]
        except:
            Encrypedtext+=hashedText[i]+"_"
      
    return Encrypedtext

def main():
    
    f = open("Plaintext.txt","r")
    Data = f.readlines()
    f.close()
    
    fd = open("Encrypted_text","w")
    for line in Data:   
         
        Encryption=encrypt(line, Key) 

        fd.write(Encryption)
        fd.write("\n")
    fd.close()
    

if __name__=="__main__":
    main()

