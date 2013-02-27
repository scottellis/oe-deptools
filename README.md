 oe-deptools
=============

Tools for working with OpenEmbedded.


  Installing
-------

You can get oe-deptools with git:

        git clone git://github.com/scottellis/oe-deptools.git


Installing is just a matter of copying the python script oey.py
to a convenient location. 

The script is hard-coded to look for the data file in the current
working directory so I just copy it to wherever I'm running builds.


  Help
-------

        ./oey.py -h

        Usage: ./oey.py [options] [package]

        Displays OE build dependencies for a given package or recipe.
        Uses the pn-depends.dot file for its raw data.
        Generate a pn-depends.dot file by running bitbake -g <recipe>.

        Options:
        -h      Show this help message and exit
        -v      Show error messages such as recursive dependencies
        -r      Show reverse dependencies, i.e. packages dependent on package
        -f      Flat output instead of default tree output
        -d <depth>      Maximum depth to follow dependencies, default and max is 10
        -s      Show child package dependencies that are already listed
                as direct parent dependencies.

        Provide a package name from the generated pn-depends.dot file.
        Run the program without a package name to get a list of
        available package names.



  Generating Data
-------

The oey.py script uses the dependency tree that bitbake generates with
the --graphviz or -g option. 

You can generate a dependency list for a particular package or a whole image
at once. This doesn't take long even for an image recipe.

        ~/jumpnow/build$ bitbake -g jumpnow-console-image


Three dot files will be generated - pn-depends.dot, task-depends.dot and
package-depends.dot. 

The oey.py script uses the pn-depends.dot for its data.


  Example
-------

        scott@hex:~/jumpnow/build$ ./oey.py -r boost

        Package [ boost ] is needed by
                libzypp
                        zypper
                                jumpnow-console-image

        scott@hex:~/jumpnow/build$ ./oey.py boost

        Package [ boost ] depends on
                boost-date-time
                boost-dev
                boost-filesystem
                boost-graph
                boost-iostreams
                boost-native
                boost-program-options
                boost-regex
                boost-signals
                boost-system
                boost-test
                boost-thread
                virtual/arm-poky-linux-gnueabi-compilerlibs
                virtual/arm-poky-linux-gnueabi-gcc
                virtual/libc
                zlib
                        zlib-dev

