import psycopg2
import os


def question3a():
    #print("QUESTION 3A")

    conn = psycopg2.connect(database="postgres", user=os.environ['USER'], port="5432")
    #print("connected to database")

    print("QUESTION 3A")
    
    cur = conn.cursor()

    cur.execute('''
                select count(distinct(sid)) from student;
                ;''')

    row = cur.fetchone()

    total_students = int(row[0])

    for i in range(1,21):
        print(str(i) + " unit(s)")
        string = "select count(distinct(sid)) from (select sid,term,sum(avgunits) as allunitsinterm from (select sid,term,crse,subj,avg(units) as avgunits from studentinmeeting natural join coursemeeting group by sid,term,crse,subj) as foo group by sid,term) as foo2 where allunitsinterm = "
        string = string + str(i) + ";"
        cur.execute(string)
        row = cur.fetchone()
        num_students = int(row[0])
        print(str((float(num_students) / float(total_students)) * 100) + "%\n")

    #print("done")
    conn.close()

def question3b():
    
    conn = psycopg2.connect(database="postgres", user=os.environ['USER'], port="5432")
    #print("connected to database")

    print("QUESTION 3B")

    cur = conn.cursor()

    for i in range(1,21):
        print(str(i) + " unit(s)")
        sum = 0
        numStudents = 0
        string_begin = """
                        SELECT GRADE
                        FROM STUDENTINMEETING NATURAL JOIN COURSEMEETING
                        WHERE SID IN (SELECT SID 
                                        FROM (SELECT SID,TERM,SUM(AVGUNITS) AS ALLUNITSINTERM
                                                FROM (SELECT SID,TERM,SUBJ,CRSE,AVG(UNITS) AS AVGUNITS, GRADE
                                                        FROM STUDENTINMEETING NATURAL JOIN COURSEMEETING
                                                        GROUP BY SID,TERM,SUBJ,CRSE,GRADE) AS FOO
                                                GROUP BY SID, TERM) AS FOO2
                                        WHERE ALLUNITSINTERM = 
                        """
        string_end = """
                        )
                    GROUP BY SID,TERM,SUBJ,CRSE,GRADE;
                    """
        string = string_begin + str(i) + string_end

        cur.execute(string)
        
        rows = cur.fetchall()
        #print(len(rows))
    
        for row in rows:
            if row[0] == "A+" or row[0] == "A":
                sum += 4.0
                numStudents += 1
            elif row[0] == "A-":
                sum += 3.7
                numStudents += 1
            elif row[0] == "B+":
                sum += 3.3
                numStudents += 1
            elif row[0] == "B":
                sum += 3.0
                numStudents += 1
            elif row[0] == "B-":
                sum += 2.7
                numStudents += 1
            elif row[0] == "C+":
                sum += 2.3
                numStudents += 1
            elif row[0] == "C":
                sum += 2.0
                numStudents += 1
            elif row[0] == "C-":
                sum += 1.7
                numStudents += 1
            elif row[0] == "D+":
                sum += 1.3
                numStudents += 1
            elif row[0] == "D":
                sum += 1.0
                numStudents += 1
            elif row[0] == "D-":
                sum += 0.7
                numStudents += 1
            else:
                continue
        print("GPA: " + str(float(sum) / float(numStudents)) + '\n')

    #print("done")
    conn.close
    


def question3c():
    
    conn = psycopg2.connect(database="postgres", user=os.environ['USER'], port="5432")
    #print("connected to database")
    
    print("QUESTION 3C")

    cur = conn.cursor()
    
    cur.execute('''SELECT INSTRUCTOR, foo.AVGGRADE
                FROM (SELECT INSTRUCTOR, AVG(GRADENUM) AS AVGGRADE
                      FROM StudentInMeeting  
                      GROUP BY INSTRUCTOR) AS foo
                WHERE foo.AVGGRADE IN (SELECT MAX(AVGGRADE)
                                       FROM (SELECT INSTRUCTOR, AVG(GRADENUM) AS AVGGRADE
                                             FROM StudentInMeeting
                                             GROUP BY INSTRUCTOR) AS foo2);''')
                     
    rows = cur.fetchall()
    
    print("Easiest instructor(s):")

    for row in rows:
        print(row)
    
    cur.execute('''SELECT INSTRUCTOR, foo.AVGGRADE
                FROM (SELECT INSTRUCTOR, AVG(GRADENUM) AS AVGGRADE
                      FROM StudentInMeeting  
                      GROUP BY INSTRUCTOR) AS foo
                WHERE foo.AVGGRADE IN (SELECT MIN(AVGGRADE)
                                       FROM (SELECT INSTRUCTOR, AVG(GRADENUM) AS AVGGRADE
                                             FROM StudentInMeeting
                                             GROUP BY INSTRUCTOR) AS foo2);''')

    rows = cur.fetchall()

    print("Hardest instructor(s):")

    for row in rows:
        print(row)  
    #print("done")
    conn.close()

