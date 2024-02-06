ENCRYPTION
Run the encryption.py program
The program asks you for a key and a  plaintext
Enter both in hexadecimal format
The program then encrypts the plaintext using the given key using AES encryption. 
The outputs of all the rounds get written in the Encryption_states.txt file
The output of round 10 is the final ciphertext
We get the final cipher in text format

DECRYPTION:
To decrypt we have to use the decrypt.py program
Now run this program and when asked for the key, enter the same key as used to encrypt.
The Cipher is the output of the encrypt.py in hexadecimal format 
Eg. If output of the encrypt program is cipher =  fa7a56618355a7e379a67eb9f01cea43
Use this as cipher for the decrypt program

The decrpytion is again carried out in 10 round and the output of each round is stored in the 'Decryption_states.txt' file

It can be verified that the output of Round 1 of encryption is same as Round 9 of decryption by inspecting the files

Similarly it can be verified that the output of Round 9 of encryption is same as Round 1 of decryption by inspecting the files