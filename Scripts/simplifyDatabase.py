# !/user/local/bin/python2.7
# -*- coding: utf-8 -*-

import os, sys, csv
from fixtures import *

UPPERCASE = {
    'a': 'A', 'à': 'À', 'á': 'Á', 'ả': 'Ả', 'ã': 'Ã', 'ạ': 'Ạ',
    'ă': 'Ă', 'ằ': 'Ằ', 'ắ': 'Ắ', 'ẳ': 'Ẳ', 'ẵ': 'Ẵ', 'ặ': 'Ặ',
    'â': 'Â', 'ầ': 'Ầ', 'ấ': 'Ấ', 'ẩ': 'Ẩ', 'ẫ': 'Ẫ', 'ậ': 'Ậ',
    'e': 'E', 'è': 'È', 'é': 'É', 'ẻ': 'Ẻ', 'ẽ': 'Ẽ', 'ẹ': 'Ẹ',
    'ê': 'Ê', 'ề': 'Ề', 'ế': 'Ế', 'ể': 'Ể', 'ễ': 'Ễ', 'ệ': 'Ệ',
    'i': 'I', 'ì': 'Ì', 'í': 'Í', 'ỉ': 'Ỉ', 'ĩ': 'Ĩ', 'ị': 'Ị',
    'o': 'O', 'ò': 'Ò', 'ó': 'Ó', 'ỏ': 'Ỏ', 'õ': 'Õ', 'ọ': 'Ọ',
    'ô': 'Ô', 'ồ': 'Ồ', 'ố': 'Ố', 'ổ': 'Ổ', 'ỗ': 'Ỗ', 'ộ': 'Ộ',
    'ơ': 'Ơ', 'ờ': 'Ờ', 'ớ': 'Ớ', 'ở': 'Ở', 'ỡ': 'Ỡ', 'ợ': 'Ợ',
    'u': 'U', 'ù': 'Ù', 'ú': 'Ú', 'ủ': 'Ủ', 'ũ': 'Ũ', 'ụ': 'Ụ',
    'ư': 'Ư', 'ừ': 'Ừ', 'ứ': 'Ứ', 'ử': 'Ử', 'ữ': 'Ữ', 'ự': 'Ự',
    'y': 'Y', 'ỳ': 'Ỳ', 'ý': 'Ý', 'ỷ': 'Ỷ', 'ỹ': 'Ỹ', 'ỵ': 'Ỵ',
    'đ': 'Đ'
}

LOWERCASE = {
    'A': 'a', 'À': 'à', 'Á': 'á', 'Ả': 'ả', 'Ã': 'ã', 'Ạ': 'ạ',
    'Ă': 'ă', 'Ằ': 'ằ', 'Ắ': 'ắ', 'Ẳ': 'ẳ', 'Ẵ': 'ẵ', 'Ặ': 'ặ',
    'Â': 'â', 'Ầ': 'ầ', 'Ấ': 'ấ', 'Ẩ': 'ẩ', 'Ẫ': 'ẫ', 'Ậ': 'ậ',
    'E': 'e', 'È': 'è', 'É': 'é', 'Ẻ': 'ẻ', 'Ẽ': 'ẽ', 'Ẹ': 'ẹ',
    'Ê': 'ê', 'Ề': 'ề', 'Ế': 'ế', 'Ể': 'ể', 'Ễ': 'ễ', 'Ệ': 'ệ',
    'I': 'i', 'Ì': 'ì', 'Í': 'í', 'Ỉ': 'ỉ', 'Ĩ': 'ĩ', 'Ị': 'ị',
    'O': 'o', 'Ò': 'ò', 'Ó': 'ó', 'Ỏ': 'ỏ', 'Õ': 'õ', 'Ọ': 'ọ',
    'Ô': 'ô', 'Ồ': 'ồ', 'Ố': 'ố', 'Ổ': 'ổ', 'Ỗ': 'ỗ', 'Ộ': 'ộ',
    'Ơ': 'ơ', 'Ờ': 'ờ', 'Ớ': 'ớ', 'Ở': 'ở', 'Ỡ': 'ỡ', 'Ợ': 'ợ',
    'U': 'u', 'Ù': 'ù', 'Ú': 'ú', 'Ủ': 'ủ', 'Ũ': 'ũ', 'Ụ': 'ụ',
    'Ư': 'ư', 'Ừ': 'ừ', 'Ứ': 'ứ', 'Ử': 'ử', 'Ữ': 'ữ', 'Ự': 'ự',
    'Y': 'y', 'Ỳ': 'ỳ', 'Ý': 'ý', 'Ỷ': 'ỷ', 'Ỹ': 'ỹ', 'Ỵ': 'ỵ',
    'Đ': 'đ', 'Đ': 'đ'
}


SCHOOL_YEAR = {
    'Năm thứ nhất': 1, 'Năm thứ hai': 2, 'Khác': 3
}

