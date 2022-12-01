import Cryptodome.Util.Padding as padding
import Cryptodome.Util.number as crypto

PRIME_LENGTH = 512

class ElGamal():
    def __init__(self, chatApp, primeLength = PRIME_LENGTH):
        super().__init__()

    #Reference to chat app for logging
        self.chatApp = chatApp

        #Ensure prime length is a multiple of 128(required for prime generation)
        if primeLength % 128 == 0:
            self.primeLength = primeLength
        else:
            self.primeLength = PRIME_LENGTH

        self.blockSize = self.primeLength//8

    #Generate public variables prime order p and generator alpha
        self.primeOrder = crypto.getPrime(self.primeLength)
        self.publicGenerator = crypto.getRandomRange(2,self.primeOrder-1)

    #Choose secret key d from within cyclic group of order p
        self.secretKey = crypto.getRandomRange(2,self.primeOrder-2)

    #Compute public key alpha^d
        self.publicKey = pow(self.publicGenerator, self.secretKey, self.primeOrder)

    #Peer public keys to use
        self.hasPeerKey = False
        self.PeerKey = []
        

    #returns an array [public key beta, generator alpha, prime order p]
    def getPublicKey(self):
        return [self.publicKey, self.publicGenerator, self.primeOrder]

    #Set peer keys
    def setPeerKey(self,args):
        if(len(args) == 3):
            self.PeerKey = args
            self.hasPeerKey = True
            self.chatApp.log('peer key acquired')
    
    #Encrypt a string, output also string
    def encrypt(self, msg):
        #pad message to fit block size
        message = padding.pad(msg.encode(), self.blockSize)
        encrypted = ''

        if(self.hasPeerKey):
            #Peer public key components
            beta = self.PeerKey[0]
            alpha = self.PeerKey[1]
            p = self.PeerKey[2]

            #plaintext 
            plainText = self.encodeToBlocks(message)

            cipherText = []
            
            for block in plainText:
                #Ephemeral key generator i
                i = crypto.getRandomRange(2, p-2)
                #Ephemeral key 
                ke = pow(alpha, i, p)
                #masking key
                km = pow(beta, i, p)
                cipherText.append([((block * km) % p), ke])

            for c in cipherText:
                encrypted += str(c[0]) + ' ' + str(c[1]) + ' '
            
            #remove last space because it messes up the split
            encrypted = encrypted[:-1]
        else:
            self.chatApp.log('No peer public key established')
        

        return encrypted
            
    def decrypt(self, encrypted):
        cipherText = encrypted.split(' ')

        plainText = []

        for i in range(0, len(cipherText), 2):
            #compute masking key
            km = pow(int(cipherText[i+1]), self.secretKey, self.primeOrder)
            #decrypt and store decrypted blocks
            plainText.append((int(cipherText[i])*crypto.inverse(km,self.primeOrder)) % self.primeOrder)

        decoded = self.decodeFromBlocks(plainText)
        decrypted = padding.unpad(decoded, self.blockSize)
        return decrypted


    def encodeToBlocks(self, message):
        encoded = []

        #start at end of first block
        i = self.blockSize
        while i <= len(message):
            encoded.append(int.from_bytes(message[i-self.blockSize:i], 'big'))
            i += self.blockSize 
        
        return encoded

    def decodeFromBlocks(self, blocks):
        decoded = bytearray()

        for b in blocks:
            decoded += b.to_bytes(self.blockSize, 'big')
        
        return bytes(decoded)
        
