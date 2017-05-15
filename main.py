from feedback import warning_info, program_info
from arguments import occurrences_count, args, rules
from requests_definition import ( single_request,
                                  standard_attack,
                                  dictionary_attack )

warning_info()
program_info()

print '\n=================================='
print '========== REQUEST LOG ==========='
print '=================================='

if occurrences_count == 0:  #  If ${brutus} is not defined:
    single_request()
else:
    if args.type == 'standard':
        standard_attack("",
              rules['charset'],
              int(rules['minimum_length']),
              int(rules['maximum_length']))
    elif args.type == 'dictionary':
        dictionary_attack()
    #  If the program gets to this line, this means that
    #   the end condition was not met.
    if args.end != '1==2':
        print '\n============================================='
        print '\nThe brute force attack has finished but the end condition' \
              ' was not met. '
        print '\n============================================='
