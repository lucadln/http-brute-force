from arguments import log_level, method, brute_choice

#  Define functions for requests logging
def log_minimum(request, response):
    print '\nBrute forcing...\n'
    print request[brute_choice['brute_argument']]

def log_info(request, response):
    print '\nBrute forcing...\n'
    print request[brute_choice['brute_argument']]
    print 'Status code:', response.status_code
    print 'Response headers:'
    print response.headers

def log_debug(request, response):
    print 'Request << '
    print method, request['url']
    print 'Request headers: ' + request['headers']
    print 'Payload: ' + request['payload']
    print '\n'
    print 'Response << '
    print 'Status code: ' + str(response.status_code)
    print '* * * *'
    for k, v in response.headers.items():
        print k, ':', v
    print '* * *'
    print '\n'
    print response.text

#  Log dictionary for which every key corresponds to a function
log = {'minimum' : log_minimum , 'info' : log_info , 'debug' : log_debug}
