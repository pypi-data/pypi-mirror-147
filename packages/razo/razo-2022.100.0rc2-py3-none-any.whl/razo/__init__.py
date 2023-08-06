#coding=utf-8
import datetime
import sys
import time
import os

try:
    from langpack import pack
except ModuleNotFoundError as aheddew:
    from langpack_d import pack
vers=['2022.100.0rc2','sys_1rc2']
rooting=False
sudoroot=False
nowsudo=False
try:
    if sys.argv[1]=='-root':
        rooting=True
except IndexError as inddde:
    rooting=False
liense=pack[0]
def setting():
    print(pack[1])
    print(liense)
    a=input(pack[2])
    if a=='n':
        print(pack[3])
        time.sleep(5)
        sys.exit(0)
    print(pack[4])
    a=input('\033[0;30;40m')
    print('\033[0;37;40m')
    with open('settings.py','a') as c:
        c.write("rootpass={}\n".format(a.encode()))
    a=input(pack[5])
    with open('settings.py','a') as c:
        c.write("username='{}'\n".format(a))
    
def showinfo():
    listget=pack[13]
    timer=datetime.datetime.now()
    weekday=listget[timer.weekday()]
    print(timer.strftime(pack[14])+' {}'.format(weekday) )
    tdo=[]
    print('Razo {0}({1})'.format(vers[0],vers[1]))
    print(pack[6])
    print(pack[7])


h=pack[8]



if __name__=='__main__':
    try:
        import settings
        d=settings.rootpass
        username=settings.username
    except ImportError as e:
        setting()
    
def sc():
    global sudoroot
    if not sudoroot:
        a=input(pack[9]+'\033[8;37;40m')
        print('\033[8;37;40m')
        import settings
        if a==settings.rootpass.decode():
            sudoroot=True
            return True
        else:
            print(pack[18])
            return False
    else:
        return True
    
def wai(a):
    global rooting
    global sudoroot
    global nowsudo
    if a=='help':
        print(h)
    elif a=='su':
        a=input(pack[9]+'\033[8;37;40m')
        print('\033[0;37;40m')
        import settings
        if a==settings.rootpass.decode():
            rooting=True
        else:
            time.sleep(2)
            print(pack[10])
    elif a=='shutdown':
        if rooting:
            yes=input(pack[11])
            if yes=='y':
                print(pack[12])
                time.sleep(5)
                sys.exit(0)
        else:
            print(pack[15])
    elif a=='info':
        showinfo()
    elif a=='setting':
        if rooting:
            setting()
            rooting=False
        else:
            print(pack[15])
    elif a=='time':
        listget=pack[13]
        timer=datetime.datetime.now()
        weekday=listget[timer.weekday()]
        print(timer.strftime(pack[14])+' {}'.format(weekday) )
        #The line between usually and sudo.
    elif a=='sudo help':
        if sc():
            nowsudo=True
        print(h)
        nowsudo=False
    elif a=='sudo su':
        if sc():
            nowsudo=True
        a=input(pack[9]+'\033[8;37;40m')
        import settings
        if a==settings.rootpass:
            rooting=True
        else:
            time.sleep(2)
            print('su:Sorry')
        nowsudo=False
    elif a=='sudo shutdown':
        if sc():
            nowsudo=True
        if nowsudo:
            yes=input(pack[11])
            if yes=='y':
                print(pack[12])
                time.sleep(5)
                sys.exit(0)
        else:
            print(pack[15])
    elif a=='sudo info':
        if sc():
            nowsudo=True
        showinfo()
        nowsudo=False
    elif a=='sudo setting':
        if sc():
            nowsudo=True
        if nowsudo:
            setting()
            rooting=False
            sudoroot=False
            nowsudo=False
        else:
            print(pack[15])
    elif a=='sudo time':
        if sc():
            nowsudo=True
        listget=pack[13]
        timer=datetime.datetime.now()
        weekday=listget[timer.weekday()]
        print(timer.strftime(pack[14])+' {}'.format(weekday) )
        nowsudo=False
    else:
        try:
            os.system(a)
        except SystemExit as fhuuuifr:
            pass
def main_p():
    while True:
        if rooting:
            a=input('[root]>>>')
        else:
            a=input('[user]>>>')
        wai(a)
if __name__=='__main__':
    showinfo()
    import settings
    print(pack[17].format(settings.username))
    main_p()

