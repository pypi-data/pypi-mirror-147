

# Encrypt
# ================
def aichin(search_word):
    
    phrase = search_word.split(' ')
    words = {}
    ctr = 0
    encrypted = ''
    with open('a2/dict.txt') as f:
            lines = [line.rstrip('\n') for line in f]
    for line in lines:  
            words[line.lower()] = ctr
            ctr = ctr + 1
    for p in phrase:
            if p.lower() in words:
                position = hex(words.get(p.lower()))
            else:
                    position = p
            encrypted = encrypted + str(position) + '.'        
    return (encrypted)

# Decrypt
# ================
def aichout(search_word):
    phrase = search_word.split('.')
    words = {}
    ctr = 0
    encrypted = ''
    with open('a2/dict.txt') as f:
            lines = [line.rstrip('\n') for line in f]
    for line in lines:  
            words[ctr] = line.lower()
            ctr = ctr + 1

    # print (phrase)
    for p in phrase:        
            if (int(p, 16)):
                    position = words[int(p, 16)]
            encrypted = encrypted + str(position) + ' '        
    return (encrypted)