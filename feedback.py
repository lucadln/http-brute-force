from arguments import *

#  Define program_info function.
def program_info():
    i = 1
    print '\n=================================='
    print '========= PROGRAM INFO ==========='
    print '=================================='

    if occurrences_count != 0 and args.type == 'standard':
        print '(%d) You are starting a standard brute force attack using the' \
              ' charset "%s" for a string that has a minimum length of %s'    \
              ' and a maximum one of %s' % (i,
                                            rules['charset'],
                                            rules['minimum_length'],
                                            rules['maximum_length'])
        i = i + 1
    if occurrences_count != 0 and args.type == 'dictionary':
        print '(%d) You are starting a dictionary brute force attack using '  \
              'the file "%s".' % (i, source)
        i = i + 1

    elif occurrences_count != 0 and args.end != '1==2':
        print "(%d) The program is instructed to end when the following "     \
              "condition is met: < %s >" % (i, end)

    print '(%d) The logging level is set to %s' % ( i, log_level.upper() )
    i = i + 1

    if allow_redirects == False:
        print '(%d) Redirects are NOT being followed automatically. You can ' \
              'change this by using the --allow_redirects argument.' % i
        i = i + 1
    else:
        print '(%d) Redirects are being followed automatically. You can '     \
              'change this by using the --allow_redirects argument.' % i
        i = i + 1

    print '(%d) The request timeout is currently set to %d seconds.' % (i,
                                                                        timeout)
    i = i + 1

#  Define warning_info function.
def warning_info():
    i = 1
    printed_warning = False
    if occurrences_count == 0:
        if printed_warning == False:
            print '\n=================================='
            print '=========== WARNING =============='
            print '=================================='
            printed_warning = True
        print '(%d) The ${brutus} variable was not found. A single request '  \
               'will be done. If you want to brute force, then please define' \
               ' the ${brutus} variable in either the url, headers or '       \
               'payload.' % i
        i = i + 1
    if (args.type == 'dictionary' and source == 'dictionary.txt'):
        if printed_warning == False:
            print '\n=================================='
            print '=========== WARNING =============='
            print '=================================='
            printed_warning = True
        print "(%d) The --type is set to 'dictionary' but no source file is"  \
              " set. The default file 'dictionary.txt' will be used. To use " \
              "your own file please use the --source argument." % i
        i = i + 1
    if occurrences_count != 0 and args.end == '1==2':
        if printed_warning == False:
            print '\n=================================='
            print '=========== WARNING =============='
            print '=================================='
            printed_warning = True
        print '(%d) The program has no --end argument defined meaning that it'\
              ' won\'t know when to stop brute forcing. Please use the '      \
              '--end argument if you want to instruct your program to '       \
              'stop somewhere.' % i
        i = i + 1
