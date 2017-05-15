import argparse
import sys

parser = argparse.ArgumentParser()

#  Define arguments to be taken by the program.
parser.add_argument("--url",
                    required=True,
                    help="Sets the URL to request.")
parser.add_argument("--method",
                    choices=['POST','GET','PUT','DELETE', 'HEAD', 'OPTIONS'],
                    default='GET',
                    type=str.upper,
                    help="Sets the HTTP method to use. Default is GET")
parser.add_argument("--headers",
                    default="$arg User-Agent: Mozilla/5.0 (Windows"           \
                    " NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",  \
                    help="Headers can be passed in the following format:"     \
                    "'$arg headerType : headerValue $arg headerType"          \
                    " : headerValue2'. \n\nSingle header"                     \
                    " request example:\n\n--headers '$arg Accept: */*' "      \
                    "\n\nMultiple headers request example:\n\n --headers '$"  \
                    "header Accept: */* $arg Accept-Language: ro-RO,ro;"      \
                    "q=0.6,en-GB;q=0.4,en,q=0.2'.")
parser.add_argument("--payload",
                    default=':',
                    help="Payload can be passed in the following format:"     \
                    " '$arg element1:value1'. Example: --payload '$arg user:" \
                    "admin $arg password:${brutus}'.")
parser.add_argument("--type", choices=['standard','dictionary'],
                    default='standard',
                    help="This determines which kind of attack you are making"\
                    ". You can choose 'standard' for a straight forward "     \
                    "'dictionary' attack  or choose 'dictionary' for a "      \
                    "dictionary attack")
parser.add_argument("--rules", default="$arg charset : ABCDEFGHIJKLMNOPQRST"  \
                    "UVWXYZabcdefghijklmnopqrstuvwxyz123456789 $arg minimum_" \
                    "length : 1 $arg maximum_length : 5",
                    help="The --rules option defines three options for"       \
                    " the STANDARD brute force: the charset to use, the"      \
                    " minimum and maximum length of the string you are "      \
                    "creating. You can set any of these rules like: "         \
                    "--rules '$arg charset : abc $arg minimum_length : 1 "    \
                    "$arg maximum_length : 5'.")
parser.add_argument("--log",
                    choices=['minimum', 'info','debug'],
                    default='info',
                    help="Sets the log level. The choices are 'minimum', "    \
                    "'info' and 'debug'. 'minimum' logs the ${brutus} "       \
                    "changes, 'info' logs the ${brutus} changes, the response"\
                    " status and the response headers, while the 'debug' "    \
                    "logs all the information i.e. request method, headers, " \
                    "payload and the response code, headers and body.")
parser.add_argument("--timeout",
                    default='5',
                    help="Sets the request timeout.")
parser.add_argument("--allow_redirects",
                    default='False',
                    help="Chooses if redirects should be made automatically." \
                    " Options are <true> or <false>.")
parser.add_argument("--end",
                    help="Sets the rule for ending the brute force. "         \
                    "This can happen if a substring is found IN (or NOT found"\
                    " IN) the response headers, body or status code. Examples"\
                    " of usage: (1) \"--end 'this text IN headers'\" ends "   \
                    "when 'this text' is found in the response headers; (2) " \
                    "\"--end '404 NOT IN status'\" ends when 404 is not found"\
                    " in the response status code.",
                    default='1==2')
parser.add_argument("--source",
                    help="Sets the path to the file you want to use"          \
                    " for the dictionary attack.", default="dictionary.txt")

args = parser.parse_args()

#  Process arguments and store them in variables.
url = args.url
#  Make sure that the URL works no matter under which form it is written.
if url.startswith( 'http://www.' ):
    url = url.replace( 'http://www.', 'http://' )
elif url.startswith( 'https://www.' ):
    url = url.replace( 'https://www.', 'https://')
#  If the url is written without specifying any protocol, then use http
elif url.startswith( 'www.' ):
    url = url.replace( 'www.', 'http://' )
