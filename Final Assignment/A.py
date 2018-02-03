#! python
# (c) DL, UTA, 2009 - 2016
import  sys, string, time
from random import *
wordsize = 24                                        # everything is a word
numregbits = 3                                       # actually +1, msb is indirect bit
opcodesize = 5
addrsize = wordsize - (opcodesize+numregbits+1)      # num bits in address
memloadsize = 1024                                   # change this for larger programs
numregs = 2**numregbits
regmask = (numregs*2)-1                              # including indirect bit
addmask = (2**(wordsize - addrsize)) -1
nummask = (2**(wordsize))-1
opcposition = wordsize - (opcodesize + 1)            # shift value to position opcode
reg1position = opcposition - (numregbits +1)            # first register position
reg2position = reg1position - (numregbits +1)
memaddrimmedposition = reg2position                  # mem address or immediate same place as reg2
realmemsize = memloadsize * 1                        # this is memory size, should be (much) bigger than a program
#memory management regs
codeseg = numregs - 1                                # last reg is a code segment pointer
dataseg = numregs - 2                                # next to last reg is a data segment pointer
#ints and traps
trapreglink = numregs - 3                            # store return value here
trapval     = numregs - 4                            # pass which trap/int
mem = [0] * realmemsize                              # this is memory, init to 0
reg = [0] * numregs                                  # registers
clock = 1                                            # clock starts ticking
ic = 0                                               # instruction count
numcoderefs = 0                                      # number of times instructions read
numdatarefs = 0                                      # number of times data read
starttime = time.time()
curtime = starttime
#hit_count=0
#global compulsarymiss
compulsarymiss=0
#global capacitymiss
capacitymiss=0
#global valid
valid=[0]*4
#global arr
#global block_size
block_size=2
number_of_rows=4
set_rows=2
arr = [[-1 for x in range(block_size)] for y in range(number_of_rows)]
arr1 = [[-1 for x in range(block_size)] for y in range(set_rows)]
arr2 = [[-1 for x in range(block_size)] for y in range(set_rows)]
miss_count=0
hit_count=0
capacitymiss=0
compulsarymiss=0
miss_count=0
hit_count=0
compulsarymiss=0
capacitymiss=0
count=0
the_choice=None




def simulateSetAssociativeMap(address,memval,address2,memval2):
    print 'Set'
    print 'address',address,'memval1',memval
    global count
    count+=1
    print count
    #print 'address2',address2
    #print 'memval2',memval2
    way=2
    global miss_count
    global arr1
    global arr2
    global arr
    global hit_count

    global compulsarymiss

    global capacitymiss

    for x in range(set_rows):
        for y in range(block_size):
            if arr1[x][y]==memval or arr2[x][y]==memval:
                hit_count+=1
                flag=True
                print 'HIT'
                print flag
                print 'array1',arr1
                print 'array2',arr2
                return
    offset = address % block_size
    which_set = address % way #which word it will go to
    row_in_set= address % set_rows
    #print 'offset',offset
    #print 'row',row_in_set
    print 'set',which_set
    #print 'valid',valid
    flag=False
    #if which_set==0:
    #    if valid1[0] == 0 and not flag:
    if not flag:
            print 'inside if'
            #valid[int(row)]=1
            #print 'valid',valid
            compulsarymiss+=1
            #add memval to array or table
            for x in range(set_rows):
                for y in range(block_size):
                    if which_set==0:
                        if arr1[x][y]==0 and y%2==0 and arr1[x][y+1]==0 :
                            arr1[x][y]=memval
                            arr1[x][y+1]=memval2
                            miss_count+=1
                            print 'MISS'
                            print 'array1',arr1
                            print 'array2',arr2
                            return
                    if which_set==1:
                        if arr2[x][y]==0 and y % 2==0 and arr2[x][y+1]==0:
                            arr2[x][y]=memval
                            arr2[x][y+1]=memval2
                            miss_count+=1
                            print 'MISS'
                            print 'array1',arr1
                            print 'array2',arr2
                            return
    notempty=True

    if notempty:
            print 'inside not empty'
            #if arr[row][offset]==memval or arr[row][offset]== memval2 or arr[row][offset+1]==memval2 or arr[row][range(offset+1)]== memval:
            #check if the memval is already present in row
            #print 'update hit count'
            #hit_count+=1

            #replace the memval in array
            print 'replace the value in array'
            capacitymiss+=1
            miss_count+=1
            #valid[int(row)]=1
            row=randint(0,1)
            print 'row chosen',row
            if which_set==0:
                #if arr1[row][offset]
                    arr1[row][0]=memval
                    arr1[row][1]=memval2
                    print 'array1',arr1
                    print 'array2',arr2
                    return

            if which_set==1:
                #if arr2[x][y]==0 and arr2[x][y+1]==0:
                    arr2[row][0]=memval
                    arr2[row][1]=memval2
                    print 'array1',arr1
                    print 'array2',arr2
                    return

