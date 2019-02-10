"""
CPSC 452
Assignment 1
Playfair Cipher Class
Programmer: Alejandro Sanchez
Python 3.3
"""

from CipherInterface import CipherInterface
import string
import re

class Playfair(CipherInterface):
  
  __slots__ ={'_key'}

  #Default initialization
  def __init__(self):
    self._key = None

  # Function: Sets the encryption/decryption key for the instance of the Playfair Cipher
  # Input:  An alphabetical key
  # Output: True if the key is set, otherwise returns False indicating it is invalid
  def setKey(self,key):
    if key.isalpha() == True:                               # If the key contains only alphabetical characters
      self._key = self.formatKey(key)                       # Set the encryption/decryption key
      return True                                           # Return True, Key successfully set
    else:                                                   # Otherwise...
      return False                                          # The Key is invalid

  # Function: Removes Duplicate Characters
  # Input:  A string of letters
  # Output: A new string of only unique characters with order preserved
  def uniqify (self,key):
    seen = set()
    seen_add = seen.add
    return [letter for letter in key if not (letter in seen or seen_add(letter))]

  # Function: Sets up input to be used as a key for Playfair Cipher
  # Input: String of characters
  # Output: Properly formatted key to be used with creating Playfair Cipher encryption matrix
  def formatKey(self,key):
    myKey = key.replace(" ","")                             # remove whitespace
    myKey += string.ascii_uppercase                         # append A-Z alphabet to key
    myKey = myKey.upper()                                   # Capiltalize key
    myKey = myKey.replace("J","I")                          # replace J with I (i.e. I and J will occupy same space in matrix)
    myKey = self.uniqify(myKey)                             # Remove duplicates
    return myKey
        
  # Function: Generates Playfair Key Matrix using properly formatted key
  # Input: Properly formatted key
  # Output: 2D list comprised of key followed by remainder of unique alphabetic characters (J is converted to I)
  def createMatrix(self,key):
    matrix = []                                             # Empty list
    count = 0                                               # Keep track of character in key string
    for i in range(5):                                      # 5 Columns
      matrix.append([])                                     # append list to each column
      for j in range(5):                                    # 5 Rows
        matrix[i].append('')                                # Insert empty cell for each row
        matrix[i][j] = key[count]                           # Insert characters from key
        count += 1                                          # Go to next character in key
    return matrix                                           # return 2d list containing key matrix

  # Function: Converts text to digraphs, inserting and appending X's when needed
  # Input: Text to convert. Can be Plaintext or Ciphertext.
  # Output: list of digraphs where each digraph is a list
  def createDigraphs(self,msg):
    msg = msg.upper()                                       # Capitalize text
    msg = msg.replace(" ","")                               # remove whitespace

    digraphs = []                                           # initialize empty list of digraphs
    count = 0                                               # count to keep track of position in text
    while count < len(msg):
      digraph = ''                                          # single digraph
      if count + 1 == len(msg):                             # End of string found after one letter in digraph
        digraph = msg[count] + 'X'                          # So append X to digraph
        digraphs.append(digraph)                            # append digraph to list of digraphs
        break                                               # end of plaintext, exit while loop
      elif msg[count] != msg[count + 1]:                    # digraph does not contain consecutive characters
        digraph = msg[count] + msg[count + 1]               #So create digraph of character pair
        digraphs.append(digraph)                            #append digraph to list of digraphs
        count += 2                                          # Go to next pair of letters in string
      else:                                                 #Otherwise digraph contains consecutive characters
        digraph = msg[count] + 'X'                          # append X to first of consecutive letters
        digraphs.append(digraph)                            # append digraph to list of digraphs
        count += 1                                          # Go to next character in string
    return digraphs                                         #return list of digraphs
  # Function: Search and find index of letter from a 5x5 2D list
  # Input: 5x5 2 dimensional list. In this case, the Playfair Key Matrix
  # Output: coordinates of desired letter
  def find(self,twoDimList, letter):
    coords = []                                             # empty list
    for i in range(5):                                      # search columns
      for j in range(5):                                    # search rows
        if twoDimList[i][j] == letter:                      # check contents of index for letter
          coords.append(i)                                  # coords[0] = column location of letter in key matrix
          coords.append(j)                                  # coords[1] = row location of letter in key matrix
    return coords                                           # return key matrix coordinates of letter


  # Function: Encrypt message using Playfair Cipher
  # Input: plaintext message that consists of only alphabetic characters
  # Output: Cipertext using Playfair Cipher
  def encrypt(self,plaintext):
    matrix = self.createMatrix(self._key)                   # Generate playfair key matrix with given key
    enciphered = ""                                         # Store encrypted text string
    digraphs = self.createDigraphs(plaintext)               # Convert plaintext into digraphs
    for digraph in digraphs:                                # Encrypt one digraph at a time
      first = digraph[0]
      second = digraph[1]
      #Find matrix index of letter in each digraph (I and J occupy same index)
      if first == "J":                                    # If first letter in digraph is 'J'
        firstLetterPos = self.find(matrix,"I")              # Use index of 'I' since they occupy same index within key Matrix
      else:                                                 # Otherwise . . .
        firstLetterPos = self.find(matrix,first)            # Index of first letter in digraph from Playfair Key Matrix
      if second == "J":                                     # If second letter in digraph is 'J'
        secondLetterPos = self.find(matrix,"I")             # Use index of 'I' since they occupy same index within key Matrix
      else:                                                 # Otherwise . . .
        secondLetterPos = self.find(matrix,second)          # Index of second letter in digraph from Playfair Key Matrix
      #Apply encryption playfair rules
      if firstLetterPos[0] == secondLetterPos[0]:           # Letters are in same row: circular shift right by 1
        firstCipherLetter = matrix[firstLetterPos[0]][(firstLetterPos[1] + 1) %5]
        secondCipherLetter = matrix[secondLetterPos[0]][(secondLetterPos[1] + 1) %5]
      elif firstLetterPos[1] == secondLetterPos[1]:         # Letters are in same column: circular shift down by 1
        firstCipherLetter = matrix[(firstLetterPos[0]+ 1) %5][firstLetterPos[1]]
        secondCipherLetter = matrix[(secondLetterPos[0] + 1) %5][secondLetterPos[1]]
      else:                                                 # Otherwise {row of first & column of second, row of second & column of first}
        firstCipherLetter = matrix[firstLetterPos[0]][secondLetterPos[1]]
        secondCipherLetter = matrix[secondLetterPos[0]][firstLetterPos[1]]
      enciphered += firstCipherLetter + secondCipherLetter  #Append digraph to ciphertext
    return enciphered
                
  # Function: Decrypt message using Playfair Cipher
  # Input: Ciphertext message that was encrypted using Playfair Cipher
  # Output: Decrypted Playfair Ciphertext
  def decrypt(self,ciphertext):
    matrix = self.createMatrix(self._key)                   # Generate playfair key matrix with given key
    deciphered = ""                                         # Store decrypted text string
    digraphs = self.createDigraphs(ciphertext)              # Convert ciphertext into digraphs
    for digraph in digraphs:                                # Decrypt one digraph at a time
      first = digraph[0]
      second = digraph[1]

      firstLetterPos = self.find(matrix,first)              # Index of first letter in digraph from Playfair Key Matrix
      secondLetterPos = self.find(matrix,second)            # Index of second letter in digraph from Playfair Key Matrix

      #Apply decrpytion playfair rules
      if firstLetterPos[0] == secondLetterPos[0]:           # Letters are in same row: circular shift left by 1
        firstPlainLetter = matrix[firstLetterPos[0]][(firstLetterPos[1] - 1 + 5) %5]
        secondPlainLetter = matrix[secondLetterPos[0]][(secondLetterPos[1] - 1 + 5 )%5]

      elif firstLetterPos[1] == secondLetterPos[1]:         # Letters are in same column: circular shift up by 1
        firstPlainLetter = matrix[(firstLetterPos[0]- 1 + 5 )% 5][firstLetterPos[1]]
        secondPlainLetter = matrix[(secondLetterPos[0] - 1 + 5 )% 5][secondLetterPos[1]]
      else:                                                 # Otherwise {row of first & column of second, row of second & column of first}
        firstPlainLetter = matrix[firstLetterPos[0]][secondLetterPos[1]]
        secondPlainLetter = matrix[secondLetterPos[0]][firstLetterPos[1]]

      deciphered += firstPlainLetter + secondPlainLetter      #Append digraph to plaintext
    return deciphered
       