def question3d():

    conn = psycopg2.connect(database="postgres", user=os.environ['USER'], port="5432")
    #print("connected to database")

    print("QUESTION 3D")

    cur = conn.cursor()

    cur.execute('''SELECT INSTRUCTOR, foo.AVGGRADE, SUBJ, CRSE
                    FROM (SELECT INSTRUCTOR, AVG(GRADENUM) AS AVGGRADE, SUBJ, CRSE
                            FROM COURSEMEETING NATURAL JOIN STUDENTINMEETING
                            WHERE SUBJ = 'ABC' AND CRSE::int >= 100 AND CRSE::int < 200
                            GROUP BY INSTRUCTOR, SUBJ, CRSE) AS foo
                    WHERE foo.AVGGRADE IN (SELECT MAX(AVGGRADE)
                    FROM (SELECT INSTRUCTOR, AVG(GRADENUM) AS AVGGRADE, SUBJ, CRSE
                            FROM COURSEMEETING NATURAL JOIN STUDENTINMEETING
                            WHERE SUBJ = 'ABC' AND CRSE::int >= 100 AND CRSE::int < 200
                            GROUP BY INSTRUCTOR, SUBJ, CRSE) AS foo2
                    GROUP BY SUBJ, CRSE)
                    order by crse
                ;''')
    
    rows = cur.fetchall()
    print("Easiest instructor(s) for each ABC 100 level course:")
    for row in rows:
        print(row)
    
    cur.execute('''SELECT INSTRUCTOR, foo.AVGGRADE, SUBJ, CRSE
                    FROM (SELECT INSTRUCTOR, AVG(GRADENUM) AS AVGGRADE, SUBJ, CRSE
                            FROM COURSEMEETING NATURAL JOIN STUDENTINMEETING
                            WHERE SUBJ = 'ABC' AND CRSE::int >= 100 AND CRSE::int < 200
                            GROUP BY INSTRUCTOR, SUBJ, CRSE) AS foo
                    WHERE foo.AVGGRADE IN (SELECT MIN(AVGGRADE)
                    FROM (SELECT INSTRUCTOR, AVG(GRADENUM) AS AVGGRADE, SUBJ, CRSE
                            FROM COURSEMEETING NATURAL JOIN STUDENTINMEETING
                            WHERE SUBJ = 'ABC' AND CRSE::int >= 100 AND CRSE::int < 200
                            GROUP BY INSTRUCTOR, SUBJ, CRSE) AS foo2
                    GROUP BY SUBJ, CRSE)
                    order by crse
                ;''')
    
    rows = cur.fetchall()
    print("Hardest instructor(s) for each ABC 100 level course:")
    for row in rows:
        print(row)
    
    #print("done")
    conn.close()

def question3e():

    conn = psycopg2.connect(database="postgres", user=os.environ['USER'], port="5432")
    #print("connected to database")

    print("QUESTION 3E")

    cur = conn.cursor()

    cur.execute('''
                SELECT CRSE, SUBJ
                FROM WHENWHEREMEET NATURAL JOIN COURSEMEETING
                WHERE CONFLICT_SPACETIME = 1
                GROUP BY SUBJ, CRSE
                ORDER BY SUBJ, CRSE
                ;''')

    rows = cur.fetchall()
    
    print("Conflicting courses:")
    for row in rows:
        print(row)

    #print("done")
    conn.close()

