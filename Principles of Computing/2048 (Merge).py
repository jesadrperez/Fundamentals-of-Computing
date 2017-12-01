"""
Merge function for 2048 game.
"""
#http://www.codeskulptor.org/#user42_qilOI7Houi_7.py


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    new_line = []
    for num in line:
        if num > 0:
            new_line.append(num)
    new_line = new_line+[0]*(len(line)-len(new_line))
    
    line = new_line[:]
    new_line = []
    
    num_one = None
    num_two = None
    for index in range(0,len(line)):
        if (num_one is None) and (index < len(line)-1):
            num_one = line[index]        
            continue
        if (num_one is None) and (index == len(line)-1):
            new_line.append(line[index])
            continue        
        if num_two is None:
            num_two = line[index]        
        if (num_one == num_two) and (num_one + num_two > 0):
            new_line.append(num_one+num_two)        
            num_one = None
            num_two = None        
        else:
            new_line.append(num_one)
            if index == len(line)-1:
                new_line.append(num_two)
                continue                
            num_one = num_two
            num_two = None
    new_line = new_line+[0]*(len(line)-len(new_line))
    return new_line