
import key_generation
from galois import GF
# Paste the cipher text as an array here:
ciphertext = input("Enter Cipher :")
cipher = [hex(0X00)]*16
ptr = 15
for i in range(len(ciphertext)-1, -1, -2):
    if(i==0):
        cipher[ptr] = hex(int(ciphertext, 16))
        ptr -= 1
        continue
    cipher[ptr] = hex(int(ciphertext[i-1:i+1], 16))
    ptr -= 1
keys= key_generation.ALL_KEYS



mul_matrix = [
        [0x0e, 0x0b, 0x0d, 0x09],
        [0x09, 0x0e, 0x0b, 0x0d],
        [0x0d, 0x09, 0x0e, 0x0b],
        [0x0b, 0x0d, 0x09, 0x0e],
    ]


def inverse_shiftRows(arr):
    
    for i in range(len(arr)):
        
        arr[i] =  arr[i][-i:]  +arr[i][:-i] 
    
    return arr

def inverse_sub_bytes(state):
    
    for i in range(4):
        for j in range(4):
            curr = state[i][j]
            row = key_generation.mapping[curr[-2]]
            col = key_generation.mapping[curr[-1]]
            state[i][j] = key_generation.Inverse_S_box[row][col]
        
        
    return state
   
def invertmixColumns(state):
    gf256 = GF(2**8,irreducible_poly=0x11b)
    
    result = [[0 for _ in range(4)] for _ in range(4)]
    for col in range(4):  
        for row in range(4):
            add=0
            
            for i in range(4):
                x=gf256(int(mul_matrix[row][i])) 
                y=gf256(int(state[i][col],16))
                
                
                product = int(x*y)
                add^=product
            result[row][col]=hex(add)
                      
    return result


def plainxorkey(state , key):
    len=0
    for i in range(4):
        for j in range(4):
            product = int(state[j][i],16)
            product^=int(key[len],16)
            len+=1
            state[j][i]=str(hex(product))
    return state
def make_state(arr):
    state = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(len(arr)):
        state[i%4][i//4] = str(arr[i])
    return state 
def printstate(state):
    result=[]
    for i in range(4):
        for j in range(4):
            result.append(state[j][i])
    return result  


state = make_state(cipher)

state=plainxorkey(state, keys[10])  
for round in range (1,11):
    key=keys[10-round] 
    
     
    state = inverse_shiftRows(state)
    

    state = inverse_sub_bytes(state)
    print("Output of round %d ",round)
    print(printstate(state))
    f = open("Decryption_states.txt", 'a')
    f.write('Output of round '+str(round)+": ")
    f.write(str(printstate(state)))
    f.write('\n')
    f.close()
    
    state=plainxorkey(state, key) 


    if(round!=10):
        state = invertmixColumns(state)
    
        #as no mix column for last round
    


PlainText = printstate(state)
print("Plaintext = " , end="")
for i in PlainText:
    print(i[2:],end="")