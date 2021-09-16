import sqlite3


conn=sqlite3.connect('student.db')


create_course=f"""
CREATE TABLE course 
(code INTEGER PRIMARY KEY AUTOINCREMENT,
title CHAR(200) NOT NULL
);
"""

create_enrollment=f'''
CREATE TABLE enrollment(
    id INTEGER,
    code INTEGER,
    FOREIGN KEY(code) REFERENCES course(code)
)

'''

insert_course=f"""
INSERT INTO course (title)
VALUES 
('Mechanical Engineering'),
('Medicine and Surgery'),
('Pharmacy'),
('Actuarial Science'),
('Computer Science'),
('Chemical Engineering'),
('Environmental Science')

"""

try:
    '''
    Create the course and enrollment table and insert some sample courses
    '''
    conn.execute(create_course)
    conn.execute(create_enrollment)
    conn.execute(insert_course)

    conn.commit()

except sqlite3.Error as error:
    print(error)


conn.close()

def get_conn():
    '''
    Return the connection object for further manipulation
    '''
    try:
        conn=sqlite3.connect('student.db')
        return conn
    except sqlite3.Error as error:
        print(error)

def all_courses():
    '''
    Loop through all rows of the course table and returns a dictionary  containing the key  as the id and 
    title as the value
    '''
    courses={}
    conn=get_conn()
    qry=conn.execute('SELECT * FROM  course')
    rows=qry.fetchall()

    for row in rows:
        k,v=[int(row[0]),row[1]]
        courses[k]=v
    conn.close()
    return courses


    