def simulateDirectMap(address,memval,address2,memval2):
    print 'Direct'
    print 'address',address
    print 'memval1',memval
    #print 'address2',address2
    #print 'memval2',memval2
    global miss_count
    #miss_count=0
    global hit_count
    #hit_count=0
    global compulsarymiss
    global capacitymiss
    for x in range(number_of_rows):
        for y in range(block_size):
            if arr[x][y]==memval:
                flag=True
                print 'HIT'
                hit_count+=1
                print flag
                return
    offset = address % block_size
    row=address%number_of_rows #which word it will go to
    print 'offset',offset
    print 'row',row
    print 'valid',valid
    flag=False

    if valid[int(row)] == 0 and not flag:
        print 'inside if'
        valid[int(row)]=1
        print 'valid',valid
        miss_count+=1
        print 'MISS'
        compulsarymiss+=1
        #add memval to array or table
        if offset == 0:
            arr[row][offset]=memval
            arr[row][offset+1]=memval2

    else:
        print 'inside else'
        #if arr[row][offset]==memval or arr[row][offset]== memval2 or arr[row][offset+1]==memval2 or arr[row][range(offset+1)]== memval:
        #check if the memval is already present in row
        #print 'update hit count'
        #hit_count+=1

        #replace the memval in array
        print 'replace the value in array'
        capacitymiss+=1
        miss_count+=1
        valid[int(row)]=1
        arr[row][0]=memval
        arr[row][1]=memval2
    print arr



def startexechere ( p ):
    # start execution at this address
    reg[ codeseg ] = p
def loadmem():                                       # get binary load image
  curaddr = 0
  for line in open("a.out", 'r').readlines():
    token = string.split( string.lower( line ))      # first token on each line is mem word, ignore rest
    if ( token[ 0 ] == 'go' ):
        startexechere(  int( token[ 1 ] ) )
    else:
        mem[ curaddr ] = int( token[ 0 ], 0 )
        curaddr = curaddr = curaddr + 1
def getcodemem ( a ):
    # get code memory at this address
    global numcoderefs
    numcoderefs+=1
    memval = mem[ a + reg[ codeseg ] ]
    b=a+1
    memval2 = mem[b + reg[ codeseg ] ]
    simulateDirectMap(a,memval,b,memval2)

    #simulateSetAssociativeMap(a,memval,b,memval2)
    return ( memval )
def getdatamem ( a ):
    global numdatarefs
    numdatarefs+=1
    # get code memory at this address
    memval = mem[ a + reg[ dataseg ] ]
    b=a+1
    memval2 = mem[b + reg[ codeseg ] ]
    #simulateSetAssociativeMap(a,memval,b,memval2)
    simulateDirectMap(a,memval,b,memval2)
    return ( memval )
def getregval ( r ):
    # get reg or indirect value
    if ( (r & (1<<numregbits)) == 0 ):               # not indirect
       rval = reg[ r ]
    else:
       rval = getdatamem( reg[ r - numregs ] )       # indirect data with mem address
    return ( rval )
def checkres( v1, v2, res):
    v1sign = ( v1 >> (wordsize - 1) ) & 1
    v2sign = ( v2 >> (wordsize - 1) ) & 1
    ressign = ( res >> (wordsize - 1) ) & 1
    if ( ( v1sign ) & ( v2sign ) & ( not ressign ) ):
      return ( 1 )
    elif ( ( not v1sign ) & ( not v2sign ) & ( ressign ) ):
      return ( 1 )
    else:
      return( 0 )
def dumpstate ( d ):
    if ( d == 1 ):
        print reg
    elif ( d == 2 ):
        print mem
    elif ( d == 3 ):
        print 'compulsaryMisses',compulsarymiss,'capacityMisses',capacitymiss,'Misses',miss_count,'HITS',hit_count,'clock=', clock, 'IC=', ic, 'Coderefs=', numcoderefs,'Datarefs=', numdatarefs, 'Start Time=', starttime, 'Currently=', time.time()

