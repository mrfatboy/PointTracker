import webbrowser
import codecs
import os
from Crypto.Cipher import AES
from Crypto import Random
import base64


#
## Python can use json from standard library
#import json
## Create object in python
#ob = {'name':'Json','email':['x@a.com','x@b.com']}
## Convert python object into json string format
#jstring = json.dumps(ob)
#print jstring
## Load python object from json string
#jobject = json.loads(jstring)
#print jobject









def write_file (text,filename):

    current_directory  = os.path.dirname(os.path.realpath(__file__))            #get current working directory
    filepath  = os.path.join(current_directory, filename)                       #add the filename to it


    f = codecs.open(filepath, 'w', encoding='utf-8')
    try:
        f.write(text)
    except Exception as e:
        print ('Trying to write file:',filename)
        msg = "An exception of type {0} occured, these were the arguments:\n{1!r}"
        print (msg.format(type(e).__name__, e.args))
    finally:
        f.close()
    return




def read_file (filename):

    current_directory  = os.path.dirname(os.path.realpath(__file__))            #get current working directory
    filepath  = os.path.join(current_directory, filename)                       #add the filename to it

    try:
        f = open(filepath,"r")
    except IOError as e:
        msg = "An exception of type {0} occured, these were the arguments:\n{1!r}"
        print (msg.format(type(e).__name__, e.args))
        data = None
        return data

    try:
        data = f.read()
    except IOError as e:
        print ('Trying to read file:',filename)
        msg = "An exception of type {0} occured, these were the arguments:\n{1!r}"
        print (msg.format(type(e).__name__, e.args))
        data = None
    finally:
        f.close()
    return data



def strToFile(text, filename):
    """Write a file with the given name and the given text."""
    output = open(filename,"w")
    output.write(text)
    output.close()
    return

def display_webpage(webpageText, filename='tempDisplayWebpage.html'):
    '''Start your webbrowser on a local file containing the text
    with given filename.'''
    write_file(webpageText,filename)
    webbrowser.open(filename)
    return






def pad_str(s):                                                         #input is a string
#this pads a string with unicode of the actually quantity of what it needs to pad
    BS = 16
    return (s + (BS - len(s) % BS) * chr(BS - len(s) % BS))             #return a byte string

def unpad_str(byte_str):                                                 #input is byte string
    x = byte_str[0:-byte_str[-1]]
    return (x)                                                           #return a byte string


def encrypt (key,string):
    s = pad_str(string)                                      #pad to nearest lenght of multiple of 16
    iv = Random.new().read( AES.block_size )
    cipher = AES.new(key, AES.MODE_CBC, iv )
    c = cipher.encrypt(s)
    enc_str = base64.b64encode(iv+c)
    return (enc_str.decode())                                #returns encoded64 and encrypted string


def decrypt (key,enc_str):                                    #encrypted string
    enc = base64.b64decode(enc_str)
    iv = enc[:16]                                           #IV is embedded in first 16 of string
    cipher = AES.new(key, AES.MODE_CBC, iv )
    c = cipher.decrypt( enc[16:] )                          #the string with want is after the IV
    dec_str = unpad_str(c)
    return (dec_str.decode())                               #returns decrypted string





#try:

#except Exception as e:
#    msg = "An exception of type {0} occured, these were the arguments:\n{1!r}"
#    print (msg.format(type(e).__name__, e.args))