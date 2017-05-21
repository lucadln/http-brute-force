#  very messy. to be cleaned someday

import string

source = 'categorized passwords/medium_passwords.txt'
length = []
consecutive_temp = 0
character_temp = '\t'
errors = 0
index = 0

#  Create a dictionary to count the number of passwords that have
#   certain lengths.
for num in range(1, 300):
    length.append( num )
password_length = dict.fromkeys(length, 0)

vowels     = [ 'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U', '\n' ]
consonants = [ 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p',
               'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'B', 'C', 'D',
               'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S',
               'T', 'V', 'W', 'X', 'Y', 'Z', '\n' ]
vowels_passes = 0
consonants_passes = 0
buzzwords = { 'love' : 0, 'fuck' : 0, 'password' : 0, 'sex' : 0, 'boy' : 0,
              'girl' : 0, 'bitch' : 0, 'real' : 0, 'admin' : 0, 'user' : 0 }
#  Define a list of accepted characters in the passwords
chars = list(   string.ascii_letters
              + string.digits
              + string.punctuation
              + ' '
              + '\n'   )
#  Transform that list into a dictionary and initialize with 0. This
#   will serve for counting purposes.
chars_occurences = dict.fromkeys(chars, 0)
end_char = dict.fromkeys(chars, 0)

#  Define a dictionary to count the number of
#   consecutive characters that are repeating
consecutive_chars = { 3 : 0 , 4 : 0 , 5 : 0 , 'more' : 0 }

#  Define a dictionary to find the number of passwords
#   that contain a certain type of characters
pswds_contain = { 'uppercase' :     0, 'numbers' : 0,
                  'special_chars' : 0, 'spaces' :  0 }

pswds_contain_inside = { 'uppercase' : 0, 'numbers' : 0, 'special_chars' : 0 }

f = open( 'machine_results.txt', 'a' )
with open(source) as password_list:
    for line in password_list:
        print 'Line {}'.format(index)
        index += 1
        #  Register the password length
        password_length[ len(line) ] += 1
        #  Find if buzzword is present in the password
        for key in buzzwords:
            if key in line:
                buzzwords[ key ] += 1
        #  Find if password is only formed from vowels or consonants
        if set( list(line) ).issubset( set( vowels ) ):
            vowels_passes += 1
        if set( list(line) ).issubset( set( consonants ) ):
            consonants_passes += 1
        #  Register if password contains certain group of chars
        if any( element in line for element in string.ascii_uppercase ):
            pswds_contain[ 'uppercase' ] += 1
        if any( element in line for element in string.digits ):
            pswds_contain[ 'numbers' ] += 1
        if any( element in line for element in string.punctuation ):
            pswds_contain[ 'special_chars' ] += 1
        if ( ' ' in line ):
            pswds_contain[ 'spaces' ] += 1
        #  Find and register the character in which a password ends
        try:
            end_char[ line[-2:-1] ] += 1
        except:
            errors += 1
        #  Count the number of passwords which contain
        #   numbers, special_chars or uppercases inside
        #   their body i.e. not in the first or last char
        if any( element in line[1:-2] for element in string.ascii_uppercase ):
            pswds_contain_inside[ 'uppercase' ] += 1
        if any( element in line[1:-2] for element in string.digits ):
            pswds_contain_inside[ 'numbers' ] += 1
        if any( element in line[1:-2] for element in string.punctuation ):
            pswds_contain_inside[ 'special_chars' ] += 1
        #  Iterate over the password's characters.
        for i, c in enumerate( line ):
            try:
                chars_occurences[ c ] += 1
                #  Find consecutive characters
                if character_temp == c:
                    consecutive_temp += 1
                else:
                    if consecutive_temp == 3:
                        consecutive_chars[ 3 ] += 1
                    if consecutive_temp == 4:
                        consecutive_chars[ 4 ] += 1
                    if consecutive_temp == 5:
                        consecutive_chars[ 5 ] += 1
                    if consecutive_temp > 5:
                        consecutive_chars[ 'more' ] += 1
                    consecutive_temp = 1
                    character_temp = c
            except:
                errors += 1
        #  Register record in case the consecutives are at the end of the
        #   password and the record wasn't registered in the for loop.
        if consecutive_temp == 3:
            consecutive_chars[ 3 ] += 1
        if consecutive_temp == 4:
            consecutive_chars[ 4 ] += 1
        if consecutive_temp == 5:
            consecutive_chars[ 5 ] += 1
        if consecutive_temp > 5:
            consecutive_chars[ 'more' ] += 1
        #  Reset values for the next loop
        character_temp = '\t'
        consecutive_temp = 0

#  Print the info about last characters in password list
f.write( """The number of occurences for each character at the last
index of the password is as follows: """)
f.write("\n\n")
for key in end_char:
    f.write( key + ': ' + str( end_char[ key ] ) )
    f.write( '\n' )
f.write("\n\n")
#  Print the number of passwords that are created exclusively
#   from vowels
f.write( """The number of passwords that are created exclusively from
            vowels is """ )
f.write( str( vowels_passes ) )
f.write("\n\n")
# Print the number of passwords that are created exclusively
#   from consonants
f.write( """The number of passwords that are created exclusively from
            consonants is """ )
f.write( str( consonants_passes ) )
f.write("\n\n")
#  Print the number of occurences in buzzwords
f.write( """The number of occurences of buzzwords are as follows:""" )
f.write("\n\n")
for key in buzzwords:
    f.write( key + ': ' + str ( buzzwords[ key ] ) )
    f.write( '\n' )
f.write("\n\n")
#  Print the number of passwords that contain certain
#   character groups inside them
f.write("""The number of passwords that contain certain character groups
           inside them (first and last position ignored) is as follows:""")
f.write("\n\n")
f.write( str( pswds_contain_inside ) )
f.write("\n\n")
#  Print the number of occurences of consecutive characters repeating
f.write("""The finding of consecutive characters is as follows: """)
f.write("\n\n")
f.write( str( consecutive_chars ) )
f.write("\n\n")
#  Print chars occurences
f.write("""The characters were found in the following numbers:""")
f.write("\n\n")
for c in chars_occurences:
    if chars_occurences[ c ] > 0 and c != '\n':
        f.write( c + ': ' + str( chars_occurences[ c ] ) )
        f.write('\n')
f.write("\n\n")
#  Print how many passwords contain certain character groups
f.write("""The number of passwords that contain certain character groups
           inside them is as follows:""")
f.write("\n\n")
f.write( str( pswds_contain ) )
f.write("\n\n")
#  Print length results:
f.write("""The number of passwords that have a certain length are displayed
           in the following:""")
f.write("\n\n")
f.write( str( password_length ) )
f.write("\n\n")
f.close()
