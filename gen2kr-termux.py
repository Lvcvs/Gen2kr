#!/usr/bin/python
# programma preso da:        Irenicus09 (https://github.com/irenicus)
# modificato e tradotto da:  Skull00    (https://github.com/Skull00)
import sys

global end,red,bright_yellow,error,sys_proc
end = '\033[0m'
red = '\033[1;31m'
bright_yellow = '\033[1;33m'
error = red + "!" + end
sys_proc = bright_yellow + "*" + end

def help():
    print """
  d888b  d8888b d8    db .d888b. db   dD d8888b.
 88' Y8b 88'    888   88 VP  `8D 88 ,8P' 88  `8D
 88      88oooo 88V8  88    odD' 88,8P   88oobY'
 88  ooo 88~~~~ 88 V8 88  .88'   88`8b   88`8b
 88. ~8~ 88.    88  V888 j88.    88 `88. 88 `88.
  Y888P  Y8888P VP   V8P 888888D YP   YD 88   YD
 ====( Automated Wordlist Generator Remake )====
 ====( Termux )==================( Edition )====

# Uso:
$ ./gen2kr -w <wordlist> -o <output> [opzioni]

 -c  Abilita la combinazione di parole tra le
     parole nella wordlist.
 -d  Aggiungi valori personalizzati da combinare
     nella wordlist (es,es,..)
 -e  Abilita il controllo wpa/wpa2 per le
     password generate.
 -h  Mostra questa schermata.
 -n  Abilita la combinazione di numeri con uso
     frequente nella wordlist.
 -o  File di output.
 -w  Wordlist > deve contenere informazioni
     relative al bersaglio.
 -y  Abilita la combinazione di date nella
     wordlist.
 -z  Abilita la conversione di parole in lettere
     maiuscole e minuscole.\n"""

def main():
    if exist('-h'):
        sys.exit(help())
    if not (exist('-w') or exist('-o')):
        sys.exit(help())
    master_list = load_words(find('-w')) # List supplied by user
    data = [] # Final wordlist
    temp = [] # Temporary wordlist
    if exist('-z'):
        master_list = gen_case(master_list)
        data = master_list
    if exist('-c'):
        temp = gen_word_combo(master_list)
        data = list(set(temp+data))
    if exist('-n'):
        temp = gen_numbers(master_list)
        data = list(set(temp+data))
    if exist('-y'):
        temp = gen_year(master_list)
        data = list(set(temp+data))
    if exist('-d'):
        try:
            custom_values = find('-d').split(',')
        except (AttributeError):
            sys.exit("[%s] Nessun valore. Mi prendi per il culo?"%(error))
        temp = gen_custom(master_list, custom_values)
        data = list(set(temp+data))
    if exist('-e'):
        data = wpa_validation_check(data)
    write_file(find('-o'), data)
    sys.exit("[%s] Parole Generate: %d"%(sys_proc,len(data)))

def merge_list(temp_list=[], final_list=[]):
    for word in temp_list:
        if word not in final_list:
            final_list.append(word)

def load_words(path_to_file):
    data = []
    try:
        handle = open(path_to_file, 'r')
        temp_list = handle.readlines()
        handle.close()
    except(BaseException):
        sys.exit("[%s] Errore nella lettura della wordlist."%(error))
    for word in temp_list:
        word = word.strip()
        if word != '':
            data.append(word)
    return data

def write_file(path_to_file, data=[]):
    try:
        handle = open(path_to_file, 'wb+')
        for word in data:
            handle.write(word+'\n')
        handle.close()
    except(BaseException):
        sys.exit("[%s] Errore nella scrittura della wordlist."%(error))

def gen_case(words=[]):
    custom_list = []
    for x in words:
        custom_list.append(x.lower())
        custom_list.append(x.capitalize())
        custom_list.append(x.upper())
    return list(set(custom_list))

def gen_numbers(words=[]):
    word_list = []
    if len(words) <= 0:
        return word_list
    num_list = ['0', '00','01', '012', '0123', '01234', '012345', '0123456', '01234567', '012345678', '0123456789',
    '1', '12', '123', '1234','12345', '123456','1234567','12345678','123456789', '1234567890', '9876543210',
    '987654321', '87654321', '7654321', '654321', '54321', '4321', '321', '21']
    for word in words:
        for num in num_list:
            word_list.append((word+num))
            word_list.append((num+word))
    return word_list

def gen_year(words=[]):
    word_list = []
    if len(words) <= 0:
        return word_list
    # Double digit dates
    start = 1
    while(start <= 99):
        for word in words:
            word_list.append(word + str("%02d") % (start))
            word_list.append(str("%02d") % start + word)
        start += 1
    # Four digit dates
    start = 1900
    while (start <= 2020):
        for word in words:
            word_list.append(word+str(start))
            word_list.append(str(start)+word)
        start += 1
    return word_list

def gen_word_combo(words=[]):
    word_list = []
    if len(words) <= 1:
        return word_list
    for word in words:
        for second_word in words:
            if word != second_word:
                word_list.append(second_word+word)
    return word_list

def gen_custom(words=[], data=[]):
    word_list = []
    if (len(words) <= 0 or len(data) <= 0):
        return word_list
    for item in data:
        for word in words:
            word_list.append(item+word)
            word_list.append(word+item)
    return word_list

def wpa_validation_check(words=[]):
    custom_list =  list(set(words))
    custom_list = [x for x in custom_list if not (len(x) < 8 or len(x) > 63)]
    return custom_list

def find(flag):
    try:
        a = sys.argv[sys.argv.index(flag)+1]
    except (IndexError, ValueError):
        return None
    else:
        return a

def exist(flag):
    if flag in sys.argv[1:]:
        return True
    else:
        return False

if __name__ == '__main__':
    main()
