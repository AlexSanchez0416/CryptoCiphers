'''
FILE: plftest.py
PyVERSION:  3.5

TO RUN PROGRAM:  $python3 plftest

DESCRIPTION: Test program for PlayfairCipher class

FILES REQUIRED: CipherInterface.pyc
				PlayfairCipher.pyc	

TEST INPUTS:
key: monarchy
message: bolloon

TEST OUTPUTS:
Cipertext output : HASUPMNA
decrypted ciphertext: BOLXLOON

'''
from CipherInterface import CipherInterface

from PlayfairCipher import Playfair

myPLF = Playfair()

key = input ("Enter the key: ")
msg = input ("enter the ciphertext: ")

if myPLF.setKey(key) == False:
	 print("Invalid key for Playfair Cipher. Key can only contain alphabetical characters!")

#out = myPLF.encrypt(msg)
#print (out)

decrypted = myPLF.decrypt(msg)
print (decrypted)
