# CommandBlock.py 
# Tarik Tosun
# University of Pennsylvania, September 2014
import pdb

class CommandBlock:
    def __init__(self):
        self.command_list = []
        self.triggers_list = []
        self.labels_list = []
        self.trigger = 0

    def __repr__(self):
        return self.make_table()


    def stitch(self, relativeBlock):
        ''' Stitches a RelativeBlock onto this CommandBlock. '''
        for block in relativeBlock.block_list:
            if isinstance(block,str):       # raw strings are commands.
                self.appendCommand(block)
                #pdb.set_trace()
            else: # it's a series or parallel block.
                if relativeBlock.type == 'series': # the iterator increases for series blocks.
                    self.trigger += 1
                self.stitch(block)

    def appendCommand(self, command_string):
        ''' Appends the command string to this CommandBlock, using the current trigger value. '''
        self.command_list.append( command_string )
        self.triggers_list.append( self.trigger )
        self.labels_list.append( self.trigger + 1 )

    def make_table(self):
        ''' Returns the formatted table for this commandBlock. '''
        out = ''
        for i in xrange(0,len(self.command_list)):
            if self.triggers_list[i]==0: # hack so that first one won't have a trigger.
                out += self.command_list[i] + ' {' + str(self.labels_list[i]) + '};\n'
            else:
                out += self.command_list[i] + ' (' + str(self.triggers_list[i]) + ') {' + str(self.labels_list[i]) + '};\n'
        return out

    def write(self, fname):
        ''' Writes out to file. '''
        tableString = self.make_table()
        f = open(fname, 'w')
        f.write(tableString)
        f.close()

