import helpers
import hashlib
import socket
import time
import threading
HOST = "127.0.0.1"#localhost
PORT = 1024 #custom port
num1 = 319705304701141539155720137200974664666792526059405792539680974929469783512821793995613718943171723765238853752439032835985158829038528214925658918372196742089464683960239919950882355844766055365179937610326127675178857306260955550407044463370239890187189750909036833976197804646589380690779463976173
num2 = 250556952327646214427246777488032351712139094643988394726193347352092526616305469220133287929222242315761834129196430398011844978805263868522770723615504744438638381670321613949280530254014602887707960375752016807510602846590492724216092721283154099469988532068424757856392563537802339735359978831013
#num1 = 37
#num2 = 71


publicKeyOfPKDA , privateKeyOfPKDA = helpers.generates_asymmetric_keys(num1, num2)


publicKeysOfClients = {}
def getClientKey(gensocket):
    while True:
        connection, client_address = gensocket.accept()
        data = connection.recv(2048)
        data=data.decode('utf-8')  
        Enc_KeyOwner, Enc_client_e, Enc_client_n = data.split(';')
        Enc_KeyOwner = int(Enc_KeyOwner)
        Enc_client_e = int(Enc_client_e)
        Enc_client_n = int(Enc_client_n)
        KeyOwner = helpers.decrypt(Enc_KeyOwner, privateKeyOfPKDA)
        client_e = helpers.decrypt(Enc_client_e, privateKeyOfPKDA)
        client_n = helpers.decrypt(Enc_client_n, privateKeyOfPKDA)
        KeyOwner = helpers.convertToStr(KeyOwner)
        print("KeyOwner",KeyOwner)
        print("Client_e",client_e)
        print("Client_n",client_n)

        publicKeysOfClients[KeyOwner]=(client_e,client_n)
        f = open("publicKeysOfClients.txt","w")
        f.write(str(publicKeysOfClients))
        f.close()

        connection.close()
        
def sharePublicKey(sharesocket):
    while True:
        connection, client_address = sharesocket.accept()
        #step 1: It recieves the request
        data = connection.recv(2048).decode('utf-8')
        
        Enc_Sender,Enc_Request, Enc_T1 = data.split(";")
        Sender = helpers.convertToStr(helpers.decrypt(int(Enc_Sender), privateKeyOfPKDA))
        Request = helpers.convertToStr(helpers.decrypt(int(Enc_Request), privateKeyOfPKDA))
        T1 = int(helpers.decrypt(int(Enc_T1), privateKeyOfPKDA))
        T2 = int(time.time() * 1000)
        if T2-T1 > 10000:
            print("Request Expired")
            connection.close()
            continue
        else:
            timeLag = T2-T1
            print("Time Lag",timeLag, "milliseconds")


        PublicKeyofRequest = publicKeysOfClients[Request]
        requested_e = PublicKeyofRequest[0]
        requested_n = PublicKeyofRequest[1]

        
        # print("The requested E and N are: ", requested_e, requested_n)
        # print("The public key of the requester is: ", PublicKeyOfRequester)
        Enc_requested_e = helpers.encrypt(requested_e, privateKeyOfPKDA)
        Enc_requested_n = helpers.encrypt(requested_n, privateKeyOfPKDA)
        Message = str(requested_n+requested_e+T1)
        
        HashedMessage = helpers.convertToNum(hashlib.sha1(Message.encode('utf-8')).hexdigest())
        Enc_Hash = helpers.encrypt(HashedMessage,privateKeyOfPKDA)
    
        Enc_T1 = helpers.encrypt(T1, privateKeyOfPKDA)
        toSend = str(Enc_requested_e)+";"+str(Enc_requested_n)+";"+str(Enc_T1)+";"+str(Enc_Hash)

        connection.sendall(str(toSend).encode('utf-8'))
        
        #step 3 " Close the connection"
        
        connection.close()
        

print("Hey")

if __name__ == "__main__":
    gensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    gensocket.bind((HOST,PORT))
    gensocket.listen(5)

    sharesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sharesocket.bind((HOST,PORT+10))
    sharesocket.listen(5)

    t1 = threading.Thread(target = getClientKey, args=(gensocket,))
    t2 = threading.Thread(target = sharePublicKey, args=(sharesocket,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()