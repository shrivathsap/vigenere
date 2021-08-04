alph = [chr(x) for x in range(ord('A'), ord('Z') + 1)] 

mes = str(input())
key = str(input("key:"))
keyU = key.upper()

def find_index(element, List = alph):
    for i in range(len(List)):
        if List[i] == element:
            return i

shifts = [find_index(letter) for letter in keyU]
n = len(shifts)
m = len(alph)

def encrypt(message):
    message = message.upper()
    key_position = 0
    encrypted = ''
    for i in range(len(message)):
        if message[i] not in alph:
            encrypted += message[i]
            continue
        shift = shifts[key_position%n]
        letter_number = find_index(message[i])
        encrypted += alph[(letter_number+shift)%m]
        key_position += 1
    return encrypted

print(encrypt(mes))
