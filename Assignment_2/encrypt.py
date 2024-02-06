
import key_generation
from galois import GF


str_plainText = input("Enter plaintext in hexadecimal: ")
keys= key_generation.ALL_KEYS
plainTextArr = [hex(0X00)]*16


mul_matrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02],
    ]

ptr = 15
for i in range(len(str_plainText)-1, -1, -2):
    if(i==0):
        plainTextArr[ptr] = hex(int(str_plainText[i], 16))
        ptr -= 1
        continue
    plainTextArr[ptr] = hex(int(str_plainText[i-1:i+1], 16))
    ptr -= 1





def shiftRows(arr):
    
    for i in range(len(arr)):
        arr[i] = arr[i][i:] + arr[i][:i]
    
    return arr

def subBytes(state):
    
    for i in range(4):
        for j in range(4):
            curr = state[i][j]
            row = key_generation.mapping[curr[-2]]
            col = key_generation.mapping[curr[-1]]
            state[i][j] = key_generation.S_Box[row][col]
        
        
    return state
   
def mixColumns(state):
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

state = make_state(plainTextArr)
state=plainxorkey(state, keys[0])
for round in range (1,11):
    key=keys[round]   
    
    
    state = subBytes(state)
    state = shiftRows(state)
    if(round!=10):
        state = mixColumns(state)
        #as no mix column for last round
    state=plainxorkey(state, key)
    print("Output of round",round)
    print(printstate(state))
    f = open("Encryption_states.txt", 'a')
    f.write('Output of round '+str(round)+": ")
    f.write(str(printstate(state)))
    f.write('\n')
    f.close()

print("cipher = ",end=" ")
for i in printstate(state):
    print(i[2:],end="")