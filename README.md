 oe-deptools
=============

Tools for working with OpenEmbedded.


Installing
-------

You can get oe-deptools by saying:

    git clone git://github.com/scottellis/oe-deptools.git

Installing is just a matter of copying the python script oey.py
to the top of your OE working directory. The same location that
you run bitbake commands.

For gumstix users, this should work

    cp ~/oe-deptools/oey.py ~/overo-oe


Help
-------

    ./oey.py --help

    Usage: ./oey.py [options] [package]

    Displays OE build dependencies for a given package or recipe.
    Uses the pn-depends.dot file for its raw data.
    Generate a pn-depends.dot file by running bitbake -g <recipe>.

    Options:
    -h, --help	        Show this help message and exit
    -v, --verbose	Show error messages such as recursive dependencies
    -r, --reverse-deps  Show reverse dependencies, i.e. packages dependent on package
    -t, --tree          Tree output instead of default flat output
    -d <depth>, --depth=<depth> 
                        Maximum depth to follow dependencies, default is infinite
    -s, --show-parent-deps
                        Show child package dependencies that are already listed
                        as direct parent dependencies.

    Provide a package name from the generated pn-depends.dot file.
    Run the program without a package name to get a list of
    available package names.


Generating Data
-------

The oey.py script uses the dependency tree that bitbake generates with
the --graphviz option. 

You can generate a dependency list for a particular package or a whole image
at once. Don't worry it doesn't take long.

    ~/overo-oe$ bitbake -g omap3-console-image


Three dot files will be generated - pn-depends.dot, task-depends.dot and
package-depends.dot. 

The oey.py script uses the pn-depends.dot for its data.

Example
-------

I took a question from the gumstix dev list. The problem was iputils failing
to build because of a problem with openjade. The question was why was openjade 
being built. There was nothing about openjade in the iputils recipe.

The raw data files were generated using bitbake -g omap3-console-image.


#### Check what packages iputils requires, tree format, three levels deep

    ~/overo-oe$ ./oey.py -t -d3 iputils

    Package [ iputils ] depends on
            coreutils-native
            docbook-utils-native
                    autoconf-native
                            m4-native
                    automake-native
			    perl-native-runtime
		    docbook-dsssl-stylesheets-native
			    sgml-common-native
		    docbook-sgml-dtd-3.1-native
			    sgml-common-native
                    gnu-config-native
                    help2man-native
                    libtool-native
                    linux-libc-headers-native
                            unifdef-native
                    openjade-native
                            opensp-native
                            sgml-common
            sgmlspl-native
                    linux-libc-headers-native
                            unifdef-native
                    perl-native
                            gdbm-native
                            virtual/db-native
            virtual/arm-angstrom-linux-gnueabi-gcc
            virtual/libc

#### Check the reverse dependencies of openjade-native, flat format

    ~/overo-oe$ ./oey.py -r openjade-native

    Package [ openjade-native ] is needed by
            docbook-utils-native
            iputils
            omap3-console-image
            task-proper-tools

#### Check the reverse dependencies of openjade-native, tree format

    ~/overo-oe$ ./oey.py -t -r openjade-native

    Package [ openjade-native ] is needed by
            docbook-utils-native
                    iputils
                            task-proper-tools
                                    omap3-console-image


Notes
-------

The script is a quick hack, but occasionally useful.

My big win with it was eliminating X completely from console builds, 
something that had nagged me for awhile. And not just deployment elimination, 
but no more X compiles at all during the build. I can now build a minimal
console image from a clean OETMP in about 30 minutes, down from around one
hour. 

There are a plenty of things you could add to improve this script. 
Wildcard matches would be a nice start.


