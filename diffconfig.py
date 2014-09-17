#!/usr/bin/env python

import sys, getopt

def read_config(config_file):
    config = {}
 
    try:
        fh = open(config_file)
    except:
        print 'Error opening ' . config_file
        sys.exit()

    try:
        lines = fh.read().splitlines()
    finally:
        fh.close()

    for line in lines:
        line  = line.rstrip()

        if line.endswith('=y'):
            config[line[:-2]] = 'y'
        elif line.endswith('=m'):
            config[line[:-2]] = 'm'
        elif line.endswith(' is not set'):
            config[line[:-11]] = 'n'
        

    return config

def a_and_b(a, b, state):
    result_list = []

    for entry in sorted(a):
        if a[entry] == state:
            if b.has_key(entry):
                if b[entry] == state:
                    result_list.append(entry)

    return result_list

def a_not_b(a, b, state):
    result_dict = {} 

    for entry in sorted(a):
        if a[entry] == state:
            if b.has_key(entry):
                if b[entry] != state:
                    result_dict[entry] = b[entry]
            else:
                result_dict[entry] = '?'

    return result_dict


def usage():
    print '\nUsage: %s <first-kernel-config> <second-kernel-config>\n' % (sys.argv[0])
    print 'Display diffs between two Linux kernel configs in an alternative format then `diff`'
    print 'Options:'
    print '-v\tShow entries that match in both configs. Default behavior shows only diffs.'
    print '-h\tShow this help message\n'


if __name__ == '__main__':

    verbose = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hv')
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt == 'h':
            usage()
            sys.exit(0)

        if opt == '-v':
            verbose = True 


    if len(args) < 2:
        usage()
        sys.exit(1)

    a_config = args[0] 
    b_config = args[1] 

    a = read_config(a_config)
    b = read_config(b_config)

    print a_config, 'has', len(a), 'entries'
    print b_config, 'has', len(b), 'entries'
     
    if verbose: 
        result_list = a_and_b(a, b, 'y')
        print '\n=y both configs', len(result_list)
        print '======================================'
        for entry in result_list:
            print 'y y', entry
        print '======================================'

        result_list = a_and_b(a, b, 'm')
        print '\n=m both configs', len(result_list)
        print '======================================'
        for entry in result_list:
            print 'm m', entry
        print '======================================'
 
        result_list = a_and_b(a, b, 'n')
        print '\nNot set in both configs', len(result_list)
        print '======================================'
        for entry in result_list:
            print 'n n', entry
        print '======================================'
 
    # just the diffs

    result_dict = a_not_b(a, b, 'y')
    print '\n=y in', a_config, 'and not in', b_config, len(result_dict)
    print '======================================'
    for key in sorted(result_dict.keys()):
        print 'y', result_dict[key], key 
    print '======================================'
 
    result_dict = a_not_b(b, a, 'y')
    print '\n=y in', b_config, 'and not in', a_config, len(result_dict)
    print '======================================'
    for key in sorted(result_dict.keys()):
        print result_dict[key], 'y', key 
    print '======================================'
 
     
