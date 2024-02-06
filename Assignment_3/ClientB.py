import socket
import helpers
import CA
import time
import hashlib
import random
public_key_of_PKDA = CA.publicKeyOfPKDA
num1 = 4777754353108489574150042968405660074481084482072805204134232904882626149351589214018410633533906617419921858928628792494854702834749389490806013915521190829908664073159925934660210713476647777666769098356046678509217307191590088308393608039009318646948205632068043129193257862673
num2 = 2472773490088428133980402514441160210616362471988372788573252776560313375548879579643617872035716953544469744723310736110488902356856738414994328039965984433249491556806522755609731304100884485833876145266471071156842673554540732151138408860390316340855518308224087245071159274479
keyWithMe = {}
mypublicKey, myprivateKey = helpers.generates_asymmetric_keys(num1, num2)
f = open("ClientB.txt", "w")
f.write(str(mypublicKey)+"\n"+str(myprivateKey))
f.close()
myName = "B"

def sendMessageToClient(client):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()

    port = helpers.portNumbers[client]
    clientsocket.connect((host, port))
    #step 1 Send ID and N1 to client
    N1 = random.randint(3,100)
    Message = myName+";"+str(N1)
    Message = helpers.EncryptMessageForSending(Message,keyWithMe[client])
    clientsocket.send(Message)
    Message = clientsocket.recv(1024)
    Message = helpers.DecryptReceivedMessage(Message,myprivateKey)
    recN1, N2 = Message.split(";")
    recN1=int(recN1)
    N2 = int(N2)
    if(N1!=recN1 or N2!=N1+1):
        print("Error while establishing connection")
        clientsocket.close()
        return
    Message = str(N2)
    Message = helpers.EncryptMessageForSending(Message,keyWithMe[client])
    clientsocket.send(Message)
    while True:
        print("Enter Message to send")
        Message = input()
        Message = helpers.EncryptMessageForSending(Message,keyWithMe[client])
        clientsocket.send(Message)
        response = clientsocket.recv(1024)
        response = helpers.DecryptReceivedMessage(response,myprivateKey)
        print("Received response from server:", response)

def verify(hashed, original):
    print("Original is", original)
    print("Hashed is", hashed)
    newHash = str(hashlib.sha1(original.encode('utf-8')).hexdigest())
    print("New",newHash)
    if hashed == newHash:
        return True
    else:
        return False
    
def turnRecieverOn():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9997
    serversocket.bind((host, port))
    serversocket.listen(1)
    print("Server is listening on port", port)
    while True:
        clientsocket, address = serversocket.accept()
        message = clientsocket.recv(2048)
        message = helpers.DecryptReceivedMessage(message,myprivateKey)
        ID, N1 = message.split(";")
        
        #Step 1 See if we have the public key, otherwise request it
        try:
            public_key_of_request = keyWithMe[ID]
        except:
            print("You don't have the public key of this client, asking the PKDA for it first")
            getKeyfromPKDA(ID)  
        
           
        #step 2 Send N1,N2 encrypted with ID public key
        N2=str(int(N1)+1)
        Message = str(N1)+";"+N2
        Message = helpers.EncryptMessageForSending(Message,keyWithMe[ID])
        clientsocket.send(Message)
        
        #step 3 Recieve N2 encrypted with Private key of request
        message = clientsocket.recv(2048)
        message = helpers.DecryptReceivedMessage(message,myprivateKey)
        recieved_N2 = message
        if(N2 ==recieved_N2):
            print(N2,recieved_N2)
            print("Connection succcess")
        else:
            print("COnnection could not be established")
            continue
        
        
        while True: 
            
            message = clientsocket.recv(3000)
            if(message==''):
                break
            message = helpers.DecryptReceivedMessage(message,myprivateKey)
            print("Message Received : ",message)
            
            message = "Got it"+message[-1]
            print(message)
            message = helpers.EncryptMessageForSending(message,keyWithMe[ID])
            clientsocket.send(message)



def send_key_to_PKDA():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost',1024)
    sock.connect(server_address)
    KeyOwner = "B"
    KeyOwner = helpers.convertToNum(KeyOwner)
    KeyOwner = helpers.encrypt(KeyOwner,public_key_of_PKDA)
    mypublicKey_e = helpers.encrypt(mypublicKey[0],public_key_of_PKDA)
    mypublicKey_n = helpers.encrypt(mypublicKey[1],public_key_of_PKDA)
    Message = str(KeyOwner)+";"+str(mypublicKey_e)+";"+str(mypublicKey_n)
    Message = Message.encode('utf-8')
    sock.sendall(Message)
    
def getKeyfromPKDA(Request):
    
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost',1034)
    sock.connect(server_address)
    #Step1 Send Request and T1
    T1= int(time.time() * 1000)
    Enc_T1 = helpers.encrypt(T1,public_key_of_PKDA)
    Enc_Requester = helpers.encrypt(helpers.convertToNum("B"),public_key_of_PKDA)
    Enc_Request = helpers.encrypt(helpers.convertToNum(Request),public_key_of_PKDA)
    Message = str(Enc_Requester)+";"+str(Enc_Request)+";"+str(Enc_T1)
    
    Message=(Message).encode('utf-8')
    sock.sendall(Message)
    
    #Step2 Receiving Public key of Request , Request and T1 back
    print("Sending ")
    data = sock.recv(4000)
    data=data.decode('utf-8')


    Enc_requested_e,Enc_requested_n,Enc_T1, Enc_hash= data.split(";")  
    Enc_requested_e = int(Enc_requested_e)
    Enc_requested_n = int(Enc_requested_n)
    Enc_T1 = int(Enc_T1)
    Enc_Hash = int(Enc_hash)
  
    requested_e = helpers.decrypt(Enc_requested_e,public_key_of_PKDA)
    requested_n = helpers.decrypt(Enc_requested_n,public_key_of_PKDA)
    Recd_T1 = helpers.decrypt(Enc_T1,public_key_of_PKDA)
    hashed = helpers.decrypt(Enc_Hash,public_key_of_PKDA )
    Message = str(requested_e+requested_n+Recd_T1)
    HashedMessage = helpers.convertToNum(hashlib.sha1(Message.encode('utf-8')).hexdigest())
    
    
    if (hashed!=HashedMessage or Recd_T1 != T1):
        
        print("This response may not be for this request.")
      
        
    else:

        print("I recieved ", requested_e, requested_n, 'for', Request)
        keyWithMe[Request] = (requested_e,requested_n)

    sock.close()



sent = False




while(True):
    print("1. Send your public key to PKDA")
    print("2. Obtain public key of another client from PKDA")
    print("3. Send message to a client")
    print("4. Turn reciever on")

    choice = int(input("Enter a choice: "))
    if(choice == 1):
        send_key_to_PKDA()
        sent = True
    elif(choice == 2):
        if(not sent):
            print("Please send your public key to PKDA first")
            continue
        Request = input("Enter the name of the client whose public key you want to obtain: ")
        getKeyfromPKDA(Request)

    elif(choice == 3):
        Request = input("Enter the name of the client you want to send message to: ")
        try:
            public_key_of_request = keyWithMe[Request]
        except:
            print("You don't have the public key of this client, ask the PKDA for it first")
            continue
        
        sendMessageToClient(Request)

    elif(choice == 4):

        turnRecieverOn()
