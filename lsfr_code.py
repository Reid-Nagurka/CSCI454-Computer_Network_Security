#!/usr/bin/python2.7

import random
import time
from mr import is_probable_prime as is_prime

def int_to_bin(i):
    o = '{0:08b}'.format(i)
    o = (8 - (len(o) % 8)) * '0' + o
    return o

def bin_to_int(b):
    return int(b,2)

def str_to_bin(s):
    o = ''
    for i in s:
        o += '{0:08b}'.format(ord(i))
    return o

def bin_to_str(b):
    l = [b[i:i+8] for i in xrange(0,len(b),8)]
    o = ''
    for i in l:
        o+=chr(int(i,2))
    return o

def egcd(a, b): # can be used to test if numbers are co-primes
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
        #if g==1, the numbers are co-prime

def modinv(a, m):
    #returns multiplicative modular inverse of a in mod m
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

class lfsr:
    # Class implementing linear feedback shift register. Please note that it operates
    # with binary strings, strings of '0's and '1's.
    taps = []
    
    def __init__ (self, taps):
    # Receives a list of taps. Taps are the bit positions that are XOR-ed
    #together and provided to the input of lfsr
        self.taps = taps
    register = '1111111111111111'
    # initial state of lfsr

    def clock(self, i='0'):
    #Receives input bit and simulates one cycle
    #This include xoring, shifting, updating input bit and returning output
    #input bit must be XOR-ed with the taps!!

    ## -- Implement me -- ##
        o = ''
        xor = ord(i)
        charray = list(self.register)
        #xor taps w/ input bit
        for el in self.taps:
            xor ^= ord(self.register[el])  

        bit = chr(xor)
        #print bit
        #bit is now what should be put into the first spot after shifts
        #shift everything right one
        o = charray[len(charray) - 1]
        count = len(charray) - 1
        while (count > 0):
            charray[count] = charray[count - 1]
            count -= 1
            
        #put xored value in first spot
        charray[0] = bit
        
        
        temp = ''.join(charray)
        self.register = temp
        return o #returns output bit

    def seed(self, s):
    # This function seeds the lfsr by feeding all bits from s into input of
    # lfsr, output is ignored
        for i in s:
            o = self.clock(i)

    def gen(self,n,skip=0):
    # This function clocks lfsr 'skip' number of cycles ignoring output,
    # then clocks 'n' cycles more and records the output. Then returns
    # the recorded output. This is used as hash or pad
        for x in xrange(skip):
            self.clock()
        out = ''
        for x in xrange(n):
            out += self.clock()
        return out

def H(inp):
    # Hash function, it must initialize a new lfsr, seed it with the inp binary string
    # skip and read the required number of lfsr output bits, returns binary string
    
    ## -- Implement me -- ##
    l = lfsr([2,4,5,7,11,14])
    l.seed(inp)
    #number of output bits and skip given on Piazza
    return l.gen(56, 1000)
    
    # Example: H(int_to_bin(0)) -> '10111000111111111111111000110001010010000101011101001100'
    # Example: H('0') -> '01010101010001110111000111111111111111000110001010010000'
    # Example: H(int_to_bin(777)) -> '00010101011001100111111100110111101011001111001101011001'

def enc_pad(m,p):
    # encrypt message m with pad p, return binary string
    o = ''

    ## -- Implement me -- ##
    
    while(len(m) > len(p)):
        p += p
    
    
    i = 0
    while (i < len(m)):
        o += str(ord(m[i]) ^ ord(p[i]))
        
        i += 1
    return o

def GenRSA():
    # Function to generate RSA keys. Use the Euler's totient function (phi)
    # As we discussed in lectures. Function must: 1) seed python's random number
    # generator with time.time() 2) Generate RSA primes by keeping generating
    # random integers of size 512 bit using the random.getrandbits(512) and testing
    # whether they are prime or not using the is_prime function until both primes found.
    # 3) compute phi 4) find e that is coprime to phi. Start from e=3 and keep
    # incrementing until you find a suitable one. 4) derive d 5) return tuple (n,e,d)
    # n - public modulo, e - public exponent, d - private exponent

    random.seed(time.time())

    ## -- Implement me -- ##
    prime1 = random.getrandbits(512)
    prime2 = random.getrandbits(512)
    while not is_prime(prime1):
        prime1 = random.getrandbits(512)
        
    while not is_prime(prime2):
        prime2 = random.getrandbits(512)
            
    n = prime1 * prime2
    phi = (prime1 - 1) * (prime2 - 1)
    
    #start at e = 3. if the greatest common divisor of e and phi is 1, e is relatively prime to phi
    e = 3
    #if the first value returned from egcd is 1, then e and phi are coprimes
    g = egcd(e, phi)[0]
    while g != 1:
        e += 1
        g = egcd(e, phi)[0]
    
    #derive d
    d = modinv(e, phi)
    return (n, e, d)    

#main
#Problem 1
'''
l = lfsr([2,4,5,7,11,14])
l.seed(int_to_bin(1234))
print (l.gen(10,2000))
'''
#Problem 2
#H(str_to_bin('My name is Reid Nagurka and I like pho.'))

#Problem 3
'''
s = "Hello, my name is Reid Nagurka"
bs = str_to_bin(s)
l = lfsr([2,4,5,7,11,14])
l.seed(int_to_bin(77))
pad = l.gen(len(bs), 1000)
print pad
cipher = enc_pad(bs, pad)
print cipher

print bin_to_str(cipher)
print bin_to_str (enc_pad(cipher,pad))
'''
#Problem 4
'''
(n, e, d) = GenRSA()
print (n, e , d)
print n
print e
print d
#e is public, d is private
'''
#Problem 5
'''
A and B agrees on a secret key d
When A wants to transfer message plaintext; A encrypts the message with the key: Ed(plaintext) = ciphertext
A sends the ciphertext to B
B receives the C and decrypts it Dd(ciphertext) = plaintext recovering the original message M
Eve cannot recover original M because she does not know K
'''
(n, e, d) = GenRSA()
#if encrypted with private, can only be decrypted with public
#if encrypted with public, can only be decrypted with private
#both parties have plaintext and same hashing algorithm
plaintext = 'Reid Nagurka rnagurka@email.wm.edu'
#Alice hashes plaintext
hashed = H(plaintext)
print "hashed: ", hashed
plain_bin = str_to_bin(hashed)
plain_int = bin_to_int(plain_bin)

#Alice encrypts hash with her private key d
signature = pow(plain_int, d, n)
print "signature: ", signature

#Bob decrypts signature with public key:
message = pow(signature, e, n)
print "decrypted with public key: ", message

#compare the resulting message with the hashed computed using the hashing function:

#the hashed message with e is the same as the original hash, meaning verification is good
message_bin = int_to_bin(message)
message_str = bin_to_str(message_bin)
print "newly computed hash: ", message_str
#in practice, the signature would be attached to the message