def trap ( t ):
    # unusual cases
    # trap 0 illegal instruction
    # trap 1 arithmetic overflow
    # trap 2 sys call
    # trap 3+ user
    rl = trapreglink                            # store return value here
    rv = trapval
    if ( ( t == 0 ) | ( t == 1 ) ):
       dumpstate( 1 )
       dumpstate( 2 )
       dumpstate( 3 )
    elif ( t == 2 ):                          # sys call, reg trapval has a parameter
       what = reg[ trapval ]
       if ( what == 1 ):
           a = a        #elapsed time
    return ( -1, -1 )
    return ( rv, rl )
# opcode type (1 reg, 2 reg, reg+addr, immed), mnemonic
opcodes = { 1: (2, 'add'), 2: ( 2, 'sub'),
            3: (1, 'dec'), 4: ( 1, 'inc' ),
            7: (3, 'ld'),  8: (3, 'st'), 9: (3, 'ldi'),
           12: (3, 'bnz'), 13: (3, 'brl'),
           14: (1, 'ret'),
           16: (3, 'int') }
startexechere( 0 )                                  # start execution here if no "go"
loadmem()                                           # load binary executable
ip = 0
def process(Input):
    global the_choice
    the_choice=Input
    print the_choice                                    # start execution at codeseg location 0
# while instruction is not halt
def choose():
    Input=raw_input("Input Number(1)Direct or (2)Set")
    process(Input)
    print Input
choose()
while( 1 ):
           ir = getcodemem( ip )                            # - fetch
           ip = ip + 1
           opcode = ir >> opcposition                       # - decode
           reg1   = (ir >> reg1position) & regmask
           reg2   = (ir >> reg2position) & regmask
           addr   = (ir) & addmask
           ic = ic + 1
                                                            # - operand fetch
           if not (opcodes.has_key( opcode )):
              tval, treg = trap(0)
              if (tval == -1):                              # illegal instruction
                 break
           memdata = 0                                      #     contents of memory for loads
           if opcodes[ opcode ] [0] == 1:                   #     dec, inc, ret type
              operand1 = getregval( reg1 )                  #       fetch operands
           elif opcodes[ opcode ] [0] == 2:                 #     add, sub type
              operand1 = getregval( reg1 )                  #       fetch operands
              operand2 = getregval( reg2 )
           elif opcodes[ opcode ] [0] == 3:                 #     ld, st, br type
              operand1 = getregval( reg1 )                  #       fetch operands
              operand2 = addr
           elif opcodes[ opcode ] [0] == 0:                 #     ? type
              break
           if (opcode == 7):                                # get data memory for loads
              memdata = getdatamem( operand2 )
           # execute
           if opcode == 1:                     # add
              result = (operand1 + operand2) & nummask
              if ( checkres( operand1, operand2, result )):
                 tval, treg = trap(1)
                 if (tval == -1):                           # overflow
                    break
           elif opcode == 2:                   # sub
              result = (operand1 - operand2) & nummask
              if ( checkres( operand1, operand2, result )):
                 tval, treg = trap(1)
                 if (tval == -1):                           # overflow
                    break
           elif opcode == 3:                   # dec
              result = operand1 - 1
           elif opcode == 4:                   # inc
              result = operand1 + 1
           elif opcode == 7:                   # load
              result = memdata
           elif opcode == 9:                   # load immediate
              result = operand2
           elif opcode == 12:                  # conditional branch
              result = operand1
              if result <> 0:
                 ip = operand2
           elif opcode == 13:                  # branch and link
              result = ip
              ip = operand2
           elif opcode == 14:                   # return
              ip = operand1
           elif opcode == 16:                   # interrupt/sys call
              result = ip
              tval, treg = trap(reg1)
              if (tval == -1):
                break
              reg1 = treg
              ip = operand2
           # write back
           if ( (opcode == 1) | (opcode == 2 ) |
                 (opcode == 3) | (opcode == 4 ) ):     # arithmetic
                reg[ reg1 ] = result
           elif ( (opcode == 7) | (opcode == 9 )):     # loads
                reg[ reg1 ] = result
           elif (opcode == 13):                        # store return address
                reg[ reg1 ] = result
           elif (opcode == 16):                        # store return address
                reg[ reg1 ] = result
           # end of instruction loop
        # end of execution
