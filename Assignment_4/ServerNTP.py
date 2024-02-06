import socket
import helpers
import  CA
import time
import hashlib
import ntplib
from datetime import datetime 
import pytz
import ssl
public_key_of_PKDA = CA.publicKeyOfPKDA
num1 = 4777754353108489574150042968405660074481084482072805204134232904882626149351589214018410633533906617419921858928628792494854702834749389490806013915521190829908664073159925934660210713476647777666769098356046678509217307191590088308393608039009318646948205632068043129193257862673
num2 = 2472773490088428133980402514441160210616362471988372788573252776560313375548879579643617872035716953544469744723310736110488902356856738414994328039965984433249491556806522755609731304100884485833876145266471071156842673554540732151138408860390316340855518308224087245071159274479
keyWithMe = {}
mypublicKey, myprivateKey = helpers.generates_asymmetric_keys(num1, num2)
f = open("ClientB.txt", "w")
f.write(str(mypublicKey)+"\n"+str(myprivateKey))
f.close()
myName = "TSA"
#Choosing NTP server from the NTP pool project 
ntp_server = 'pool.ntp.org'


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
        message = message.decode()
       
            
        
        print("Hash Received : ",message)
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request(ntp_server)
        ntp_time = datetime.utcfromtimestamp(response.tx_time)
        gmt = pytz.timezone('GMT')
        gmt_now = gmt.localize(ntp_time)
        uploadedTime = f"The upload time is: {gmt_now.strftime('%Y-%m-%d %H:%M:%S')}"
        message+=" TIME: " + gmt_now.strftime('%Y-%m-%d %H:%M:%S')
        data = helpers.EncryptMessageForSending(message,myprivateKey)
        clientsocket.sendall(data)
        



def send_key_to_PKDA():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost',1024)
    sock.connect(server_address)
    KeyOwner = myName
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






send_key_to_PKDA()

turnRecieverOn()
