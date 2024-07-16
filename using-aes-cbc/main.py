import os

from cryptography.hazmat.primitives.ciphers import Cipher 
from cryptography.hazmat.primitives.ciphers.algorithms import AES 
from cryptography.hazmat.primitives.ciphers.modes import CBC 
from cryptography.hazmat.primitives import padding 

if __name__ == "__main__":
    #plaintext to be kept confidential 
    plaintext = b"Fundamental Cryptography in Python"
    print(plaintext)

    #generate 256-bit-key and 128-random-bits for cbc 
    key = os.urandom(256//8)
    random_128_bits = os.urandom(256//16)

    #create the aes-cbc cipher
    aes_cbc_cipher = Cipher(AES(key),CBC(random_128_bits))

    #encrypt the plaintext 
    ciphertext = aes_cbc_cipher.encryptor().update(plaintext)
    print(f"Encrypted text with no padding: {ciphertext}")

    #decrypt the cipher text 
    recovered_plaintext = aes_cbc_cipher.decryptor().update(ciphertext)
    print(f"Recovered plaintext(no padding): {recovered_plaintext}")

    #pad the plaintext 
    pkcs7_padder = padding.PKCS7(AES.block_size).padder()
    padded_plaintext = pkcs7_padder.update(plaintext) + pkcs7_padder.finalize()
    print(f"Padded plaintext: {padded_plaintext}")    

    #encrypt the padded plaintext 
    ciphertext = aes_cbc_cipher.encryptor().update(padded_plaintext)
    print(f"Encrypted text with padding: {ciphertext}")

    #decrypt the padded ciphertext 
    recovered_padded_plaintext = aes_cbc_cipher.decryptor().update(ciphertext)
    print(f"Recovered padded plaintext: {recovered_padded_plaintext}")

    #remove padding 
    pkcs7_unpadder = padding.PKCS7(AES.block_size).unpadder()
    recovered_plaintext = pkcs7_unpadder.update(recovered_padded_plaintext) + pkcs7_unpadder.finalize()
    print(f"Recovered text with padding removed: {recovered_plaintext}")

    #read the image into the memory

    with open("mandelbrot.ppm","rb") as image:
        image_file = image.read()
        image_bytes = bytearray(image_file)
    
    #keep the ppm header 
    header_size = 60 
    image_header = image_bytes[:header_size] 
    image_body = image_bytes[header_size:]

    #pad the image body 
    pkcs7_padder = padding.PKCS7(AES.block_size).padder()
    padded_image_body = pkcs7_padder.update(image_body) + pkcs7_padder.finalize()

    #encrypt the image body 
    encrypted_image_body = aes_cbc_cipher.encryptor().update(padded_image_body)

    #assemble the encrypted image 
    encrypted_image = image_header + encrypted_image_body
    #create and save the full encrypted image 

    with open("mandelbrot_aes_cbc_encrypted.ppm","wb") as image_encrypted:
        image_encrypted.write(encrypted_image)

    #decrypt the image body 

    recovered_image_body = aes_cbc_cipher.decryptor().update(encrypted_image_body)
    
    #assemble the recovered image 
    recovered_image = image_header + recovered_image_body 

    #create and save the full recovered image

    with open("mandelbrot_recovered.ppm","wb") as image_recovered:
        image_recovered.write(recovered_image)