def lowercase(my_string):
    '''
        Usage: rename(my_string)
        This function transforms a Vietnamese string into its decapitalized form, "TRưƠnG" to "trương"
        Params(1):
            my_string: The string to be transformed.
    '''
    my_new_string = ''
    current = ''
    for index in xrange(len(my_string)):
        # Only transform letters in the REMOVE_ACCENT dictionary
        if current in LOWERCASE:
            my_new_string += LOWERCASE[current]
            current = ''

        if current in UPPERCASE:
            my_new_string += current
            current = ''

        # All ASCII letters should be conserved
        if ord(my_string[index]) <= 122 and ord(my_string[index]) >= 65:
            my_new_string += current + my_string[index].lower()
            current = ''

        else:
            current += my_string[index]
    if current in LOWERCASE:
        my_new_string += LOWERCASE[current]
    if current in UPPERCASE:
        my_new_string += current    
    return my_new_string

def titlestyle(my_string):
    my_new_string = ''
    current = ''
    firstletter = True
    for index in xrange(len(my_string)):
        # Only transform letters in the REMOVE_ACCENT dictionary
        if current in LOWERCASE:
            if firstletter:
                my_new_string += current
            else:
                my_new_string += LOWERCASE[current]
            firstletter = False
            current = ''

        elif current in UPPERCASE:
            if firstletter:
                my_new_string += UPPERCASE[current]
            else:
                my_new_string += current
            firstletter = False
            current = ''

        # All ASCII letters should be conserved
        if ord(my_string[index]) <= 122 and ord(my_string[index]) >= 40:
            if firstletter:
                my_new_string += current + my_string[index].upper()
            else:
                my_new_string += current + my_string[index].lower()
            firstletter = False
            current = ''

        elif my_string[index]==' ':
            firstletter = True
            current = ''
            my_new_string += ' ' 

        else:
            current += my_string[index]

    if current in LOWERCASE:
        if firstletter:
            my_new_string += current
        else:
            my_new_string += LOWERCASE[current]

    if current in UPPERCASE:
        if firstletter:
            my_new_string += UPPERCASE[current]
        else:
            my_new_string += current
    

    my_new_string = my_new_string.replace('  ', ' ')
    if my_new_string[-1]==' ':
        my_new_string = my_new_string[:-1]
    return my_new_string

def city(string1, string2):
    if string1 == '' or string2 == '':
        return ''
    else:
        return titlestyle(string1).replace('Huyện ', '').replace('Quận ', '').replace('Thị Xã ', '').replace(',', '-') + "; " + string2

    
def transformCSVToList(filename):
    with open(os.path.abspath(filename), 'rU') as f:
        reader = csv.reader(f)
        data = list(list(rec) for rec in csv.reader(f, delimiter = ','))
        f.close()
    return data

def simplify(record):
    new_record = [""]*12
    fullname = titlestyle(record[1]).split(" ")
    new_record[0] = str(CURRENT_SEMESTER) + SCHOOL_NB[record[8]]
    new_record[1] = " ".join(fullname[:-1])
    new_record[2] = fullname[-1]
    new_record[3] = record[2]
    new_record[4] = record[3]
    new_record[5] = SCHOOL_YEAR[record[5]] if record[5] in SCHOOL_YEAR else ""
    new_record[6] = record[7].replace(',', ';')
    new_record[7] = SCHOOL_CODE[record[8]]
    new_record[8] = city(record[10], record[11])
    new_record[9] = record[16]
    new_record[10] = CURRENT_SEMESTER
    # last column is for result
    return new_record

def simplify2(record):
    new_record = [""]*12
    fullname = titlestyle(record[0]).split(" ")
    new_record[0] = str(CURRENT_SEMESTER) + SCHOOL_NB[record[1]]
    new_record[1] = " ".join(fullname[:-1])
    new_record[2] = fullname[-1]
    new_record[3] = record[2]
    new_record[4] = record[3]
    new_record[5] = SCHOOL_YEAR[record[5]]
    new_record[6] = record[7].replace(',', ';')
    new_record[7] = SCHOOL_CODE[record[1]]
    new_record[8] = ""
    new_record[9] = ""
    new_record[10] = CURRENT_SEMESTER
    new_record[11] = ""
    return new_record

def getKeyToCompare(item):
    return item[7].ljust(10, '0') + item[2].ljust(12, '0') +  item[1].ljust(40, '0')

if __name__ == '__main__':
    data = transformCSVToList(sys.argv[1])
    newdata = []
    for i in range(1, len(data)):
        res = simplify(data[i])
        newdata.append(res)
    newdata = sorted(newdata, key=getKeyToCompare)
    myfile = open(sys.argv[1][:-4] + '_Simplified.csv', 'w' )
    for i in xrange(len(newdata)):
        myfile.write(newdata[i][0])
        for j in range(1, len(newdata[0])):
            myfile.write(',')
            myfile.write(str(newdata[i][j]))
        myfile.write('\n')
    myfile.close()
    print "Successfully finished."