elif not url.startswith( 'http' ):
    url = 'http://' + url
method = args.method
headers = args.headers
payload = args.payload
rules = { 'charset' : 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1' \
                      '23456789',
          'minimum_length' : 1,
          'maximum_length' : 5}
for record in args.rules.split('$arg')[1:]:
    if record.split(':', 1)[0].strip() not in ['charset',
                                               'minimum_length',
                                               'maximum_length']:
        sys.exit('\n\n=== ERROR=== \n\nInvalid rules.\n\n')
    rules[record.split(':', 1)[0].strip()] = record.split(':', 1)[1].strip()

log_level = args.log
timeout = int(args.timeout)
if args.allow_redirects.lower() == 'true':
    allow_redirects = True
elif args.allow_redirects.lower() == 'false':
    allow_redirects = False

#  Split the --end expression in 4 parts in order to analyze it.
if args.end != '1==2':  #  i.e. if args.end is set.
    end_temp = args.end.rsplit(None, 3)
    #  Create a variable for adjusting the end_temp list indexing
    #   in case the length is only of 3 words
    adjust = 0
    if len(end_temp) < 4:
        adjust = 1
    #  Find the last word in the 'end' expression.
    if end_temp[ 3 - adjust ].lower() == 'headers':
        end = 'str(r.headers)'
    elif end_temp[ 3 - adjust ].lower() == 'body':
        end = 'r.text'
    elif end_temp[ 3 - adjust ].lower() == 'status':
        end = 'str(r.status_code)'
    else:
        print '\n\nERROR\n\nUnidentified element: "%s". Please make your '    \
              'condition based on either "headers", "body" or "status". '     \
              'Use --help for more information.' % end_temp[ 3 - adjust ]
        sys.exit('The program is now ended.')
    #  Look for the locator 'in' or 'not in' which should
    #   be placed just before the end[ 3 - adjust ].
    if end_temp[ 2 - adjust ].lower() == 'in':
        #  If the end_temp list only consists of 3 words:
        if adjust == 1:
            end = "'%s' in " % end_temp[0].replace("'", "\\'") + end
        #  Else if the end_temp list consists of 4 parts:
        else:
            #  If the second part in the end_temp is the word 'not':
            if end_temp[1].lower() == 'not':
                end = "'%s' not in " % end_temp[0].replace("'", "\\'") + end
            else:
                #  If the second part in the end_temp is not the word 'not',
                #   then end_temp[0] = end_temp[0] + end_temp[1]
                end = "'%s' in " % ' '.join(end_temp[0:2]).replace("'", "\\'") + end
    else:
        sys.exit('Unrecognized end rule. Use --help for more info on how'     \
                 ' to use the --end argument.')

source = args.source

#  TO DO
#  The 'brute_choice' dictionary helps to dynamically assess which
#      argument to brute force.
brute_choice = { 'url' : url , 'headers' : headers , 'payload' : payload ,
                 'brute_argument' : '' , 'initial_value' : '' }
#  Set brute_choice argument as 'url' for default
#  A default value is needed in order to deduce brute_choice['initial_value']
#   for the case in which no brutus variable is defined
brute_choice['brute_argument'] = 'url'
#  Check if the Brutus variable is defined in an argument. This will tell us if
#  the program is trying to attack or just make a single request.
#  Attack arguments example: --url 'http://localhost/${brutus}' or
#                            --payload 'username=admin&password=${brutus}'.
attack = 'no'
occurrences_count = 0
if '${brutus}' in args.url:
    brute_choice['brute_argument'] = 'url'
    occurrences_count += 1
    attack = 'yes'
elif '${brutus}' in args.headers:
    brute_choice['brute_argument'] = 'headers'
    occurrences_count += 1
    attack = 'yes'
elif '${brutus}' in args.payload:
    brute_choice['brute_argument'] = 'payload'
    occurrences_count += 1
    attack = 'yes'

brute_choice['initial_value'] = brute_choice[brute_choice['brute_argument']]
