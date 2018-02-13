import xml.etree.ElementTree as ET
import calendar
import datetime
import subprocess


def LastChosenDay(numberOfMonthBack,ChosenCalendar):
    tree = ET.parse('D:\\ControlM\\Calendars\\ExportCalendar\\out.xml')
    root = tree.getroot()
    for Calendar in root.iter('CALENDAR'):
        CalendarName = str(Calendar.get('NAME'))
        if CalendarName == ChosenCalendar:
            prevMonth = now - datetime.timedelta(numberOfMonthBack * 365 / 12)
            for Year in Calendar.iter('YEAR'):
                Yearstr = str(Year.get('NAME'))
                Daysstr = []
                Daysstr = str(Year.get('DAYS'))
                i = 0
                if (Yearstr == str(prevMonth.year)):
                    DaysArr = []
                    zero = 0
                    while (i <=11):
                        numOfDays = calendar.monthrange(int(Yearstr),i + 1)[1]
                        DaysArr.append(Daysstr[zero:(numOfDays + zero)])
                        i+=1
                        zero += numOfDays

                    Location = str(DaysArr[prevMonth.month -1][::-1].index('Y'))
                    if Location == None:
                        print("There is no Y in month : " + str(prevMonth.month) + "\nIn Year : " + str(prevMonth.year))
                        exit(1)
                    Location = int(Location)
                    NewLoc = "%s%02d%02d" %  (str(prevMonth.year),prevMonth.month,calendar.monthrange(prevMonth.year, prevMonth.month)[1] - Location)
                    return (NewLoc)


if __name__ == '__main__':
    now = datetime.datetime.now()
    Var1 = "%%\LastOneMonth" + 'LCALDAYS'
    Var2 = "%%\LastTwoMonth" + 'LCALDAYS'
    OneMonth = str(LastChosenDay(1,'LCALDAYS'))
    TwoMonth = str(LastChosenDay(2,'LCALDAYS'))

    resultOne = subprocess.call(['D:\Program Files\BMC Software\Control-M Agent\Default\EXE\ctmvar.exe','-action','set','-var',Var1,'-varexpr',OneMonth])
    resultTwo = subprocess.call(['D:\Program Files\BMC Software\Control-M Agent\Default\EXE\ctmvar.exe','-action','set','-var',Var2,'-varexpr',TwoMonth])
    if (resultOne != 0):
        print("ERROR!")
        exit(1)
    else:
        print("Defined: " + Var1 + " is equal to - " + OneMonth)

    if (resultTwo != 0):
        print("ERROR!")
        exit(1)
    else:
        print("Defined: " + Var2 + " is equal to - " + TwoMonth)