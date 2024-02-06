import os
import hashlib

numericMappingOfCombinations = {
    '0': "A",
    '1': "AA",
    '2': "AB",
    '3': "AC",
    '4': "BA",
    '5': "BB",
    '6': "BC",
    '7': "CA",
    '8': "CB",
    '9': "CC"
}
def generate_plaintext(Original_text):
    hashedText = hashlib.sha256(Original_text.encode())
    plainText = Original_text+"."+hashedText.hexdigest()
    print(plainText)

def hashText(original):
    numeric_mappings = {'A':'00', 'B':'01', 'C':'10'}

def generate_plaintext(Original_text):

    hashedText = hash(Original_text)
    #print(hashedText.hexdigest())
    plainText = Original_text+"."+hashedText
    return(plainText)


def is_recognizable(Plaintext):
    proposedOriginalText = Plaintext.split(".")[0]
    proposedHashedText = Plaintext.split(".")[1]
    hashedText = hash(proposedOriginalText)
    if hashedText == proposedHashedText:
        return True
    else:
        return False









def hash(originalText):
    num_A = 0 
    num_B = 0
    num_C = 0
    value = 0
    for char in originalText:
        value = value * 3
        if char == 'A':
            value += 0
            num_A += 1
        elif char == 'B':
            value += 1
            num_B += 1
        elif char == 'C':
            value += 2
            num_C += 1
    value = str(value % 256)
    value += str(num_A)
    value += str(num_B)
    value += str(num_C)
    finalAns = ""
    for i in value:
        finalAns += numericMappingOfCombinations[i]
        
    return finalAns



def main():
    f= open("Plaintext.txt","w")
    data= ["AABBCCABABBABCCACB" , "ABBCBCAACBBACBACBA","AABCBCBABCACBACBABCA","AABCBCBCBABACABCABCA","BBACBACABCBACCBACAAB"]
    for line in data:
    
       plaintext=generate_plaintext(line)
       f.write(plaintext)
       f.write("\n")
    f.close()
   
if __name__=="__main__":
    main()
