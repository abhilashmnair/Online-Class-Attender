from selenium import webdriver
import datetime
from os import path
import schedule
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")


opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1
})

meetLink = 'https://meet.google.com/'
username = "18b211@nssce.ac.in"
password = "Abhilash@2000"

today = datetime.datetime.now().strftime("%A")

def startScreen():
    print('\n    Auto Class Attender (for Google Meet)')
    print('--------------------------------------------')
    print('1. Create/Update new timetable')
    print('2. View existing timetable')
    print('3. Create/Update class links')
    print('4. View existing class links')
    print('5. Use existing timetable and links')
    print('6. Exit')
    
    opt = int(input('Enter your choice : '))
    return opt

def bypass(driver):
    driver.get('https://stackoverflow.com/users/login')
    driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(username)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button').click()
    time.sleep(3)

def openMeeting(link,end_time):
    driver = webdriver.Chrome('C:\webdrivers\chromedriver.exe',options=opt)
    newLink = str(meetLink) + str(link)
    bypass(driver)
    driver.get(newLink)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[1]/div/div/div').click()
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[2]/div/div').click()
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]').click()
    members = driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[8]/div[3]/div[6]/div[3]/div/div[2]/div[1]/span/span/div/div/span[2]').getText()
    current = datetime.datetime.now()
    current_time=current.strftime("%H:%M")
    while(str(end_time)!=str(current_time) and int(members) < 10):
        time.sleep(5)
        current = datetime.datetime.now()
        current_time=current.strftime("%H:%M")
    driver.quit()

def joinClass() :
    conn_tt = sqlite3.connect('timetable.db')
    c_tt = conn_tt.cursor()
    conn_l = sqlite3.connect('links.db')
    c_l = conn_l.cursor()
    for row in c_tt.execute("SELECT * FROM timetable where day = '%s'"%(today.lower())):
        sub = row[1].lower()
        start_time = row[2]
        end_time = row[3]
        current = datetime.datetime.now()
        current_time=current.strftime("%H:%M")
        try:
            for row in c_l.execute("SELECT links FROM links WHERE subject='%s'"%(sub)):
                link = row[0]
            if(start_time < current_time and end_time > current_time):
                print("Oops...Your're late for ",sub," class.")
                openMeeting(link,end_time)
            else:
                while(str(start_time) != str(current_time)):
                    time.sleep(5)
                    current = datetime.datetime.now()
                    current_time=current.strftime("%H:%M")
                print('Joining.\nSubject : ',sub)
                openMeeting(link,end_time)
        except:
            print('Class link not found!')
        print(sub,' class over.')
    print("Today's classes are over!")

choice = startScreen()

while(choice!=6) :
    if choice == 1 :
        if (not(path.exists('timetable.db'))):
            conn = sqlite3.connect('timetable.db')
            c = conn.cursor()
            c.execute('DROP TABLE IF EXISTS timetable')
            c.execute('CREATE TABLE timetable(day text, subject text, start_time text, end_time text)')
            conn.commit()
            conn.close()
            print('Table Created.')
            op = int(input('\n1. Enter class details\n2. Done\nEnter choice : '))
            while(op==1):
                day = input('Enter day : ')
                subject = input('Enter subject : ')
                start_time = input('Enter class start time (HH:MM) : ')
                end_time = input('Enter class end time (HH:MM) : ')

                conn = sqlite3.connect('timetable.db')
                c = conn.cursor()
                c.execute("INSERT INTO timetable VALUES ('%s', '%s', '%s', '%s')"%(day,subject,start_time,end_time))
                conn.commit()
                conn.close()
                print("Class added to database\n")
                op = int(input('\n1. Enter class details\n2. Done\nEnter choice : '))
        else:
            op = input('Table exists. Add to timetable? (Y/n) : ')
            while(op == 'Y' or op=='y') : 
                day = input('Enter day : ')
                subject = input('Enter subject : ')
                start_time = input('Enter class start time (HH:MM) : ')
                end_time = input('Enter class end time (HH:MM) : ')
                conn = sqlite3.connect('timetable.db')
                c = conn.cursor()
                c.execute("INSERT INTO timetable VALUES ('%s', '%s', '%s', '%s')"%(day,subject,start_time,end_time))
                conn.commit()
                conn.close()
                print("Class added to database\n")
                op = input('Update more? (Y/n) : ')
        time.sleep(1)
        choice = startScreen()

    elif choice == 2 :
        try:
            conn = sqlite3.connect('timetable.db')
            print('Day\tClass\tStart Time\tEnd Time')
            print('-----------------------------------------')
            conn = sqlite3.connect('timetable.db')
            c = conn.cursor()
            for row in c.execute("SELECT * FROM timetable"):
                print(row[0] + '\t' + row[1] + '\t' + row[2] + '\t\t' + row[3])
            conn.commit()
            conn.close()
        except:
            print('No table created. Create one!')
        time.sleep(1)
        choice = startScreen()

    elif choice == 3:
        if (not(path.exists('links.db'))):
            conn = sqlite3.connect('links.db')
            c=conn.cursor()
            c.execute('DROP TABLE IF EXISTS links')
            c.execute('CREATE TABLE links(subject text, links text)')
            conn.commit()
            conn.close()
            print('Table created')
            op = int(input('1.Enter class link\n2.Done\nEnter choice : '))
            while(op==1):
                subject = input('Enter class : ')
                link = input('Enter link (meeting code only): ')
                conn = sqlite3.connect('links.db')
                c = conn.cursor()
                c.execute("INSERT INTO links VALUES ('%s', '%s')"%(subject,link))
                conn.commit()
                print("Link added to database\n")
                op = int(input('1. Enter class link\n2. Done\nEnter choice : '))
        else :
            op = input('Table exists. Update links? (Y/n) : ')
            while(op == 'Y' or op=='y') : 
                subject = input("Enter subject to update : ")
                link = input("Enter new link code : ")
                conn = sqlite3.connect('links.db')
                c = conn.cursor()
                c.execute("UPDATE links SET links = '%s' WHERE subject = '%s'"%(link,subject))
                conn.commit()
                op = input('Update more? (Y/n) : ')
        conn.close()
        time.sleep(1)
        choice = startScreen()

    elif choice == 4 :
        if (not(path.exists('links.db'))):
            print('No links created. Please create a table!')
            time.sleep(1)
        else:
            print('\nClass\tLinks')
            print('--------------')
            conn = sqlite3.connect('links.db')
            c = conn.cursor()
            for row in c.execute("SELECT * FROM links"):
                print(row[0] + '\t' + row[1])
            conn.commit()
            conn.close()
            time.sleep(1)
        choice = startScreen()

    elif choice == 5 :
        joinClass()
        break

print('\nSee ya...')
print('--------------------------------------------')
print('        www.github.com/abhilashmnair        ')
print('      www.instagram.com/abhilashmnair       ')
print('--------------------------------------------')