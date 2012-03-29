# pchGenerator

import sys
import unittest

#
# printHelp
#
def printHelp():
	print( "Usage: ", sys.argv[0] )
	print( "Author: Lukasz Czerwinski (wo3kie@gmail.com)" )

#
# parseLine
#
def parseLine( line ):
	i = 0
	length = len( line )
	
	while i < length and line[i] == '.':
		i += 1
	
	if i == 0:
		raise Exception( "Wrong file format: 'filename'" )
	
	if line[i] != ' ':
		raise Exception( "Wrong file format: '...filename'" )

	if i + 1 == length:
		raise Exception( "Wrong file format: '... '" )
	
	return ( i, line[ i + 1 : len(line) ] )
	
	
class TestParseLine(unittest.TestCase):
	def test_negative( self ):
		self.assertRaises( Exception, parseLine, "line" )
		self.assertRaises( Exception, parseLine, ". " )
		self.assertRaises( Exception, parseLine, "...line" )
		self.assertRaises( Exception, parseLine, "......." )

	def test_positive( self ):
		self.assertEqual( parseLine( ". f" ), ( 1, "f" ) )
		self.assertEqual( parseLine( ".. directory" ), ( 2, "directory" ) )
		self.assertEqual( parseLine( "... path" ), ( 3, "path" ) )

#
# runApplication
#
def runApplication():
	if len( sys.argv ) != 2:
		printHelp()
		exit( 1 )
	
	file = open( sys.argv[1], 'r' )
	
	for line in file:
		print( parseLine( line ) )

#
# main
#
if __name__ == "__main__":
	if len( sys.argv ) == 1:
		unittest.main()
	else:
		runApplication()