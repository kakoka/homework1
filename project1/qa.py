import time
from datetime import date
#define files with questions and answers, log-file
qa_file = "qa.txt"

# define file with statistics
log_file = "log.txt"

log = open(log_file, 'a', encoding='utf-8')

#setting global variables
A_COUNT = 0

#who are u?

name = input ("What is your name, my little friend? My name is:")
today = str(date.today())
#Howdy %USERNAME%! Lets start...

print ("Howdy",name.capitalize(),"!","Today is",today)

log_header = name + '\n' + today + '\n'
log_format = "Question" + '|' + "Answer" + '|' + '|' + "True or False" + '\n'
log.write(log_header)
log.write(log_format)

#print ("Let's game, type Yes for start or No")

while True:
    if A_COUNT == 0:
        st = input("Let's start game, type 'Yes' for start or 'No' to exit:")
    else:
        st = input("Again? Type 'Yes' for start or 'No' to exit:")
        log.write(log_header)
        log.write(log_format)
    if st.lower() == "yes":
        with open(qa_file, 'r', encoding='utf-8') as qa:
            Q_COUNT = 0
            W_COUNT = 0
            for line in qa:
            #split line from file with delimeter |
                q = line.split("|")[0] + ': '
                a = (line.split("|")[1]).rstrip('\n')
                qw = input(q)
                if qw.lower() == a.lower():
                    print (a)
                    Q_COUNT += 1
                    print ("You are right!", Q_COUNT)
                    log_date_right = q + '|' + a + '|' + "True" + '\n'
                    log.write(log_date_right)
                else:
                    W_COUNT += 1 
                    print ("Wrong answer!", W_COUNT)
                    log_date_wrong = q + '|' + a + '|' + "False" + '\n'
                    log.write(log_date_wrong)
                A_COUNT += 1
                #write final stats into file
            log_final_stat = "right:" + str(Q_COUNT) + "wrong:" + str(W_COUNT) + '\n' + 'end of seesion' + '\n'
            log.write(log_final_stat)
            print (log_final_stat)
    elif st.lower() == "no":
        print("Game over!")
        break
log.close()
#else:
#	print("Please, print Yes or No")
