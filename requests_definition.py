from pip._vendor import requests
from arguments import *
from log_functions import *
import sys

headers = "dict(map(str.strip, item.split(':', 1)) for item in " \
          "map(str.strip, brute_choice['headers'].split('$arg')[1:]))"
data    = "dict(map(str.strip, item.split(':', 1)) for item in " \
          "map(str.strip, brute_choice['payload'].split('$arg')[1:]))"

request = { 'GET'  : requests.get  , 'POST'    : requests.post   , \
            'PUT'  : requests.put  , 'DELETE'  : requests.delete , \
            'HEAD' : requests.head , 'OPTIONS' : requests.options  }

#  Define single request function
def single_request():
    r = request[method](
        brute_choice['url'],
        headers = eval(headers),
        data = eval(data),
        allow_redirects=allow_redirects,
        timeout=timeout
        )
    r.encoding = 'utf-8'
    #  Request logging
    log['debug']( brute_choice, r )

#  Define standard brute force attack function
def standard_attack(string, charset, min_length, max_length):
    if len(string) == max_length:
        return
    for char in charset:
        try:
            temp = string + char
            #  Replace ${brutus} with temp value in the url,
            #   headers or payload.
            brute_choice[brute_choice['brute_argument']] = \
                brute_choice['initial_value'].replace( '${brutus}', temp )
            if len(temp) < min_length:
                standard_attack( temp, charset, min_length, max_length )
            else:
                r = request[method](
                    brute_choice['url'],
                    headers = eval(headers),
                    data = eval(data),
                    allow_redirects=allow_redirects,
                    timeout=timeout
                    )
                #  Request logging
                log[log_level]( brute_choice, r )
                #  If end condition is met then stop looping
                if eval(end) == True:
                    sys.exit('\n=============================================' \
                             '\n\nCondition <%s> met for ${brutus}=\'%s\'.\n'  \
                             '\n=============================================' \
                              % (args.end, temp))
                standard_attack(temp, charset, min_length, max_length)
        except Exception:
            #  TO DO
            pass

#  Define dictionary attack function
def dictionary_attack():
    with open(source) as dictionary:
        for line in dictionary:
            #  Replace ${brutus} with temp value in the url,
            #   headers or payload.
            brute_choice[brute_choice['brute_argument']] = \
                brute_choice['initial_value'].replace('${brutus}', line).strip()
            try:
                r = request[method](
                        brute_choice['url'],
                        headers = eval(headers),
                        data = eval(data),
                        allow_redirects=allow_redirects,
                        timeout=timeout)
                #  Request logging
                log[log_level]( brute_choice, r )
                #  If end condition is met then stop looping
                if eval(end) == True:
                    sys.exit('\n=============================================' \
                             '\n\nCondition <%s> met for ${brutus}=\'%s\'.\n'  \
                             '\n=============================================' \
                              % (args.end, line.strip()))
            except Exception:
                #  TO DO
                pass
