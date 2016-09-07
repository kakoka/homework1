# Homework 1. Difficult task. Pavel M. Konotopov
# 07-09-2016
from datetime import datetime

#setting some variables
A_COUNT = 0

#define files with questions and answers, log-file
qa_file = "qa.txt"
log_file = "log.txt"
log = open(log_file, 'a', encoding='utf-8')

#Who are you? no empty names supported!

while True:
    name = input ("What is your name, my little friend? \n My name is: ")
    if name == '':
        print ("You give me an empty name.\nTry again, please.")
    elif name != '':
        break

#Captalize'em'all
name = name.title()

#Getting time and date
today = str(datetime.now())

#Howdy %USERNAME%! Lets start...
print ("Howdy",name,"!\n","Today is",today,"\n")

#Write to log Name, Date


#main
while True:
    #you never play
    if A_COUNT == 0:
        #some stats
        log_header = "Username:" + name + '\n' + today + '\n'
        log_format = '|' + '\t\t' + "Question" + '\t\t|' + "Answer" + '\t\t|' + "True or False" + '\n'
        log.write(log_header)
        log.write(log_format)
        st = input("Let's make choice!\nType 'Yes' to start game or 'No' to exit:")
    #you play again
    else:
        st = input("Play Again?\nType 'Yes' for start or 'No' to exit:")
    if st.lower() == "yes":
        # writing some stats here
        today = str(datetime.now())
        log_header = name + '\n' + today + '\n'
        log.write(log_header)
        #game stats
        #open file with q&a
        with open(qa_file, 'r', encoding='utf-8') as qa:
            #setting wrong and right counters to null
            Q_COUNT = 0
            W_COUNT = 0
            #read strings from file
            for line in qa:
            #split line from file with delimeter |
                #getting question
                q = line.split("|")[0] + ': '
                # remove \n from the end of the strings
                a = (line.split("|")[1]).rstrip('\n')
                #got the answer
                qw = input(q)
                #compare
                #right answer
                if qw.lower() == a.lower():
                    print (a)
                    Q_COUNT += 1
                    print ("You are right!\n", "Number of right answers: ", Q_COUNT, "Number of wrong answers:", W_COUNT)
                    log_date_right = q +'\t\t'+ '|' + a + '\t\t'+'|' + "True" + '\n'
                    log.write(log_date_right)
                #wrong answer
                else:
                    W_COUNT += 1 
                    print ("Wrong answer!\n", "Number of right answers: ", Q_COUNT, "Number of wrong answers:", W_COUNT)
                    log_date_wrong = q +'\t\t'+ '|' + a +'\t\t' + '|' + "False" + '\n'
                    log.write(log_date_wrong)
                A_COUNT += 1
            #write final stats into file right and wrond answers
            log_final_stat = "Game over.\n" + "Number of right answers:" + str(Q_COUNT) +'\t'+ "Number of wrong answers:" + str(W_COUNT) + '\n' + '\n'
            log.write(log_final_stat)
            print (log_final_stat)
    elif st.lower() == "no":
        print("Game over!\n")
        log_header = "Username:" + name + '\n' + today + '\n' + "Exit from game.\n"
        log.write(log_header)
        break
log.close()