#!/usr/bin/env python
'''
OWASP ZSC | ZCR Shellcoder
https://www.owasp.org/index.php/OWASP_ZSC_Tool_Project
https://github.com/Ali-Razmjoo/OWASP-ZSC
http://api.z3r0d4y.com/
https://groups.google.com/d/forum/owasp-zsc [ owasp-zsc[at]googlegroups[dot]com ]
'''
import binascii
import random
import string
from core.compatible import version
_version = version()

def encode(f):
    var_name = ''.join(random.choice(string.ascii_lowercase+string.ascii_uppercase) for i in range(50))

    if _version is 2:
        rev_data = binascii.b2a_base64(f)[-2::-1]
        data = var_name + ' = "' + str(rev_data) +'"'
    if _version is 3:
        rev_data = binascii.b2a_base64(f.encode('utf8')).decode('utf8')[-2::-1]
        data = var_name + ' = "' + str(rev_data) +'"'

    var_data = random.choice(string.ascii_lowercase) + ''.join(random.choice(string.ascii_lowercase+string.ascii_uppercase) for i in range(50))
    func_name = ''.join(random.choice(string.ascii_lowercase+string.ascii_uppercase) for i in range(50))
    func_argv = random.choice(string.ascii_lowercase) + ''.join(random.choice(string.ascii_lowercase+string.ascii_uppercase) for i in range(50))
    var_str = random.choice(string.ascii_lowercase) + ''.join(random.choice(string.ascii_lowercase+string.ascii_uppercase) for i in range(50))
    f = '''
require "base64"
%s
def %s(%s)
    %s = Base64.decode64(%s.reverse)
    return %s
end
%s = %s;
eval(%s(%s));'''%(data, func_name, func_argv, var_str, func_argv, var_str, var_data, var_name, func_name, var_data)
    return f

def start(content):
    return str(str('=begin\n')+str(content.replace('=begin','#=begin').replace('=end','#=end'))+str('\n=end') + str(encode(content))+str('\n'))
