#!/usr/bin/env python

import sys


# keyed by package-name, contains the list of package dependencies
pn = {}

# keyed by package-name, contains the list of dependent packages
rev_pn = {}


def parse_pn_depends():
	try:
		fh = open('pn-depends.dot')
	except:
		print 'File pn-depends.dot not found'
		print 'Generate the file with bitbake -g <recipe>'
		sys.exit()	

	try:
		raw_lines = fh.read().splitlines()
	finally:
		fh.close()

	for line in raw_lines:
		line = line.rstrip()
		fields = line.split(' ')

		if (len(fields) == 3 and fields[1] == '->'):
			name = fields[0][1:-1]
			depend = fields[2][1:-1]

			if not pn.has_key(name):
				pn[name] = []

			pn[name].append(depend)


def build_reverse_dependencies():
	for key in pn:
		for name in pn[key]:
			if not rev_pn.has_key(name):
				rev_pn[name] = []

			rev_pn[name].append(key)


def list_packages():
	print 'All Packages'

	for key in sorted(pn):
		print key

	print '\n',


def list_deps(package):
	if pn.has_key(package):
		print '\nPackage [', package, '] depends on'
		for dep in pn[package]:
			print '\t', dep

	elif rev_pn.has_key(package):
		print 'Package [', package, '] has no dependencies'

	else:
		print 'Package [', package, '] not found'

	print '\n',
	
	
def list_reverse_deps(package):
	if rev_pn.has_key(package):
		print '\nPackage [', package, '] is needed by'
		for needs in rev_pn[package]:
			print '\t', needs
	
	elif pn.has_key(package):
		print 'No package depends on [', package, ']'
	
	else:
		print 'Package [', package, '] not found'

	print '\n',



def usage():
	print '\nUsage: %s [package-name | -h]' % (sys.argv[0])
	print 'The program uses the pn-depends.dot file for its raw data.'
	print 'Generate a pn-depends.dot file by running bitbake -g <some-recipe>.\n'
	print 'Run with no arguments to get a list all packages <some-recipe> depends on.'
	print 'Run with a package-name to get a list of dependencies and dependent packages'
	print 'for an individual package.'
	print '-h or (--help) prints this help message'
	print '\n',


if __name__ == '__main__':

	parse_pn_depends()
	build_reverse_dependencies()

	if len(sys.argv) > 1:
		if sys.argv[1] == '-h' or sys.argv[1] == '--help':
			usage()
		else:
			list_deps(sys.argv[1])
			list_reverse_deps(sys.argv[1])

	else:
		list_packages()