def question3f():

    conn = psycopg2.connect(database="postgres", user=os.environ['USER'], port="5432")
    #print("connected to database")

    print("QUESTION 3F")

    cur = conn.cursor()

    cur.execute('''
                SELECT foo2.MAJOR, foo2.avggrade
                FROM (SELECT major, AVG(SINGLEGRADE) AS AVGGRADE
                    FROM    (SELECT MAJOR, AVG(GRADENUM) AS SINGLEGRADE
                            FROM COURSEMEETING NATURAL JOIN STUDENTINMEETING
                            WHERE SUBJ = 'ABC'
                            GROUP BY SID, SUBJ, CRSE, MAJOR) AS FOO
                    GROUP BY MAJOR) as foo2
                where foo2.avggrade in (SELECT MAX(AVGGRADE)
                FROM (SELECT major, AVG(SINGLEGRADE) AS AVGGRADE
                    FROM    (SELECT MAJOR, AVG(GRADENUM) AS SINGLEGRADE
                            FROM COURSEMEETING NATURAL JOIN STUDENTINMEETING
                            WHERE SUBJ = 'ABC'
                            GROUP BY SID, SUBJ, CRSE, MAJOR) AS FOO
                    GROUP BY MAJOR) as foowhatever)
                ;''')

    rows = cur.fetchall()
    print("Best major(s):")
    for row in rows:
        print(row)

    cur.execute('''
                SELECT foo2.MAJOR, foo2.avggrade
                FROM (SELECT major, AVG(SINGLEGRADE) AS AVGGRADE
                    FROM    (SELECT MAJOR, AVG(GRADENUM) AS SINGLEGRADE
                            FROM COURSEMEETING NATURAL JOIN STUDENTINMEETING
                            WHERE SUBJ = 'ABC'
                            GROUP BY SID, SUBJ, CRSE, MAJOR) AS FOO
                    GROUP BY MAJOR) as foo2
                where foo2.avggrade in (SELECT MIN(AVGGRADE)
                FROM (SELECT major, AVG(SINGLEGRADE) AS AVGGRADE
                    FROM    (SELECT MAJOR, AVG(GRADENUM) AS SINGLEGRADE
                            FROM COURSEMEETING NATURAL JOIN STUDENTINMEETING
                            WHERE SUBJ = 'ABC'
                            GROUP BY SID, SUBJ, CRSE, MAJOR) AS FOO
                    GROUP BY MAJOR) as foowhatever)
                ;''')

    rows = cur.fetchall()
    print("Worst major(s):")
    for row in rows:
        print(row)

    #print("done")
    conn.close()

def question3g():
    
    conn = psycopg2.connect(database="postgres", user=os.environ['USER'], port="5432")
    #print("connected to database")

    print("QUESTION 3G")

    cur = conn.cursor()

    #number of students who graduate as ABC major
    cur.execute('''
                select count(distinct(sim.sid))
                from studentinmeeting as SIM
                     cross join
                      (select sid, max(term) as lastterm
                      from studentinmeeting
                      group by sid) as last
                where sim.sid = last.sid and sim.term = last.lastterm and sim.major like 'ABC%'
                ;''')

    row = cur.fetchone()

    total_students = int(row[0])
    #print(total_students)    

    #number of students who switch to ABC from something else
    cur.execute("""
                SELECT COUNT(*)
                FROM (SELECT SID, MIN(TERM) AS BEGINTERM, MAJOR AS BEGINMAJOR
                      FROM STUDENTINMEETING
                      WHERE MAJOR NOT LIKE 'ABC%'
                      GROUP BY SID, MAJOR) as BEGIN
                      CROSS JOIN
                     (SELECT SID, MAX(TERM) AS LASTTERM, MAJOR AS LASTMAJOR
                      FROM STUDENTINMEETING
                      WHERE MAJOR LIKE 'ABC%'
                      GROUP BY SID, MAJOR) As Ed
               WHERE BEGIN.SID = Ed.SID AND LASTTERM > BEGINTERM AND BEGINMAJOR != LASTMAJOR
                ;""")

    row = cur.fetchone()

    switch_students = int(row[0])
    #print(switch_students)
    print("Percent of students who transfer into one of the ABC majors: " + str(float(switch_students) / float(total_students) * 100) + "%")


    cur.execute("""
                select count(*)
                from (select sid,term,major
                      from studentinmeeting
                      group by sid,term,major) SIM1
                      cross join
                      (select sid,term,major
                      from studentinmeeting
                      group by sid,term,major) SIM2
                where SIM1.SID = SIM2.SID and SIM1.term < SIM2.term and SIM1.major not like 'ABC%' and SIM2.major like 'ABC%'
                ;""")

    row = cur.fetchone()
    total_transfers = int(row[0])
    #print(total_transfers)

    cur.execute("""
                select *
                from (select SIM1.major, count(sim1.major) as num
                      from (select sid,term,major
                            from studentinmeeting
                            group by sid,term,major) SIM1
                            cross join
                            (select sid,term,major
                             from studentinmeeting
                            group by sid,term,major) SIM2
                            where SIM1.SID = SIM2.SID and SIM1.term < SIM2.term and SIM1.major not like 'ABC%' and SIM2.major like 'ABC%'
                      group by SIM1.major) compare
                order by num desc limit 5
                ;""")

    rows = cur.fetchall()
    print("Top 5 majors that students transfer from into ABC and the percent of students from each of these majors:")
    for row in rows:
        print(row)
        print(str(float(row[1]) / float(total_transfers) * 100) + "%")


question3a()
question3b()   
question3c()
question3d()
question3e()
question3f()
question3g()
