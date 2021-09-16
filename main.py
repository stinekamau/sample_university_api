from bottle import Bottle,run,template,route
from database import all_courses, get_conn
from utilities import *

def api():    
        @route('/enroll/<student>/<course>')
        def enroll(student,course):
            courses=all_courses()
            #Check for the validity of the student id
            if  check_student_id(student):
                conn=get_conn() 
                #Check if the course exists in the database
                if course in courses.values():
                    try:
                            k=[int(k) for k,v in courses.items() if v==str(course)][0]
                            query='''INSERT INTO enrollment (id,code)  VALUES (?,?)'''
                            conn.execute(query,(student,k))
                            conn.commit()
                            conn.close()
                            return f"Successfully Enrolled {student} into the course {course}"
                    finally:
                        conn.close()
                #The course does not exist in the database        
                else:
                    try:
                        #Create a new record containing the new course
                        temp="""INSERT INTO course (title) VALUES (?)"""
                        conn.execute(temp,(course,))            
                        conn.commit()

                        #Now that the course has been created in the course table , Obtain it's Id and  insert 
                        #into the enrollment table. 
                        k=''
                        for k,v in courses.items():
                            if str(v)==str(course):
                                k=int(k)
                        query='''INSERT INTO enrollment (id,code)  VALUES (?,?)'''
                        conn.execute(query,(student,k))
                        conn.commit()
                        return f"Successfully Enrolled {student} into the course {course}"
                    finally:
                        conn.close() #Close the connection

            
            else:
                return "The  student id must have eight decimal numbers"
                
        @route('/drop/<student>/<course>')
        def drop(student,course):
            try:
                    courses=all_courses()
                    conn=get_conn()
                    #check for the valididity of the student id
                    if check_student_id(student):
                        k=[int(k) for k,v in courses.items() if v==course][0]
                        #Remove the record from the database
                        query=f"""DELETE FROM  enrollment WHERE id={student} AND code={k}"""
                        conn.execute(query)
                        #Save  the database state
                        conn.commit()
                        return f"Successfully deleted the {course}  of the student {student}"
                    else:
                        return "The  student id must have eight decimal numbers"
            finally:
                conn.close()
            
        @route('/list/<student>')
        def enlisted(student):
            #Validate the student id has 8 numbers
            if check_student_id(student):
                conn=get_conn()
                prompt=f"""SELECT code from enrollment where id={student}"""
                query=conn.execute(prompt)
                course_id=[]
                #Loop through  the result of the query and extract only the course id
                for row in query.fetchall():
                    course_id.append(row[0])

                arr=tuple(course_id)
                print(arr)
                #Create the parameterized query for the database
                pm= ','.join('?' for i in arr)
                qry="""SELECT title FROM course WHERE code in (%s)"""
                val_qry=conn.execute("SELECT title FROM course WHERE code in (%s)"%pm,arr)
                
                res=''
                #Loop through the results of the query  and extract the course title
                for item in val_qry.fetchall():
                    res+=item[0]
                    res+=',  '
                return f"Student {student} has been enrolled in  {res}"

        run(host='localhost', port=8080,server='paste',debug=True)

if __name__=='__main__':
    api()
                
        
        
        
    

        



