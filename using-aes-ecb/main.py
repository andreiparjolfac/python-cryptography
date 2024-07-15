import os;
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES;
from cryptography.hazmat.primitives.ciphers.modes import ECB
from cryptography.hazmat.primitives import padding

if __name__ == "__main__":
    # Plain text to be kept confidential
    plaintext = b'Fundamental Cryptography in Python'
    print(f"Plaintext: {plaintext}")
    #256 bit AES  key
    key = os.urandom(256//8)
    print(key)
    #create the AES ECB Cipher
    aes_ecb_cipher = Cipher(AES(key),ECB())

    #Encrypt the plaintext
    ciphertext = aes_ecb_cipher.encryptor().update(plaintext)
    print(f"CipherText:{ciphertext}")

    #Decrypt
    recovered_plaintext=aes_ecb_cipher.decryptor().update(ciphertext)
    print(f"Decrypted ciphertext: {recovered_plaintext}")

    #pad the plaintext
    pkcs7_padder = padding.PKCS7(AES.block_size).padder()
    padded_plaintext = pkcs7_padder.update(plaintext) + pkcs7_padder.finalize()
    print(f"Padded plaintext: {padded_plaintext}")
    
    #encrypt paded plaintext
    ciphertext = aes_ecb_cipher.encryptor().update(padded_plaintext)
    print(f"Encrypted padded plaintext: {ciphertext}")
    #decrypt to paded plaintext
    recovered_plaintext_with_padding = aes_ecb_cipher.decryptor().update(ciphertext)
    print(f"Recovered padded plaintext: {recovered_plaintext_with_padding}")
    #remove padding
    pkcs7_unpadder = padding.PKCS7(AES.block_size).unpadder()
    recovered_plaintext = pkcs7_unpadder.update(recovered_plaintext_with_padding) + pkcs7_unpadder.finalize()
    print(f"Final text is:{recovered_plaintext}")
    assert(plaintext == recovered_plaintext)

    #encrypt mandelbrot.ppm

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
    encrypted_image_body = aes_ecb_cipher.encryptor().update(padded_image_body)

    #assemble the encrypted image
    encrypted_image = image_header + encrypted_image_body
    #create and save the full encrypted image

    with open("mandelbrot_encrypted_aes_ecb.ppm","wb") as image_encrypted:
        image_encrypted.write(encrypted_image)