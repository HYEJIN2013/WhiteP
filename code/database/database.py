__author__ = 'ViGo'
# -*- coding: utf-8 -*-
import copy
class Student():
    name = ""
    scores = []
    def __init__(self,strname):
        self.name = strname
        self.scores = []

    def addScore(self,strscore):
        self.scores.append(strscore)

    def avg(self):
        if len(self.scores)>0:
            return round(float(sum(self.scores))/float(len(self.scores)),2)
        else:
            return 0.0
    def __repr__(self):
        returnstr = ""
        returnstr = returnstr+self.name+": "
        for i in xrange(0,len(self.scores),1):
            returnstr = returnstr  + str(self.scores[i])
            if i!=(len(self.scores)-1):
                returnstr = returnstr + " "
        return returnstr
        


class Database(object):
    students = []
    filename = ""
    def __init__(self,filename):
        #filename = raw_input()
        #infile = open(filename)
        i =0
        self.filename = filename
        for line in open(filename,"r"):
            if i!=0:
                readName = 0
                stName =  line[0:line.find(':')]
                student = Student(stName)
                line = line[line.find(':')+2:len(line)]
                scores = line.split(' ')
                for score in scores:
                    scoreNumber = int(score)
                    student.addScore(scoreNumber)


                self.students.append(student)
                #print self.students
            i+=1

    def addStudent(self,name):
        student = Student(name)
        self.students.append(student)

    def delStudent(self,name):
        #print "--"
        indexToDel = -1
        for i in xrange(0,len(self.students),1):
            if self.students[i].name==name:
                indexToDel=i
                #del self.students[i]
            #else:
             #   print self.students[i]
        if indexToDel>-1:
            del self.students[indexToDel]
        #print "--"

    def backup(self):
        self.filename="db_new.txt"
        infile = open(self.filename,'w')
        infile.write(str(len(self.students))+"\n")
        for student in self.students:
            infile.write(str(student)+"\n")

    def bestStudent(self):
        bestStudent = object
        maxavg = 0
        for student in self.students:
            #print student.avg()
            if student.avg()>maxavg:
                bestStudent = student
                maxavg=student.avg()
        return bestStudent



        




#qwe = Student("пупкин")
#qwe.addScore(5)
#qwe.addScore(4)
#qwe.addScore(5)
#print qwe.avg()
#print qwe

base = Database("db.txt")

print base.students[2]

base.addStudent("Море волнуется раз")

print base.students[4]
base.delStudent("Петя Васечкин")

base.backup()

print base.bestStudent()
