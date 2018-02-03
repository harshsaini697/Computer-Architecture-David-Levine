#! python
# (c) DL, UTA, 2009 - 2016
import  sys, string
wordsize = 24                                        # everything is a word
numregbits = 3                                       # actually +1, msb is indirect bit
opcodesize = 5         
memloadsize = 1024                                   # change this for larger programs
numregs = 2**numregbits
opcposition = wordsize - (opcodesize + 1)            # shift value to position opcode
reg1position = opcposition - (numregbits + 1)        # first register position
reg2position = reg1position - (numregbits + 1)
memaddrimmedposition = reg2position                  # mem address or immediate same place as reg2
startexecptr = 0;
def regval ( rstr ):                                 # help with reg or indirect addressing
    if rstr.isdigit():
       return ( int( rstr ) )
    elif rstr[0] == '*':
       return ( int ( rstr[1:] ) + (1<<numregbits) )
    else:
       return 0                                      # should not happen
mem = [0] * memloadsize                              # this is the memory load executable
# instruction mnemonic, type: (1 reg, 2 reg, reg+addr, immed, pseudoop), opcode  
opcodes = {'add': (2, 1),'sub': (2, 2),                # ie, "add" is a type 2 instruction, opcode = 1
           'dec': ( 1, 3), 'inc': ( 1, 4 ), 
           'ld': (3, 7), 'st': (3, 8), 'ldi': (3, 9),
           'bnz': (3, 12), 'brl': (3, 13),
           'ret': ( 1, 14 ),
           'int': (3, 16), 'sys': (3, 16),             # syscalls are same as interrupts
           'dw': (4, 0), 'go':(3, 0), 'end': (0, 0) }  # pseudo ops
curaddr = 0                                            # start assembling to location 0
#for line in open(sys.argv[1], 'r').readlines():       # command line
infile = open("in.asm", 'r')
# Build Symbol Table
symboltable = {}
for line in infile.readlines():           # read our asm code
   tokens = string.split( string.lower( line ))        # tokens on each line
   firsttoken = tokens[0]
   if firsttoken.isdigit():                             # if line starts with an address
       curaddr = int( tokens[0] )                      # assemble to here
       tokens = tokens[1:]
   if firsttoken == ';':                                # skip comments
      continue
   if firsttoken == 'go':                               # start execution here
      startexecptr = ( int( tokens[ 1 ] ) & ((2**wordsize)-1))  # data
      continue
   if firsttoken[0] == '.':
      symboltable[firsttoken] = curaddr
   curaddr = curaddr + 1
print symboltable 
infile.close()
infile = open("in.asm", 'r')
for line in infile.readlines():           # read our asm code
   tokens = string.split( string.lower( line ))        # tokens on each line
   firsttoken = tokens[0]
   if firsttoken.isdigit():                             # if line starts with an address
       curaddr = int( tokens[0] )                      # assemble to here
       tokens = tokens[1:]
   if firsttoken == ';':                                # skip comments
      continue
   if firsttoken == 'go':                               # start execution here
      startexecptr = ( int( tokens[ 1 ] ) & ((2**wordsize)-1))  # data
      continue
   if firsttoken[0] == '.':
      symaddr = symboltable[firsttoken]
      tokens = tokens[1:]
   memdata = 0                                             # build instruction step by step
   instype = opcodes[ tokens[0] ] [0]
   memdata = ( opcodes[ tokens[0] ] [1] ) << opcposition   # put in opcode  
   if instype == 4:                                        # dw type
      memdata = ( int( tokens[ 1 ] ) & ((2**wordsize)-1))  # data is wordsize long
   elif instype == 0:                                      # end type
      memdata = memdata 
   elif instype == 1:                                      # dec,inc type, one reg
      memdata = memdata + (regval( tokens[1] ) << reg1position)
   elif instype == 2:                                      # add, sub type, two regs
      memdata = memdata + ( regval( tokens[1] ) << reg1position ) + ( regval( tokens[2] ) << reg2position)
   elif instype == 3:                                      # ld,st type
      token2 = tokens[2]
      if token2.isdigit():
         memaddr = int( tokens[2] )
      else:
         memaddr = symboltable[ token2 ] 
      memdata = memdata + ( regval( tokens[1] ) << reg1position ) + memaddr
   mem[ curaddr ] = memdata                                # memory image at the current location
   curaddr = curaddr + 1
outfile = open("a.out", 'w')                               # done, write it out
outfile.write( 'go ' + '%d' % startexecptr )               # start execution here
outfile.write( "\n" )
for i in range(memloadsize):                               # write memory image   
   outfile.write( hex( mem[ i ] ) + "    " + '%d'%i)
   outfile.write( "\n" )
outfile.close()
