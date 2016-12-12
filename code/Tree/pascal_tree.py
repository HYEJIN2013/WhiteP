def triangle(rows):
    for rownum in range (rows):
        newValue=1
        PrintingList = [newValue]
        for iteration in range (rownum):
            newValue = newValue * ( rownum-iteration ) / ( iteration + 1 )
            PrintingList.append(int(newValue))
        print(PrintingList)
