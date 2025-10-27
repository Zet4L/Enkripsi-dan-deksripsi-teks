def create_playfair_matrix(key):
    matrix = []
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Tanpa 'J'
    key = ''.join(sorted(set(key), key=key.index)).upper()  # Menghapus duplikat

    for char in key:
        if char in alphabet and char not in matrix:
            matrix.append(char)
            alphabet = alphabet.replace(char, '')

    for char in alphabet:
        matrix.append(char)

    return matrix

def prepare_text(text):
    text = text.upper().replace('J', 'I')  # Ganti 'J' dengan 'I'
    prepared = []
    
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
        else:
            b = 'X'  # Tambahkan 'X' jika ada huruf ganjil

        if a == b:  # Jika kedua huruf sama, tambahkan 'X'
            prepared.append(a + 'X')
            i += 1
        else:
            prepared.append(a + b)
            i += 2
    
    return prepared

def playfair_encrypt(plaintext, key):
    matrix = create_playfair_matrix(key)
    prepared_text = prepare_text(plaintext)
    ciphertext = []

    for digraph in prepared_text:
        row1, col1 = divmod(matrix.index(digraph[0]), 5)
        row2, col2 = divmod(matrix.index(digraph[1]), 5)

        if row1 == row2:  # Satu baris
            ciphertext.append(matrix[row1 * 5 + (col1 + 1) % 5])
            ciphertext.append(matrix[row2 * 5 + (col2 + 1) % 5])
        elif col1 == col2:  # Satu kolom
            ciphertext.append(matrix[((row1 + 1) % 5) * 5 + col1])
            ciphertext.append(matrix[((row2 + 1) % 5) * 5 + col2])
        else:  # Persegi
            ciphertext.append(matrix[row1 * 5 + col2])
            ciphertext.append(matrix[row2 * 5 + col1])

    return ''.join(ciphertext)

def playfair_decrypt(ciphertext, key):
    matrix = create_playfair_matrix(key)
    prepared_text = prepare_text(ciphertext)
    plaintext = []

    for digraph in prepared_text:
        row1, col1 = divmod(matrix.index(digraph[0]), 5)
        row2, col2 = divmod(matrix.index(digraph[1]), 5)

        if row1 == row2:  # Satu baris
            plaintext.append(matrix[row1 * 5 + (col1 - 1) % 5])
            plaintext.append(matrix[row2 * 5 + (col2 - 1) % 5])
        elif col1 == col2:  # Satu kolom
            plaintext.append(matrix[((row1 - 1) % 5) * 5 + col1])
            plaintext.append(matrix[((row2 - 1) % 5) * 5 + col2])
        else:  # Persegi
            plaintext.append(matrix[row1 * 5 + col2])
            plaintext.append(matrix[row2 * 5 + col1])

    return ''.join(plaintext)

def vigenere_encrypt(plaintext, keyword):
    ciphertext = []
    keyword_repeated = (keyword * (len(plaintext) // len(keyword) + 1))[:len(plaintext)]
    
    for p, k in zip(plaintext, keyword_repeated):
        if p.isalpha():  # Hanya proses huruf
            shift = ord(k.lower()) - ord('a')
            base = ord('A') if p.isupper() else ord('a')
            encrypted_char = chr((ord(p) - base + shift) % 26 + base)
            ciphertext.append(encrypted_char)
        else:
            ciphertext.append(p)  # Tambahkan karakter yang bukan huruf tanpa perubahan
    
    return ''.join(ciphertext)

def vigenere_decrypt(ciphertext, keyword):
    plaintext = []
    keyword_repeated = (keyword * (len(ciphertext) // len(keyword) + 1))[:len(ciphertext)]
    
    for c, k in zip(ciphertext, keyword_repeated):
        if c.isalpha():
            shift = ord(k.lower()) - ord('a')
            base = ord('A') if c.isupper() else ord('a')
            decrypted_char = chr((ord(c) - base - shift) % 26 + base)
            plaintext.append(decrypted_char)
        else:
            plaintext.append(c)
    
    return ''.join(plaintext)

# Pilihan Cipher
cipher_choice = input("Pilih cipher (1: Vigenere, 2: Playfair): ")

if cipher_choice == '1':
    plaintext = input("Masukkan Teks untuk Vigenere > ")
    keyword = input("Masukkan Kata Kunci untuk Vigenere > ")
    encrypted = vigenere_encrypt(plaintext, keyword)
    decrypted = vigenere_decrypt(encrypted, keyword)

    print("\nVigenere Cipher:")
    print("Plaintext:", plaintext)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)

elif cipher_choice == '2':
    plaintext = input("Masukkan Teks untuk Playfair > ")
    playfair_key = input("Masukkan Kata Kunci untuk Playfair > ")
    encrypted = playfair_encrypt(plaintext, playfair_key)
    decrypted = playfair_decrypt(encrypted, playfair_key)

    print("\nPlayfair Cipher:")
    print("Plaintext:", plaintext)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)

else:
    print("Pilihan tidak valid. Silakan pilih 1 atau 2.")
