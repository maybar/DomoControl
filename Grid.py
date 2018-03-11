class Grid(dict):
    """
      A two-dimensional array that can be accessed by row, by column, or by cell.
 
      Create with lists of row and column names plus any valid dict() constructor args.
 
      >>> data = Grid( ['A', 'B'], [1, 2] )
 
      Row and column lists must not have any values in common.
 
      >>> data = Grid([1, 2], [2, 3])
      Traceback (most recent call last):
      ...
      ValueError: Row and column lists must not have any values in common
 
      Here is an example with data:
 
      >>> rowNames = ['A','B','C','D']
      >>> colNames = [1,'J']
      >>> rawData = [ 'cat', 3, object, 9, 4, [1], 5, 6 ]
      >>> indices = [ (row, col) for col in colNames for row in rowNames ]
      >>> data = Grid(rowNames, colNames, zip(indices, rawData))
 
 
      Data can be accessed by cell:
 
      >>> for i in indices:
      ...    print i, data[i]
      ('A', 1) cat
      ('B', 1) 3
      ('C', 1) <type 'object'>
      ('D', 1) 9
      ('A', 'J') 4
      ('B', 'J') [1]
      ('C', 'J') 5
      ('D', 'J') 6
 
      >>> data['B', 'J'] = 5
 
 
      Cell indices must contain valid row and column names:
 
      >>> data[3]
      Traceback (most recent call last):
      ...
      KeyError: 3
 
      >>> data['C', 2] = 5
      Traceback (most recent call last):
      ...
      ValueError: Invalid key or value: Grid[('C', 2)] = 5
 
 
      Data can be accessed by row or column index alone to set or retrieve
      an entire row or column:
 
      >>> print data['A']
      ['cat', 4]
 
      >>> print data[1]
      ['cat', 3, <type 'object'>, 9]
 
      >>> data['A'] = ['dog', 2]
      >>> print data['A']
      ['dog', 2]
 
 
      When setting a row or column, data must be the correct length.
 
      >>> data['A'] = ['dog']
      Traceback (most recent call last):
      ...
      ValueError: Invalid key or value: Grid['A'] = ['dog']
 
    """
 
    def __init__(self, rowNames, colNames, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.rowNames = list(rowNames)
        self.colNames = list(colNames)
 
        # Check for no shared row and col names
        if set(rowNames).intersection(colNames):
            raise ValueError('Row and column lists must not have any values in common')
 
    def __getitem__(self, key):
        if self._isCellKey(key):
            return dict.__getitem__(self, key)

        elif key in self.rowNames:
            return [ dict.__getitem__(self, (key, col)) for col in self.colNames ]

        elif key in self.colNames:
            return [ dict.__getitem__(self, (row, key)) for row in self.rowNames ]

        else:
            raise KeyError( key)
 
 
    def __setitem__(self, key, value):
        if self._isCellKey(key):
            return dict.__setitem__(self, key, value)
 
        elif key in self.rowNames and len(value) == len(self.colNames):
            for col, val in zip(self.colNames, value):
                dict.__setitem__(self, (key, col), val)
 
        elif key in self.colNames and len(value) == len(self.rowNames):
            for row, val in zip(self.rowNames, value):
                dict.__setitem__(self, (row, key), val)
 
        else:
            raise ValueError( 'Invalid key or value: Grid[%r] = %r' % (key, value))
 
 
    def _isCellKey(self, key):
        ''' Is key a valid cell index? '''
        return isinstance(key, tuple) \
            and len(key) == 2 \
            and key[0] in self.rowNames \
            and key[1] in self.colNames
            
        