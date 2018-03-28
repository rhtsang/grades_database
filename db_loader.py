import sys
import csv
import psycopg2
import os

studentKey = []
courseKey = []

def parser():
    for param in sys.argv[1:]:
        
        # just to make sure it's still running and not frozen
        print(param)
        
        CID_info = ["","","","","",""]
        
        INSTRUCTOR_info = ["","","","","",""]
        INSTRUCTOR_list = []
        
        SEAT_info = []
        SEAT_list = []
        
        term_spacetime = []
        spacetime = ["","","",""]
        conflicting_spacetime = []
        
        term_CIDs = []
        conflicting_CIDs = []
        
        counter = 0
        
        instructorName = ""
        
        StudentTable = []
        StudentTuple = []
    
        CourseMeetingTable = []
        CourseMeetingTuple = []
        
        CourseTable = []        
        CourseTuple = []

        StudentInMeetingTable = []
        StudentInMeetingTuple = []

        WhenWhereMeetTable = []
        WhenWhereMeetTuple = []
        
        studentKeyTuple = []
        courseKeyTuple = []

        with open(param, 'rU') as csvfile:
            openfile = csv.reader(csvfile, delimiter=',')
            for row in openfile:
                
                # http://stackoverflow.com/a/27405287
                # checks for empty line
                if not ''.join(row).strip():
                    counter += 1
                    
                    # if counter == 4, we've reached the end of a chunk of
                    # CID/INSTRUCTOR(S)/SEAT info, so make tuples before deleting
                    if (counter == 4):
                        counter = 1
                        
                        if SEAT_list:
                            # escape apostrophes in names, ex. change O'Brien to O''Brien
                            # to insert into Postgres
                            # apparently emails can have apostrophes too?
                            for student in SEAT_list:
                                index = student[2].find("'")
                                if index != -1:
                                    student[2] = student[2][:index] + "'" + student[2][index:]
                                index = student[-1].find("'")
                                if index != -1:
                                    student[-1] = student[-1][:index] + "'" + student[-1][index:]
                        
                            # make StudentTuple and StudentTable
                            for student in SEAT_list:
                                StudentTuple.append(student[1]) # SID
                                StudentTuple.append(student[2]) # surname
                                StudentTuple.append(student[3]) # prefname
                                StudentTuple.append(student[-1]) # email

                                #####key tuple####
                                studentKeyTuple = student[1]
                                ##################
                                if studentKeyTuple not in studentKey:
                                    studentKey.append(studentKeyTuple)
                                    StudentTable.append(StudentTuple[:])
                                studentKeyTuple = None
                                del StudentTuple[:]
                        
                            # make CourseMeetingTuple and CourseMeetingTable
                            for instructor in INSTRUCTOR_list:
                                CourseMeetingTuple.append(CID_info[0]) # CID
                                CourseMeetingTuple.append(CID_info[1]) # term
                                CourseMeetingTuple.append(CID_info[2]) # subj
                                CourseMeetingTuple.append(CID_info[3]) # crse
                                CourseMeetingTuple.append(CID_info[4]) # sec
                                CourseMeetingTuple.append(instructor[0]) # instructor
                                CourseMeetingTuple.append(instructor[1]) # type
                                # CourseMeetingTuple.append(instructor[2]) # days
                                # CourseMeetingTuple.append(instructor[3]) # time
                                # CourseMeetingTuple.append(instructor[4]) # building
                                # CourseMeetingTuple.append(instructor[5]) # room
                                CourseMeetingTable.append(CourseMeetingTuple[:])
                                del CourseMeetingTuple[:]
                            
                        
                            # make CourseTuple and CourseTable
                            CourseTuple.append(CID_info[2]) # subj
                            CourseTuple.append(CID_info[3]) # crse
                            CourseTuple.append(CID_info[-1]) # units
                            # if CourseTuple not in CourseTable:s
                            courseKeyTuple.append(CID_info[2])
                            courseKeyTuple.append(CID_info[3])

                            if courseKeyTuple not in courseKey:
                                courseKey.append(courseKeyTuple[:])
                                CourseTable.append(CourseTuple[:])
                            del courseKeyTuple[:]
                            del CourseTuple[:]
                        


                            # make StudentInMeetingTuple and StudentInMeetingTable
                            for instructor in INSTRUCTOR_list:
                                for student in SEAT_list:
                                    StudentInMeetingTuple.append(CID_info[0]) # CID
                                    StudentInMeetingTuple.append(CID_info[1]) # term
                                    StudentInMeetingTuple.append(instructor[0]) # instructor
                                    StudentInMeetingTuple.append(student[0]) # seat
                                    StudentInMeetingTuple.append(student[1]) # SID
                                    StudentInMeetingTuple.append(student[4]) # level
                                    StudentInMeetingTuple.append(student[5]) # units
                                    StudentInMeetingTuple.append(student[6]) # class
                                    StudentInMeetingTuple.append(student[7]) # major
                                    StudentInMeetingTuple.append(student[8]) # grade
                                    StudentInMeetingTuple.append(student[9]) # status
                                    if StudentInMeetingTuple[-2] == "F":
                                        StudentInMeetingTuple.append('0')
                                    elif StudentInMeetingTuple[-2] == "D-":
                                        StudentInMeetingTuple.append('1')
                                    elif StudentInMeetingTuple[-2] == "D":
                                        StudentInMeetingTuple.append('2')
                                    elif StudentInMeetingTuple[-2] == "D+":
                                        StudentInMeetingTuple.append('3')
                                    elif StudentInMeetingTuple[-2] == "C-":
                                        StudentInMeetingTuple.append('4')
                                    elif StudentInMeetingTuple[-2] == "C":
                                        StudentInMeetingTuple.append('5')
                                    elif StudentInMeetingTuple[-2] == "C+":
                                        StudentInMeetingTuple.append('6')
                                    elif StudentInMeetingTuple[-2] == "B-":
                                        StudentInMeetingTuple.append('7')
                                    elif StudentInMeetingTuple[-2] == "B":
                                        StudentInMeetingTuple.append('8')
                                    elif StudentInMeetingTuple[-2] == "B+":
                                        StudentInMeetingTuple.append('9')
                                    elif StudentInMeetingTuple[-2] == "A-":
                                        StudentInMeetingTuple.append('10')
                                    elif StudentInMeetingTuple[-2] == "A":
                                        StudentInMeetingTuple.append('11')
                                    elif StudentInMeetingTuple[-2] == "A+":
                                        StudentInMeetingTuple.append('12')
                                    else: # not a letter grade
                                        StudentInMeetingTuple.append(None)
                                    StudentInMeetingTuple.append(instructor[2]) # days
                                    StudentInMeetingTuple.append(instructor[3]) # time
                                    StudentInMeetingTable.append(StudentInMeetingTuple[:])
                                    del StudentInMeetingTuple[:]
                                
                            # make WhenWhereMeetTuple and WhenWhereMeetTable
                            for instructor in INSTRUCTOR_list:
                                if instructor[5] == "":
                                    instructor[5] = None
                                WhenWhereMeetTuple.append(CID_info[0]) # CID
                                WhenWhereMeetTuple.append(CID_info[1]) # term
                                WhenWhereMeetTuple.append(instructor[0]) # instructor
                                WhenWhereMeetTuple.append(instructor[2]) # days
                                WhenWhereMeetTuple.append(instructor[3]) # time
                                WhenWhereMeetTuple.append(instructor[4]) # building
                                WhenWhereMeetTuple.append(instructor[5]) # room
                                WhenWhereMeetTuple.append('0') # summer conflict due to same CID
                                WhenWhereMeetTuple.append('0') # summer conflict due to same day/time/building/room
                                # default 0 = false, change to 1 if there is a conflict

                                WhenWhereMeetTable.append(WhenWhereMeetTuple[:])
                                del WhenWhereMeetTuple[:]

                        # reset for new chunk of information
                        #del CID_info[:]
                        for i in range(len(INSTRUCTOR_info)):
                            INSTRUCTOR_info[i] = ""
                        instructorName = ""
                        del INSTRUCTOR_list[:]
                        del SEAT_info[:]
                        del SEAT_list[:]
                        
                    continue
                
                # if counter == 1, we are in section containing CID information
                if (counter == 1):
                    if "CID" in row:
                        continue

                    for i in range(len(row)):
                        CID_info[i] = row[i]
                    
                    # conflicts due to same CID in same term    
                    if row[0] not in term_CIDs:
                        term_CIDs.append(row[0])
                    else:
                        conflicting_CIDs.append(row[0])
                    
                # if counter == 2, we are in section containing Instructor(s) information    
                if (counter == 2):
                    if "INSTRUCTOR(S)" in row:
                        continue
                    
                    # skip row where only the class type is given
                    if row[0] == "" and row[2] == "" and row[3] == "" and row[4] == "" and row[5] == "":
                        continue
                    
                    if row[0] != "":
                        instructorName = row[0]
                        
                        
                    INSTRUCTOR_info[0] = instructorName
                
                    # ============== CHANGE THIS LATER TO ACCOUNT FOR MULTIPLE INSTRUCTORS @1107
                    #if row[1] == "" and row[2] == "" and row[3] == "" and row[4] == "" and row[5] == "":
                        #print("do nothing")
                    #else:
                    if row[1] != "" and row[2] != "" and row[3] != "" and row[4] != "" and row[5] != "":
                        for i in range(1, len(row)):
                            INSTRUCTOR_info[i] = row[i]
                    
                    
                    # literally spent 2-3 hours debugging this one line,
                    # when all I had to do was look in the StackOverflow Bible
                    # http://stackoverflow.com/questions/5280799/list-append-changing-all-elements-to-the-appended-item
                    INSTRUCTOR_list.append(INSTRUCTOR_info[:])
                        
                    # conflicts due to same day/time/building/room in same term
                    # not a conflict if lecture, since you can have multiple CIDs
                    # for one lecture
                    if row[1] != "" and row[2] != "" and row[3] != "" and row[4] != "" and row[5] != "":
                        for i in range(2, len(row)):
                            spacetime[i-2] = row[i]
                            
                    if spacetime not in term_spacetime:
                        term_spacetime.append(spacetime[:])
                    else:
                        if row[1] == "Lecture":
                            continue
                        conflicting_spacetime.append(spacetime[:])
                        
                # if counter == 3, we are in section containing Seat/Student info        
                if (counter == 3):
                    if "SEAT" in row:
                        continue
                    
                    for column in row:
                        SEAT_info.append(column)
                        
                    SEAT_list.append(SEAT_info[:])
                    
                    del SEAT_info[:]
        
          
        for item in WhenWhereMeetTable:
            if item[1] == CID_info[1]:
                if item[0] in conflicting_CIDs:
                    item[-2] = "1"
                if item[3:7] in conflicting_spacetime:
                    item[-1] = "1"
            if item[2] == "":
                item[2] = "Unknown"
                    
        for item in CourseMeetingTable:
            if item[-2] == "":
                item[-2] = "Unknown"
                
        for item in StudentInMeetingTable:
            if item[2] == "":
                item[2] = "Unknown"
            if item[6] == "":
                item[6] = None

        # # http://stackoverflow.com/questions/5506511/python-converting-list-of-lists-to-tuples-of-tuples
        StudentTable = tuple(tuple(x) for x in StudentTable)
        CourseMeetingTable = tuple(tuple(x) for x in CourseMeetingTable)
        CourseTable = tuple(tuple(x) for x in CourseTable)
        StudentInMeetingTable = tuple(tuple(x) for x in StudentInMeetingTable)
        WhenWhereMeetTable = tuple(tuple(x) for x in WhenWhereMeetTable)

        # ################################################################
        # ############### CONNECTING TO DATABASE #########################
        # ################################################################  
        
        try: 
            conn = psycopg2.connect(database='postgres', user=os.environ['USER'],port="5432")
        except:
            print ("Error: Cannot connect to database 'mydb'")

        cur = conn.cursor()

        # # # ################################################################
        # # # ################## CREATING TABLES #############################
        # # # ################################################################

        cur.execute('''CREATE TABLE IF NOT EXISTS Student
            (SID INT PRIMARY KEY NOT NULL,
             SURNAME VARCHAR(100),
             PREFNAME VARCHAR(100),
             EMAIL VARCHAR(100)); ''')

        cur.execute('''CREATE TABLE IF NOT EXISTS CourseMeeting
              (CID INT,
              term INT,
              subj VARCHAR(10),
              crse VARCHAR(10),
              sec INT,
              instructor VARCHAR(30),
              type VARCHAR(30)); ''')

        cur.execute('''CREATE TABLE IF NOT EXISTS Course
              (SUBJ VARCHAR(10),
              CRSE VARCHAR(10),
              UNITS VARCHAR(20),
              PRIMARY KEY(SUBJ, CRSE));''')

        cur.execute(''' CREATE TABLE IF NOT EXISTS StudentInMeeting
              (CID INT,
              TERM INT,
              INSTRUCTOR VARCHAR(50),
              SEAT INT,
              SID INT,
              LEVEL VARCHAR(2),
              UNITS FLOAT,
              CLASS VARCHAR(2),
              MAJOR VARCHAR(20),
              GRADE VARCHAR(20),
              STATUS VARCHAR(20),
              GRADENUM INT,
              day VARCHAR(10),
              time VARCHAR(20)); ''')

        cur.execute(''' CREATE TABLE IF NOT EXISTS WhenWhereMeet
              (CID INT,
              TERM INT,
              INSTRUCTOR VARCHAR(30),
              DAY VARCHAR(10),
              TIME VARCHAR(20),
              BUILDING VARCHAR(20),
              ROOM INT,
              CONFLICT_CID INT,
              CONFLICT_SPACETIME INT); ''')

        # ################################################################
        # ###################### INSERTIONS ##############################
        # ################################################################

        # # http://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query
        Student_str = ','.join(cur.mogrify("(%s,%s,%s,%s)", x) for x in StudentTable)
        cur.execute("INSERT INTO Student VALUES " + Student_str)

        Course_Meeting_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x) for x in CourseMeetingTable)
        cur.execute("INSERT INTO CourseMeeting VALUES " + Course_Meeting_str)

        if CourseTable:
            Course_str = ','.join(cur.mogrify("(%s,%s,%s)", x) for x in CourseTable)
            cur.execute("INSERT INTO Course VALUES " + Course_str)

        Student_In_Meeting_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in StudentInMeetingTable)
        cur.execute("INSERT INTO StudentInMeeting VALUES " + Student_In_Meeting_str)

        When_Where_Meet_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in WhenWhereMeetTable)
        cur.execute("INSERT INTO WhenWhereMeet VALUES " + When_Where_Meet_str)

        conn.commit()

        print("changes made to database. ")
        conn.close()
        print("closed connection.")

parser()










