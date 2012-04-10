# pchGenerator

import sys
import subprocess

from gcc_facade import GCCFacade
from headers_dag import HeaderNode, HeadersDag
from process_argv import processArgv
from recursive_filter import RecursiveFilter
from should_be_in_pch import ShouldBeInPCH
from stack import Stack
from topological_sorter import TopologicalSorter

#
# generateHeadersDag
#
def generateHeadersDag( options, compilerFacade ):
    dag = HeadersDag()

    compilationOptions = compilerFacade.processCompOptions( options.compilation_options )

    for sourceFilename in options.files:
        print( "Processing... ", sourceFilename, ", found ", len( dag.getNodes() ), " till now." )

        args = compilerFacade.name()
        args = args + " " + compilationOptions
        args = args + " " + sourceFilename

        proc = subprocess.Popen(
            args,
            shell = True,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            universal_newlines=True
        )

        stdout_output, stderr_output = proc.communicate()

        for line in stderr_output.split( "\n" ):
            if len( line ) == 0:
                continue

            depth, filename = compilerFacade.parseLine( line )
            dag.add( depth, filename )

        dag.processOneFile()

    return dag

#
# generatePCHPrologue
#
def generatePCHPrologue( outputFile, options ):
    outputFile.write( "// File generated by : " + sys.argv[0] + "\n" )
    outputFile.write( "// Compilation options: " + options.compilation_options + "\n" )
    outputFile.write( "// Project path       : *" + options.project_path + "*\n" )
    outputFile.write( "// Threshold          : " + str( options.threshold ) + "\n" )
    outputFile.write( "// Exclude pattern    : " + options.exclude + "\n" )
    outputFile.write( "// Exclude but pattern: " + options.exclude_except + "\n" )

#
# generatePCH
#
def generatePCH( rFilter, options ):
    outputFile = open( options.output, "w" )

    generatePCHPrologue( outputFile, options )

    for node in rFilter.getNodes():
        outputFile.write( "#include \"" + node.getData() + "\"\n" )

#
# runApplication
#
def runApplication():
    options = processArgv( sys.argv[1:] )

    dag = generateHeadersDag( options, GCCFacade() )

    tSorter = TopologicalSorter( dag )

    predicate = ShouldBeInPCH( options )

    rFilter = RecursiveFilter( tSorter, predicate )

    generatePCH( rFilter, options )

#
# main
#
if __name__ == "__main__":
    runApplication()
