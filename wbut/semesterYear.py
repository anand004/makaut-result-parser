def getSemYear(year,semester):
    semYear = year
    print(semYear)
    if semester == 2 or semester == 3:
        semYear += 1
    elif semester == 4 or semester == 5:
        semYear += 2
    elif semester == 6 or semester == 7:
        semYear += 3
    elif semester == 8:
        semYear += 4
    if semester % 2 == 0:
        semYear = "MAY-JUNE EXAMINATION: 20"+str(semYear)
    else:
        semYear = "DEC-JAN EXAMINATION: 20"+str(semYear)+"-"+str(semYear+1)
    return semYear

