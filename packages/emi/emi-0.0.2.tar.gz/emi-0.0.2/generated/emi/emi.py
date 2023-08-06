import os
import logging
import eons as e

######## START CONTENT ########
# All builder errors
class BuildError(Exception): pass


# Exception used for miscellaneous build errors.
class OtherBuildError(BuildError): pass


# Project types can be things like "lib" for library, "bin" for binary, etc. Generally, they are any string that evaluates to a different means of building code.
class ProjectTypeNotSupported(BuildError): pass


class EMI(e.Executor):

    def __init__(this):
        super().__init__(name="eons Module Installer", descriptionStr="A package manager for eons and infrastructure technologies.")

        this.RegisterDirectory("epic")

    #Override of eons.Executor method. See that class for details
    def RegisterAllClasses(this):
        super().RegisterAllClasses()

    #Override of eons.Executor method. See that class for details
    def AddArgs(this):
        super().AddArgs()
        this.argparser.add_argument('-i', 'install', type = str, action='append', nargs='*', metavar = 'package_mine', help = 'install a package', dest = 'install')
        this.argparser.add_argument('-u','update', type = str, action='append', nargs='*', metavar = 'package_mine', help = 'update a package', dest = 'update')
        this.argparser.add_argument('-r','remove', type = str, action='append', nargs='*', metavar = 'package_mine', help = 'remove a package (aka uninstall)', dest = 'remove')


    #Override of eons.Executor method. See that class for details
    def ParseArgs(this):
        super().ParseArgs()

    #Override of eons.Executor method. See that class for details
    def UserFunction(this, **kwargs):
        super().UserFunction(**kwargs)
        this.Execute(this.args.builder, this.args.path, this.args.build_in, this.events, **this.extraArgs)

    #Install a package
    def Install(this, packageName):
        pass

    #Install a package
    def Update(this, packageName):
        pass

    #Install a package
    def Remove(this, packageName):
        pass
