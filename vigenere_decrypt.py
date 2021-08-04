'''IMPORTANT NOTE: If the text is too long and there are too many overlaps etc, then it is best to skip three in the marked place below, i.e., when considering strings
of length k, don't take every such string, take every third such string or something, it makes the process faster, but inaccurate when ciphertext is short (in which
case, take every such string).
'''
import statistics

ciphertext = str(input())
ciphertext = ciphertext.upper()

alph = [chr(ord) for ord in range(ord('A'), ord('Z')+1)]
std_freq = [8.2, 1.5, 2.8, 4.3, 13, 2.2, 2, 6.1, 7, 0.15, 0.77, 4, 2.4,
            6.7, 7.5, 1.9, 0.095, 6, 6.3, 9.1, 2.8, 0.98, 2.4, 0.15, 2, 0.074]#standard frequency of letters in english, taken from wikipedia

def best_divisor(List):#given a list of numbers, gives tuples of how many numbers each x\in List divides, helps in identifying key length
    list1 = list(set(List))
    scores = []
    for num in list1:
        multiples = [x for x in list1 if x%num == 0]
        if len(multiples)>1:#x trivially divides x, so we ignore that
            scores.append((num, len(multiples)))
##    M = max([item[1] for item in scores])
##    best_div = [item[0] for item in scores if item [1] == M]
##    print(best_div)
    print(sorted(scores, key=lambda x:x[1], reverse = True))

def find_index(element, List = alph):
    for i in range(len(List)):
        if List[i] == element:
            return i

def frequency_analysis(string):
    #first obtain the frequency of letters in the given string
    string = string.upper()
    scores = []
    for letter in alph:
        scores.append(100*len([item for item in string if item == letter])/len(string))

    #next shift the frequencies and see which agrees the most with the standard frequency using a chi-squared method. Maximum doesn't always mean correct, sometimes
    #it is the second maximum that is the correct shift
    overlap_score = []
    for i in range(len(alph)):
        overlap_score.append(sum([std_freq[j]*scores[(j+i)%len(alph)] for j in range(len(alph))]))
    M = max(overlap_score)
    return([i for i in range(len(overlap_score)) if overlap_score[i] == M])

def score_calc(crypt):
    score_list = []
    for i in range(1, len(crypt)):
        score = 0
        for j in range(len(crypt)):
            try:
                if crypt[i+j] == crypt[j] and crypt[j]in alph:#shift by i and compare only letters, comparing spaces gives false counts. Eg, it is common to group the
                                                            #ciphertext into blocks of 5, counting spaces makes the key length more likely to be 6 because every 6th
                                                            #letter is a space
                    score += 1
            except:
                continue
        score_list.append((i, score))
    avg_overlap = statistics.mean([item[1] for item in score_list])
    stdeviation = statistics.stdev([item[1] for item in score_list])
    above_avg = [item for item in score_list if item[1] >= avg_overlap]
    above_avg1 = [item for item in score_list if item[1] >= avg_overlap+1*stdeviation]
    above_avg2 = [item for item in score_list if item[1] >= avg_overlap+2*stdeviation]
    above_avg3 = [item for item in score_list if item[1] >= avg_overlap+3*stdeviation]

    print(avg_overlap, stdeviation)
    for l in [above_avg, above_avg1, above_avg2, above_avg3]:
        if len(l)>0:
            print((l[-1][0]-l[0][0])/len(l))
        else:
            print(0)
##    dist0 = (above_avg[-1][0]-above_avg[0][0])/(len(above_avg))
##    dist1 = (above_avg1[-1][0]-above_avg1[0][0])/(len(above_avg1))
##    dist2 = (above_avg2[-1][0]-above_avg2[0][0])/(len(above_avg2))
##    dist3 = (above_avg3[-1][0]-above_avg3[0][0])/(len(above_avg3))
##    print(dist0, dist1, dist2, dist3)
    distances = []
##    min_length = int(input("Will now look for repeating strings, what minimum length would you like to start at? If average overlaps are high, please enter a high number:"))
    crypt = ''.join(crypt.split(' '))#remove spaces
    for k in range(3, int(avg_overlap)+1):#look for repeating strings of lenght a least 3 and at most the average overlap score
        k_at_a_time = [crypt[i:i+k] for i in range(len(crypt)-k+1)]###MARKED POINT: instead of range(...) use range(0, len(crypt)-k+1, 3) or something
        for sequence in set(k_at_a_time):
            bazinga = []#i'm running out of var names
            for i in range(len(k_at_a_time)):
                if k_at_a_time[i] == sequence:
                    bazinga.append(i)
            dist = (bazinga[-1]-bazinga[0])#/len(bazinga)
            if dist!= 0:
                distances.append(dist)
    print(list(set(distances)))
    best_divisor(distances)

##    print([item for item in score_list if item[1] >= 15])#many zeros, so I took arbitrary level of score being greater than --;  might be stupid

score_calc(ciphertext)
key_length = int(input("What key length to try?"))

def key_identify(crypt, key_length):
    crypt = crypt.upper()
    spaced_letters = []
    key_shifts = []
    #remove all useless characters, otherwise stuff like spaces mess up the actual frequencies
    new_crypt = ''
    for letter in crypt:
        if letter in alph:
            new_crypt+= letter
    crypt = new_crypt
    for i in range(key_length):
        spaced_letters.append(crypt[i::key_length])
    for spaced in spaced_letters:
        key_shifts.append(frequency_analysis(spaced))
    key_letters = []
    for shifts in key_shifts:
        letters = [alph[i] for i in shifts]
        key_letters.append(letters)
    print(key_letters)

key_identify(ciphertext, key_length)
key = str(input("What key would you like to try?"))

def decrypt(message, key):
    keyU = key.upper()
    shifts = [find_index(letter) for letter in keyU]
    n = len(shifts)
    m = len(alph)
    message = message.upper()
    key_position = 0
    decrypted = ''
    for i in range(len(message)):
        if message[i] not in alph:
            decrypted += message[i]
            continue
        shift = shifts[key_position%n]
        letter_number = find_index(message[i])
        decrypted += alph[(letter_number-shift)%m]
        key_position += 1
    return decrypted

print(decrypt(ciphertext, key))
