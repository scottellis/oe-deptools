## oe-deptools

A few scripts for working with Yocto/OpenEmbedded and Linux.

###  Installing

To install, clone the repo with git:

        git clone git://github.com/scottellis/oe-deptools.git

You'll get two python scripts

* oey.py
* diffconfig.py

You can copy the scripts to a standard location in your path or just
run them specifying the full path everytime (./oey.py <args>)

###  oey.py

Used to show dependencies for Yocto/OE packages.
 
#####  Help

        oey.py -h

        Usage: oey.py [options] [package]

        Displays dependencies for a given package or recipe.
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



#####  Generating Data

The oey.py script uses the dependency tree that bitbake generates with
the `--graphviz` or `-g` option. 

You can generate a dependency list for a particular package or a whole image
at once. This doesn't take long even for an image recipe.

        ~/overo/build$ bitbake -g console-image


The following files will be generated in the *build* directory.

* package-depends.dot 
* pn-buildlist
* pn-depends.dot
* task-depends.dot

The `oey.py` script uses `pn-depends.dot` for its data.

The script is hard-coded to look for the data file in the current
working directory so you should run it from the directory where
`pn-depends.dot` is located.


#####  Example

    scott@octo:~/overo/build$ oey.py openssl

    Package [ openssl ] depends on
            cryptodev-linux
                    cryptodev-linux-dev
            openssl-conf
            openssl-dev
            perl-native-runtime
            pkgconfig-native
                    autoconf-native
                            m4-native
                    automake-native
                            perl-native-runtime
                    gnu-config-native
                            perl-native-runtime
                    libtool-native
            virtual/arm-poky-linux-gnueabi-compilerlibs
            virtual/arm-poky-linux-gnueabi-gcc
            virtual/libc


    scott@octo:~/overo/build$ oey.py -r openssl

    Package [ openssl ] is needed by
            git
                    console-image
            openssh
                    packagegroup-core-ssh-openssh
            python
                    iotop
                            console-image
                    opkg-utils
            wget
                    console-image

