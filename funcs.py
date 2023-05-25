import datetime as dt
import os
import math
import numpy as np
from numpy import linalg as la
import itertools

ver = 0

def isint(number):
    try:
        int(number)
        return True
    except ValueError:
        return False

def isfloat(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def exist (file):
    if os.path.exists (file) == True:
        return True
    else:
        return False

def readfile (file):
    if exist (file) == True:
        q = open(file, errors = 'ignore')
        lines = q.readlines()
        line = 0
        global ver
        while True:
            if 'RINEX VERSION / TYPE' in lines[line]:
                ver1 = lines[line].split()[0]
                type = lines[line]
                break
            else:
                line += 1
        if 'OBS' in type:
            if ver1.startswith('2'):
                return readobsrinex2(file)
                ver = 2
            elif ver1.startswith('3'):
                ver = 3
                return readobsrinex3(file)
            elif ver1.startswith('4'):
                print('разработка')
            else:
                print('Невозможно определить версию файла RINEX')
        elif 'NAV' in type:
            if ver1.startswith('2'):
                ver = 2
                return readnavrinex2(file)
            elif ver1.startswith('3'):
                ver = 3
                return readmixnavrinex3(file)
            elif ver1.startswith('4'):
                print('В разработке')
            else:
                print('Невозможно определить версию файла RINEX')
        else:
            print('Невозможно определить тип файла')
    else:
        print('Файл не найден')

def mnk(obs):
    line = 0
    while True:
        x = obs[line][4][0]
        y = obs[line][4][1]
        z = obs[line][4][2]
        line += 1
        if line == obs.index(obs[-1]):
            x = x + obs[line][4][0]
            y = y + obs[line][4][1]
            z = z + obs[line][4][2]
            break
    k = np.array(range(len(obs)))
    f = np.array([x * z + y for z in range(len(obs))])
    b = f + np.random.normal(0, k, y)
    mx = x.sum() / len(obs)
    my = y.sum() / len(obs)
    a2 = np.dot(x.T, x) / len(obs)
    a11 = np.dot(x.T, y) / len(obs)
    kk = (a11 - mx * my) / (a2 - mx ** 2)
    bb = my - kk * mx
    ff = np.array([kk * b + bb for z in range(len(obs))])
    return (x, y, z)
#мир уступает дорогу тому, кто знает куда идти    ауф
def readobsrinex2(file):
    q = open(file, errors='ignore')
    lines = q.readlines()
    line = 0
    lines = [el.replace('#', ' #') for el in lines]
    chas1 = []
    for i in range(len(lines)):
        if 'RINEX VERSION / TYPE' in lines[line]:
            qwer = lines[line].split()
            type = qwer[3]
            line += 1
        elif 'PGM / RUN BY / DATE' in lines[line]:
            line += 1
        elif 'COMMENT' in lines[line]:
            line += 1
        elif 'MARKER NAME' in lines[line]:
            line += 1
        elif 'OBSERVER / AGENCY' in lines[line]:
            line += 1
        elif 'REC # / TYPE / VERS' in lines[line]:
            line += 1
        elif 'ANT # / TYPE' in lines[line]:
            line += 1
        elif 'APPROX POSITION XYZ' in lines[line]:
            line += 1
        elif 'ANTENNA: DELTA H/E/N' in lines[line]:
            line += 1
        elif 'WAVELENGTH FACT L1/2' in lines[line]:
            line += 1
        elif '# / TYPES OF OBSERV' in lines[line]:
            qwer = lines[line].split()
            it = isint(qwer[0])
            if it == True:
                chas1.append(qwer[1:-5])
            else:
                chas1.append(qwer[0:-5])
            line += 1
        elif 'INTERVAL' in lines[line]:
            line += 1
        elif 'TIME OF FIRST OBS' in lines[line]:
            line += 1
        elif 'LEAP SECONDS' in lines[line]:
            leap = int(lines[line].split()[0])
            line += 1
        elif 'END' in lines[line]:
            line += 1
            break
        else:
            line += 1
    del lines[0:line]
    lines = [element.replace('              ', '0') for element in lines]
    lines = [element.replace('G ', 'G') for element in lines]
    lines = [element.replace('G', ' G') for element in lines]
    obs = []
    line = 0
    for i in range(len(lines)):
        if 'G' in lines[line] or 'R' in lines[line] and 'COMMENT' not in lines[line]:
            temp = lines[line].split()
            if 80 <= int(temp[0]) <= 99:
                year = 1980 + int(temp[0])
            elif 0 <= int(temp[0]) <= 79:
                year = 2000 + int(temp[0])
            else:
                raise Warning('Нет времени наблюдения')
            time = [year, int(temp[1]), int(temp[2]), int(temp[3]), int(temp[4]), float(temp[5])]
            satkol = int(temp[7])
            satlist1 = temp[8:]
            linedop = line + 1
            linesat = 0
            for i in range(satkol):
                obsline = lines[linedop].split()
                ismer = []
                q = 0
                for i in range(len(obsline)):
                    ismer.extend([float(obsline[q])])
                    q += 1
                abv = []
                abv.extend(time)
                abv.extend([satlist1[linesat]])
                abv.extend(ismer)
                obs.append(abv)
                linedop += 1
                linesat += 1
            line += 1
        elif 'COMMENT' in lines[line]:
            line += 1
        elif len(lines[line].split()) == 2:
            line += 1
        else:
            line += 1
    if 'G' in type:
        return type, chas1, obs
    else:
        return type, leap, chas1, obs

def readnavrinex2(file):
    q = open(file, errors='ignore')
    lines = q.readlines()
    type = lines[0].split()[1] + lines[0].split()[2] + lines[0].split()[3]
    if 'GPS' in type or 'GALILEO' in type or 'QZSS' in type or 'BDS' in type or 'IRNSS' in type:
        return readnavgpsrinex2(file)
    elif 'GLONASS' in type or 'SBAS' in type:
        return readnavglonassrinex2(file)
    else:
        raise Warning('Невозможно определить спутниковую систему файла')

def readnavglonassrinex2(file):
    q = open(file, errors='ignore')
    lines = q.readlines()
    line = 0
    for i in range(len(lines)):
        if 'RINEX VERSION / TYPE' in lines[line]:
            ver = lines[line].split()[0]
            type = lines[line].split()[1] + ' ' + lines[line].split()[2]
            line += 1
        elif 'PGM / RUN BY / DATE' in lines[line]:
            pgm = lines[line].split()
            try:
                aaa = int(pgm[-8])
                if aaa != None:
                    vr = -9
            except:
                vr = -8
            create_date2 = pgm[vr:-6]
            if len(create_date2) == 3:
                create_date = create_date2[0] + create_date2[1] + ' ' + create_date2[2]
            elif len(create_date2) == 2:
                create_date = create_date2[0] + ' ' + create_date2[1]
            else:
                create_date = create_date2
            line += 1
        elif 'COMMENT' in lines[line]:
            line += 1
        elif 'CORR TO SYSTEM TIME' in lines[line]:
            corr1 = lines[line].split()
            corr = [corr1[0], corr1[1], corr1[2], corr1[3]]
            line += 1
        elif 'LEAP SECONDS' in lines[line]:
            leap = int(lines[line].split()[0])
            line += 1
        elif 'END' in lines[line]:
            line += 1
            break
        else:
            line += 1
    del lines[0:line]
    line = 0
    lines = [element.replace('E', 'e') for element in lines]
    lines = [element.replace('0-', '0 -') for element in lines]
    lines = [element.replace('1-', '1 -') for element in lines]
    lines = [element.replace('2-', '2 -') for element in lines]
    lines = [element.replace('3-', '3 -') for element in lines]
    lines = [element.replace('4-', '4 -') for element in lines]
    lines = [element.replace('5-', '5 -') for element in lines]
    lines = [element.replace('6-', '6 -') for element in lines]
    lines = [element.replace('7-', '7 -') for element in lines]
    lines = [element.replace('8-', '8 -') for element in lines]
    lines = [element.replace('9-', '9 -') for element in lines]
    lines = [element.replace('   ', '> ') for element in lines]
    nav = []
    for i in range(len(lines)):
        curline = lines[line].split()
        if '>' not in curline:
            satnum = int(curline[0])
            year = int(curline[1])
            if 80 <= year <= 99:
                year = year + 1980
            elif 0 <= year <= 79:
                year = year + 2000
            else:
                raise Warning('Год неопознан')
            month = int(curline[2])
            day = int(curline[3])
            hour = int(curline[4])
            minute = int(curline[5])
            second = float(curline[6])
            sv_clock_bias = float(curline[7])
            sv_relative_frequency = float(curline[8])
            message_frame_time = float(curline[9])
            broadline1 = lines[line + 1].split()
            broadline2 = lines[line + 2].split()
            broadline3 = lines[line + 3].split()
            satpositionX = float(broadline1[1])
            satvelocityX = float(broadline1[2])
            satXacceleration = float(broadline1[3])
            sathealth = float(broadline1[4])
            satpositionY = float(broadline2[1])
            satvelocityY = float(broadline2[2])
            satYacceleration = float(broadline2[3])
            satfrequencynum = float(broadline2[4])
            satpositionZ = float(broadline3[1])
            satvelocityZ = float(broadline3[2])
            satZacceleration = float(broadline3[3])
            satageofoperinf = float(broadline3[4])
            navtemp = [satnum, year, month, day, hour, minute, second, sv_clock_bias, sv_relative_frequency, message_frame_time,
                       satpositionX, satvelocityX, satXacceleration, sathealth,
                       satpositionY, satvelocityY, satYacceleration, satfrequencynum,
                       satpositionZ, satvelocityZ, satZacceleration, satageofoperinf]
            nav.append(navtemp)
            line += 1
        elif '>' in curline:
            line += 1
        else:
            del lines[line]
        if line + 3 == len(lines):
            break
        else:
            line += 1
    return nav, ver, type, create_date, corr, leap

def readnavgpsrinex2(file):
    q = open(file, errors='ignore')
    lines = q.readlines()
    line = 0
    for i in range(len(lines)):
        if line == len(lines):
            break
        if 'RINEX VERSION / TYPE' in lines[line]:
            ver = lines[line].split()[0]
            type = lines[line].split()[2]
            line += 1
        elif 'PGM / RUN BY / DATE' in lines[line]:
            date_create_file = lines[line][-40:-20].rsplit()
            date_create_file = ''.join(date_create_file)
            date_create_file2 = 'Дата создания файла RINEX: ' + date_create_file[0:4] + '.' \
                                + date_create_file[5:6] + '.' + date_create_file[7:8]
            line += 1
        elif 'COMMENT' in lines[line]:
            line += 1
        elif 'ION ALPHA' in lines[line]:
            alpha = lines[line].split()
            alpha.pop(-1)
            alpha.pop(-1)
            alpha = [element.replace('D', 'e') for element in alpha]
            alpha = [float(element) for element in alpha]
            line += 1
        elif 'ION BETA' in lines[line]:
            beta = lines[line].split()
            beta.pop(-1)
            beta.pop(-1)
            beta = [element.replace('D', 'e') for element in beta]
            beta = [float(element) for element in beta]
            line += 1
        elif 'DELTA' in lines[line]:
            utc = lines[line].split()
            utc = [element.replace('D', 'e') for element in utc]
            q1 = utc[0][0:19]
            q1 = float(q1)
            q2 = utc[0][19:]
            q2 = float(q2)
            utc.pop(0)
            utc.pop(-1)
            utc.pop(-1)
            utc = [int(element) for element in utc]
            utc.append(q1)
            utc.append(q2)
            utc[1], utc[0] = utc[0], utc[1]
            line += 1
        elif 'LEAP' in lines[line]:
            leap = lines[line].split()
            leap.pop(-1)
            leap.pop(-1)
            leap = [float(element) for element in leap]
            line += 1
        elif 'END' in lines[line]:
            line += 1
            break
        else:
            line += 1
    del lines[0:line]
    line = 0
    lines = [element.replace('D', 'e') for element in lines]
    lines = [element.replace('0-', '0 -') for element in lines]
    lines = [element.replace('1-', '1 -') for element in lines]
    lines = [element.replace('2-', '2 -') for element in lines]
    lines = [element.replace('3-', '3 -') for element in lines]
    lines = [element.replace('4-', '4 -') for element in lines]
    lines = [element.replace('5-', '5 -') for element in lines]
    lines = [element.replace('6-', '6 -') for element in lines]
    lines = [element.replace('7-', '7 -') for element in lines]
    lines = [element.replace('8-', '8 -') for element in lines]
    lines = [element.replace('9-', '9 -') for element in lines]
    nav1 = []
    while True:
        if line == lines.index(lines[-1]):
            nav1.append([float(elements) for elements in lines[line].split()])
            break
        elif lines[line].startswith('   '):
            line += 1
        else:
            prenav = lines[line].split()
            prenav = [float(element) for element in prenav]
            for i in range(7):
                line += 1
                term = []
                term = lines[line].split()
                term = [float(element) for element in term]
                prenav.append(term)
            nav1.append(prenav)
    line = 0
    nav = []
    for i in range(len(nav1)):
        if line == len(nav1) - 1:
            break
        nav2 = []
        el = 0
        for i in range(10):
            nav2.append(nav1[line][el])
            el += 1
        el = 0
        for i in range(4):
            nav2.append(nav1[line][10][el])
            el += 1
        el = 0
        for i in range(4):
            nav2.append(nav1[line][11][el])
            el += 1
        el = 0
        for i in range(4):
            nav2.append(nav1[line][12][el])
            el += 1
        el = 0
        for i in range(4):
            nav2.append(nav1[line][13][el])
            el += 1
        el = 0
        for i in range(4):
            nav2.append(nav1[line][14][el])
            el += 1
        el = 0
        for i in range(4):
            nav2.append(nav1[line][15][el])
            el += 1
        if line == nav1.index(nav1[-2]):
            nav2.append(nav1[line][0])
            nav.append(nav2)
        else:
            nav2.append(nav1[line][16][0])
            nav.append(nav2)
        line += 1
    line = 0
    for i in range(len(nav)):
        if line == len(nav):
            break
        if 80 <= nav[line][1] <= 99:
            nav[line][1] = nav[line][1] + 1900
            line += 1
        elif 0 <= nav[line][1] <= 79:
            nav[line][1] = nav[line][1] + 2000
            line += 1
        else:
            raise Warning('Год неопознан')
    return ver, date_create_file2, alpha, beta, utc, leap, nav, type

def readobsrinex3(file):
    q = open(file, errors='ignore')
    lines = q.readlines()
    line = 0
    chas = []
    phase_shift = []
    glo_freq = []
    for i in range(len(lines)):
        if 'RINEX VERSION' in lines[line]:
            qwe = lines[line].split()
            if 'MIXED' in qwe:
                typeobs = 'MIXED'
            elif 'GPS' in qwe:
                typeobs = 'GPS'
            elif 'GALILEO' in qwe:
                typeobs = 'GALILEO'
            elif 'BEIDOU' or 'BDS' in qwe:
                typeobs = 'BEIDOU'
            elif 'GLONASS' in qwe:
                typeobs = 'GLONASS'
            line += 1
        elif 'PGM / RUN BY / DATE' in lines[line]:
            qwe = lines[line].split()
            create_file_date = [int(qwe[-9][0:4]), int(qwe[-9][4:6]), int(qwe[-9][6:8]), int(qwe[-8][0:2]), int(qwe[-8][2:4]), int(qwe[-8][4:6])]
            line += 1
        elif 'COMMENT' in lines[line]:
            line += 1
        elif 'OBSERVER / AGENCY' in lines[line]:
            line += 1
        elif 'REC # / TYPE / VERS' in lines[line]:
            line += 1
        elif 'ANT # / TYPE' in lines[line]:
            antentype = lines[line].split()[1]
            line += 1
        elif 'ANTENNA: DELTA H/E/N' in lines[line]:
            line += 1
        elif 'MARKER NAME' in lines[line]:
            line += 1
        elif 'APPROX POSITION XYZ' in lines[line]:
            line += 1
        elif 'TIME OF FIRST OBS' in lines[line]:
            qwe = lines[line].split()
            first_obs = [int(qwe[0]), int(qwe[1]), int(qwe[2]), int(qwe[3]), int(qwe[4]), float(qwe[5])]
            line += 1
        elif 'TIME OF LAST OBS' in lines[line]:
            last_obs = [int(qwe[0]), int(qwe[1]), int(qwe[2]), int(qwe[3]), int(qwe[4]), float(qwe[5])]
            line += 1
        elif 'INTERVAL' in lines[line]:
            line += 1
        elif 'SYS / # / OBS TYPES' in lines[line]:
            chas.append(lines[line].split()[:-6])
            line += 1
        elif '# OF SATELLITES' in lines[line]:
            line += 1
        elif 'PRN / # OF OBS' in lines[line]:
            line += 1
        elif 'SYS / PHASE SHIFT' in lines[line]:
            phase_shift.append(lines[line].split()[:-4])
            line += 1
        elif 'GLONASS SLOT / FRQ #' in lines[line]:
            glo_freq.append(lines[line].split()[0:-5])
            line += 1
        elif 'GLONASS COD/PHS/BIS' in lines[line]:
            line += 1
        elif 'LEAP SECONDS' in lines[line]:
            leap = lines[line].split()[0:-2]
            line += 1
        elif 'END' in lines[line]:
            line += 1
            break
        else:
            line += 1
    del lines[0:line]
    linech = 0
    satsys = []
    for i in range(len(chas)):
        if 'G' in chas[linech]:
            chaskolgps = int(chas[linech][1])
            satsys.append(chas[linech][0])
            linech += 1
        elif 'R' in chas[linech]:
            chaskolglo = int(chas[linech][1])
            satsys.append(chas[linech][0])
            linech += 1
        elif 'E' in chas[linech]:
            chaskolgal = int(chas[linech][1])
            satsys.append(chas[linech][0])
            linech += 1
        elif 'J' in chas[linech]:
            chaskolqzss = int(chas[linech][1])
            satsys.append(chas[linech][0])
            linech += 1
        elif 'C' in chas[linech]:
            chaskolbds = int(chas[linech][1])
            satsys.append(chas[linech][0])
            linech += 1
        elif 'I' in chas[linech]:
            chaskolirnss = int(chas[linech][1])
            satsys.append(chas[linech][0])
            linech += 1
        else:
            linech += 1
    lines = [element.replace(' 1 ', ' ') for element in lines]
    lines = [element.replace(' 2 ', ' ') for element in lines]
    lines = [element.replace(' 3 ', ' ') for element in lines]
    lines = [element.replace(' 4 ', ' ') for element in lines]
    lines = [element.replace(' 5 ', ' ') for element in lines]
    lines = [element.replace(' 6 ', ' ') for element in lines]
    lines = [element.replace(' 7 ', ' ') for element in lines]
    lines = [element.replace(' 8 ', ' ') for element in lines]
    lines = [element.replace(' 9 ', ' ') for element in lines]
    lines = [element.replace(' 0 ', ' ') for element in lines]
    obs = []
    line = 0
    for i in range(len(lines)):
        if lines[line].startswith('>'):
            linep = lines[line].split()
            satkol = int(linep[7])
            time = [int(linep[1]), int(linep[2]), int(linep[3]), int(linep[4]), int(linep[5]), float(linep[6])]
            lineobs = line
            for i in range(satkol):
                o1 = lines[lineobs].split()
                sat = o1[0]
                if 'G' in sat:
                    curobs = o1[1:chaskolgps]
                    floatobs = []
                    q = 0
                    for i in range(len(curobs)):
                        a = float(curobs[q])
                        floatobs.extend([a])
                        q += 1
                    b = []
                    b.extend(time)
                    b.append(sat)
                    b.extend(floatobs)
                    obs.append(b)
                    lineobs += 1
                elif 'R' in sat:
                    curobs = o1[1:chaskolglo]
                    floatobs = []
                    q = 0
                    for i in range(len(curobs)):
                        a = float(curobs[q])
                        floatobs.extend([a])
                        q += 1
                    b = []
                    b.extend(time)
                    b.append(sat)
                    b.extend(floatobs)
                    obs.append(b)
                    lineobs += 1
                elif 'E' in sat:
                    curobs = o1[1:chaskolgal]
                    floatobs = []
                    q = 0
                    for i in range(len(curobs)):
                        a = float(curobs[q])
                        floatobs.extend([a])
                        q += 1
                    b = []
                    b.extend(time)
                    b.append(sat)
                    b.extend(floatobs)
                    obs.append(b)
                    lineobs += 1
                elif 'J' in sat:
                    curobs = o1[1:chaskolqzss]
                    floatobs = []
                    q = 0
                    for i in range(len(curobs)):
                        a = float(curobs[q])
                        floatobs.extend([a])
                        q += 1
                    b = []
                    b.extend(time)
                    b.append(sat)
                    b.extend(floatobs)
                    obs.append(b)
                    lineobs += 1
                elif 'C' in sat:
                    curobs = o1[1:chaskolbds]
                    floatobs = []
                    q = 0
                    for i in range(len(curobs)):
                        a = float(curobs[q])
                        floatobs.extend([a])
                        q += 1
                    b = []
                    b.extend(time)
                    b.append(sat)
                    b.extend(floatobs)
                    obs.append(b)
                    lineobs += 1
                elif 'I' in sat:
                    curobs = o1[1:chaskolirnss]
                    floatobs = []
                    q = 0
                    for i in range(len(curobs)):
                        a = float(curobs[q])
                        floatobs.extend([a])
                        q += 1
                    b = []
                    b.extend(time)
                    b.append(sat)
                    b.extend(floatobs)
                    obs.append(b)
                    lineobs += 1
                else:
                    lineobs += 1
            line += 1
        else:
            line += 1
    return typeobs, create_file_date, antentype, first_obs, last_obs, chas, satsys, phase_shift, glo_freq, leap, obs

def readmixnavrinex3(file):
    q = open(file, errors='ignore')
    lines = q.readlines()
    lines = [element.replace('0-', '0 -') for element in lines]
    lines = [element.replace('1-', '1 -') for element in lines]
    lines = [element.replace('2-', '2 -') for element in lines]
    lines = [element.replace('3-', '3 -') for element in lines]
    lines = [element.replace('4-', '4 -') for element in lines]
    lines = [element.replace('5-', '5 -') for element in lines]
    lines = [element.replace('6-', '6 -') for element in lines]
    lines = [element.replace('7-', '7 -') for element in lines]
    lines = [element.replace('8-', '8 -') for element in lines]
    lines = [element.replace('9-', '9 -') for element in lines]
    line = 0
    ion_corr = []
    time_sys_corr = []
    for i in range(len(lines)):
        if 'RINEX VERSION / TYPE' in lines[line]:
            if 'MIXED' in lines[line]:
                typenav = 'MIXED'
            elif 'GPS' in lines[line]:
                typenav = 'GPS'
            elif 'GALILEO' in lines[line]:
                typenav = 'GALILEO'
            elif 'BEIDOU' or 'BDS' in lines[line]:
                typenav = 'BEIDOU'
            elif 'GLONASS' in lines[line]:
                typenav = 'GLONASS'
            line += 1
        elif 'PGM / RUN BY / DATE' in lines[line]:
            qwe = lines[line].split()
            create_file_date = [int(qwe[-9][0:4]), int(qwe[-9][4:6]), int(qwe[-9][6:8]), int(qwe[-8][0:2]), int(qwe[-8][2:4]), int(qwe[-8][4:6])]
            line += 1
        elif 'COMMENT' in lines[line]:
            line += 1
        elif 'IONOSPHERIC CORR' in lines[line]:
            qwe = lines[line].split()
            ion = [qwe[0], float(qwe[1]), float(qwe[2]), float(qwe[3]), float(qwe[4])]
            ion_corr.append(ion)
            line += 1
        elif 'TIME SYSTEM CORR' in lines[line]:
            qwe = lines[line].split()
            corr = [qwe[0], float(qwe[1]), float(qwe[2]), float(qwe[3]), float(qwe[4])]
            time_sys_corr.append(corr)
            line += 1
        elif 'LEAP SECONDS' in lines[line]:
            leap = lines[line].split()[0:-2]
            line += 1
        elif 'END' in lines[line]:
            line += 1
            break
        else:
            line += 1
    del lines[0:line]
    line = 0
    lines = [element.replace('E', 'e') for element in lines]
    # gps=qzss=bds=galileo=irnss
    # glonass = sbas
    # sbas
    nav = []
    for i in range(len(lines)):
        if 'G' in lines[line] or 'R' in lines[line] or 'S' in lines[line] or 'J' in lines[line] or 'C' in lines[line] or 'I' in lines[line] or 'E' in lines[line]:
            if 'G' in lines[line] or 'J' in lines[line] or 'C' in lines[line] or 'I' in lines[line] or 'E' in lines[line]:
                curline = lines[line].split()
                navtemp = [curline[0]]
                q = 1
                for i in range(len(curline) - 1):
                    navtemp.extend([float(curline[q])])
                    q += 1
                linetemp = line + 1
                for i in range(7):
                    curline2 = lines[linetemp].split()
                    f = 0
                    for i in range(len(curline2)):
                        navtemp.extend([float(curline2[f])])
                        f += 1
                    linetemp += 1
                nav.append(navtemp)
                line += 1
            elif 'R' in lines[line] or 'S' in lines[line]:
                curline = lines[line].split()
                navtemp = [curline[0]]
                q = 1
                for i in range(len(curline) - 1):
                    navtemp.extend([float(curline[q])])
                    q += 1
                linetemp = line + 1
                for i in range(4):
                    curline2 = lines[linetemp].split()
                    f = 0
                    for i in range(len(curline2)):
                        navtemp.extend([float(curline2[f])])
                        f += 1
                    linetemp += 1
                nav.append(navtemp)
                line += 1
            else:
                line += 1
        else:
            line += 1
    return typenav, ion_corr, time_sys_corr, create_file_date, leap, nav

def compile2(nav, obs, chas):
    global ver
    line = 0
    linen = 0
    obsdatetimestart = dt.datetime(year = obs[0][0], month = obs[0][1], day = obs[0][2],
                               hour = obs[0][3], minute = obs[0][4], second = int(obs[0][5]))
    obsdatetimeend = dt.datetime(year = obs[-1][0], month = obs[-1][1], day = obs[-1][2],
                               hour = obs[-1][3], minute = obs[-1][4], second = int(obs[-1][5]))
    check1 = dt.datetime(year = 1, month = 1, day = 1, hour = 2, minute = 0, second = 1)
    check2 = dt.datetime(year = 1, month = 1, day = 1, hour = 0, minute = 0, second = 0)
    check = check1 - check2
    for i in range(len(nav)):
        navdatetime = dt.datetime(year = int(nav[linen][1]), month = int(nav[linen][2]), day = int(nav[linen][3]),
                                  hour = int(nav[linen][4]), minute = int(nav[linen][5]), second = int(nav[linen][6]))
        if obsdatetimeend < navdatetime:
            a = navdatetime - obsdatetimeend
            if a < check:
                linen += 1
            else:
                del nav[linen]
        elif obsdatetimestart > navdatetime:
            a = obsdatetimestart - navdatetime
            if a < check:
                linen += 1
            else:
                del nav[linen]
        else:
            linen += 1
    itog = []
    iq = 1
    for i in range(len(obs)):
        satsys = obs[line][6][0]
        sat = 0
        for i in range(len(chas)):
            if satsys in chas[sat] and ver == 3:
                satchas = chas[sat][2:]
            elif satsys not in chas[sat] and ver == 3:
                sat += 1
            else:
                satchas = chas[0]
        iq += 1
        if 'C1' in satchas and 'P2' not in satchas:
            timeobs = obs[line][0:6]
            pseudo = obs[line][satchas.index('C1') + 7]
        elif 'C1C' in satchas:
            timeobs = obs[line][0:6]
            pseudo = obs[line][satchas.index('C1C') + 7]
        elif 'P2' in satchas and 'C1' not in satchas:
            timeobs = obs[line][0:6]
            pseudo = obs[line][satchas.index('C1') + 7]
        elif 'C1' and 'P2' in satchas:
            timeobs = obs[line][0:6]
            pseudo = obs[line][satchas.index('C1') + 7]
        else:
            raise Warning('Нет несущей частоты')
        nsato = obs[line][6]
        timeo = dt.datetime(year = obs[line][0], month = obs[line][1], day = obs[line][2],
                            hour = obs[line][3], minute = obs[line][4], second = int(obs[line][5]))
        linen = 0
        navtemp = []
        it1 = 0
        for i in range(len(nav)):
            it1 += 1
            if ver == 3:
                nsatn = nav[linen][0]
            else:
                aqwe = nav[linen][0]
                nsatn = satsys + str(int(aqwe))
            if nsatn == nsato:
                navtemp.append(nav[linen])
            linen += 1
        linet = 0
        navdata = []
        for i in range(len(navtemp)):
            timen1 = dt.datetime(year = int(navtemp[linet][1]), month = int(navtemp[linet][2]), day = int(navtemp[linet][3]),
                                hour = int(navtemp[linet][4]), minute = int(navtemp[linet][5]), second = int(navtemp[linet][6]))
            try:
                timen2 = dt.datetime(year = int(navtemp[linet + 1][1]), month = int(navtemp[linet + 1][2]), day = int(navtemp[linet + 1][3]),
                                     hour = int(navtemp[linet + 1][4]), minute = int(navtemp[linet + 1][5]), second = int(navtemp[linet + 1][6]))
            except:
                timen2 = None
            if timen2 == None:
                navdata = navtemp[linet]
                break
            if timen2 > timen1:
                timeostart = timeo - timen1
                timeoend = timen2 - timeo
                a = 1
            else:       #timen1 > timen2
                timeostart = timeo - timen2
                timeoend = timen1 - timeo
                a = 2
            if timeostart >= timeoend and a == 1:
                navdata = navtemp[linet + 1]
                break
            elif timeoend > timeostart and a == 1:
                navdata = navtemp[linet]
                break
            elif timeostart >= timeoend and a == 2:
                navdata = navtemp[linet]
                break
            elif timeoend > timeostart and a == 2:
                navdata = navtemp[linet + 1]
                break
            linet += 1
        line += 1
        itogcompile = [timeobs[0]]
        itogcompile.extend([timeobs[1], timeobs[2], timeobs[3], timeobs[4], timeobs[5]])
        itogcompile.extend([pseudo])
        linedop = 0
        navdata1 = []
        if ver == 2:
            satnum = satsys + str(int(navdata[0]))
            navdata1.extend([satnum])
            j = 1
            for i in range(len(navdata) - 1):
                navdata1.extend([navdata[j]])
                j += 1
            for i in range(len(navdata1)):
                itogcompile.extend([navdata1[linedop]])
                linedop += 1
        elif ver == 3:
            for i in range(len(navdata)):
                itogcompile.extend([navdata[linedop]])
                linedop += 1
        else:
            continue
        itog.append(itogcompile)
    return(itog)

def deltatime(date, c):
    gps1 = dt.datetime(year = 1980, month = 1, day = 6, hour = 0, minute = 0, second = 0)
    gps2 = dt.datetime(year = 1999, month = 8, day = 21, hour = 0, minute = 0, second = 0)
    gps3 = dt.datetime(year = 2019, month = 4, day = 6, hour = 0, minute = 0, second = 0)
    galileo = dt.datetime(year = 1999, month = 8, day = 22, hour = 0, minute = 0, second = 0)
    beidou = dt.datetime(year = 2006, month = 1, day = 1, hour = 0, minute = 0, second = 0)
    glonass = dt.datetime(year = 2006, month = 1, day = 1, hour = 0, minute = 0, second = 0)
    if 'G' in c:
        if date < gps2 and date < gps3:
            delta = date - gps1
        elif date < gps3 and date > gps2:
            delta = date - gps1
        else:
            delta = date - gps1
    elif 'C' in c:
        delta = date - beidou
    elif 'E' in c:
        delta = date - galileo
    elif 'R' in c:
        delta = date - glonass
    else:
        raise Warning('Нету даты начала отсчета времени')
    g = str(delta)
    g = g.replace(':', ' ')
    g1 = g.split()
    day = int(g1[0])
    hour = int(g1[2])
    minute = int(g1[3])
    second = int(g1[4])
    week = day // 7
    days = day - (week * 7)
    seconds = days * 86400 + hour * 3600 + minute * 60 + second
    return(week, seconds)

def coorsat(week, tobs, P, Crs, dn, M0, Cuc, e, Cus, A12, Toe, Cic, omega0, Cis, i0, Crc, omeg, omegadot, idot, wn, satnum, time):
    c = 299792458
    omegadote = 7.2921151467e-5
    nu = 3.986004418e14
    n0 = math.sqrt(nu/(A12**6))
    tem = tobs - (P/c)
    t = tem - Toe
    if t > 302400:
        t = t - 604800
    elif t < -302400:
        t = t + 604800
    else:
        t = t
    n = n0 + dn
    M = M0 + (n * t)
    E = M - e * math.sin(M)
    b = 0
    a = 1
    while a > 0.0005:
        E1 = E
        E = M - e * math.sin(E)
        a = math.fabs(E - E1)
        b += 1
        #if b == 500:
            #break
    v = 2 * math.atan(math.tan(E / 2) * math.sqrt((1 + e) / (1 - e)))
    fi = v + omeg
    si_u = Cus * math.sin(2 * fi) + Cuc * math.cos(2 * fi)
    si_r = Crs * math.sin(2 * fi) + Crc * math.cos(2 * fi)
    si_i = Cis * math.sin(2 * fi) + Cic * math.cos(2 * fi)
    u = fi + si_u
    r = A12 * A12 * (1 - e * math.cos(E)) + si_r
    i = i0 + si_i + idot * t
    Xorb = r * math.cos(u)
    Yorb = r * math.sin(u)
    Omega = omega0 + (omegadot - omegadote) * t - (omegadote * Toe)
    x = Xorb * math.cos(Omega) - Yorb * math.cos(i) * math.sin(Omega)
    y = Xorb * math.sin(Omega) + Yorb * math.cos(i) * math.cos(Omega)
    z = Yorb * math.sin(i)
    return(x, y, z, satnum, time)

def absolute(data):
    line = 0
    coorsper = []
    for i in range(len(data)):
        date = dt.datetime(year = data[line][0], month = data[line][1], day = data[line][2],
                           hour = data[line][3], minute = data[line][4], second = int(data[line][5]))
        week, tobs = deltatime(date, data[line][7])
        if 'G' in data[line][7]:
            P, Crs, dn, M0 = data[line][6], data[line][18], data[line][19], data[line][20]
            Cuc, e, Cus, A12 = data[line][21], data[line][22], data[line][23], data[line][24]
            Toe, Cic, omega0, Cis = data[line][25], data[line][26], data[line][27], data[line][28]
            i0, Crc, omeg, omegadot = data[line][29], data[line][30], data[line][31], data[line][32]
            idot, wn = data[line][33], data[line][35]
            dT = data[line][14]
            satnum = data[line][7]
        else:
            # P, Crs, dn, M0 = data[line][8], data[line][20], data[line][21], data[line][22]
            # Cuc, e, Cus, A12 = data[line][23], data[line][24], data[line][25], data[line][26]
            # Toe, Cic, omega0, Cis = data[line][27], data[line][28], data[line][29], data[line][30]
            # i0, Crc, omeg, omegadot = data[line][31], data[line][32], data[line][33], data[line][34]
            # idot, wn = data[line][35], data[line][37]
            # dT = data[line][16]
            line += 1
            continue
        xsat, ysat, zsat, satnumber, time = coorsat(week, tobs, P, Crs, dn, M0, Cuc, e, Cus, A12, Toe, Cic, omega0, Cis, i0, Crc, omeg, omegadot, idot, wn, satnum, data[line][0:6])
        pom = [xsat, ysat, zsat, dT, P, satnum]
        pom.extend(data[line][0:6])
        coorsper.append(pom)
        line += 1
    line = 0
    c = 299792458
    a = 6378137
    b = 6356752
    xrms = 0
    yrms = 0
    zrms = 0
    n = 0
    coor = []
    for i in range(len(coorsper)):
        massive = []
        date1 = dt.datetime(year = coorsper[line][6], month = coorsper[line][7], day = coorsper[line][8],
                           hour = coorsper[line][9], minute = coorsper[line][10], second = int(coorsper[line][11]))
        try:
            date2 = dt.datetime(year=coorsper[line + 3][6], month=coorsper[line + 3][7], day=coorsper[line + 3][8],
                                hour=coorsper[line + 3][9], minute=coorsper[line + 3][10], second= int(coorsper[line + 3][11]))
        except:
            break
        satnum1 = coorsper[line][5]
        satnum2 = coorsper[line + 1][5]
        satnum3 = coorsper[line + 2][5]
        satnum4 = coorsper[line + 3][5]
        satnum = [satnum1, satnum2, satnum3, satnum4]
        if date1 == date2 and len(set(satnum)) == 4:
            linet = line
            for i in range(4):
                a1 = [coorsper[linet][0], coorsper[linet][1], coorsper[linet][2], coorsper[linet][3], coorsper[linet][4]]
                massive.append(a1)
                linet += 1
        else:
            line += 1
            continue
        linev = 0
        massigma = []
        masdelta = []
        masA = []
        for i in range(3):
            P1 = massive[linev][4] + (c * massive[linev][3])
            P2 = massive[linev + 1][4] + (c * massive[linev + 1][3])
            dP = P2 - P1
            sP = P2 + P1
            dX = massive[linev + 1][0] - massive[linev][0]
            sX = massive[linev + 1][0] + massive[linev][0]
            dY = massive[linev + 1][1] - massive[linev][1]
            sY = massive[linev + 1][1] + massive[linev][1]
            dZ = massive[linev + 1][2] - massive[linev][2]
            sZ = massive[linev + 1][2] + massive[linev][2]
            A = (dX * sX + dY * sY + dZ * sZ - dP * sP)/2
            q1 = [sX, sY, sZ, sP]
            q2 = [dX, dY, dZ, dP]
            massigma.append(q1)
            masdelta.append(q2)
            masA.append(A)
            linev += 1
        Dd = np.array([[masdelta[0][0], masdelta[0][1], masdelta[0][2]],
                       [masdelta[1][0], masdelta[1][1], masdelta[1][2]],
                       [masdelta[2][0], masdelta[2][1], masdelta[2][2]]], dtype= np.float64)
        D1d = np.array([[masA[0], masdelta[0][1], masdelta[0][2]],
                        [masA[1], masdelta[1][1], masdelta[1][2]],
                        [masA[2], masdelta[2][1], masdelta[2][2]]], dtype= np.float64)
        D2d = np.array([[masdelta[0][0], masA[0], masdelta[0][2]],
                        [masdelta[1][0], masA[1], masdelta[1][2]],
                        [masdelta[2][0], masA[2], masdelta[2][2]]], dtype= np.float64)
        D3d = np.array([[masdelta[0][0], masdelta[0][1], masA[0]],
                        [masdelta[1][0], masdelta[1][1], masA[1]],
                        [masdelta[2][0], masdelta[2][1], masA[2]]], dtype= np.float64)
        d1d = np.array([[-masdelta[0][3], masdelta[0][1], masdelta[0][2]],
                        [-masdelta[1][3], masdelta[1][1], masdelta[1][2]],
                        [-masdelta[2][3], masdelta[2][1], masdelta[2][2]]], dtype= np.float64)
        d2d = np.array([[masdelta[0][0], -masdelta[0][3], masdelta[0][2]],
                        [masdelta[1][0], -masdelta[1][3], masdelta[1][2]],
                        [masdelta[2][0], -masdelta[2][3], masdelta[2][2]]], dtype= np.float64)
        d3d = np.array([[masdelta[0][0], masdelta[0][1], -masdelta[0][3]],
                        [masdelta[1][0], masdelta[1][1], -masdelta[1][3]],
                        [masdelta[2][0], masdelta[2][1], -masdelta[2][3]]], dtype= np.float64)
        D = la.det(Dd)
        D1 = la.det(D1d)
        D2 = la.det(D2d)
        D3 = la.det(D3d)
        d1 = la.det(d1d)
        d2 = la.det(d2d)
        d3 = la.det(d3d)
        Xsh = D1/D
        Ysh = D2/D
        Zsh = D3/D
        ax = d1/D
        ay = d2/D
        az = d3/D
        dX4 = massive[3][0] - Xsh
        dY4 = massive[3][1] - Ysh
        dZ4 = massive[3][2] - Zsh
        a4 = 1 - ax ** 2 - ay ** 2 - az ** 2
        P4 = massive[3][4] + (c * massive[3][3])
        b4 = P4 + dX4 * ax + dY4 * ay + dZ4 * az
        c4 = P4 ** 2 - dX4 ** 2 - dY4 ** 2 - dZ4 ** 2
        b42 = (2 * b4) ** 2
        Disc = b42 - 4 * a4 * c4
        try:
            Disqrt = math.sqrt(Disc)
        except:
            line += 1
            continue
        e1 = (-(2 * b4) - Disqrt)/(2 * a4)
        e2 = (-(2 * b4) + Disqrt)/(2 * a4)
        dt1 = e1/c
        dt2 = e2/c
        if dt1 > -0.0005 and dt2 < 0.0005:
            ep = e1
        else:
            if math.fabs(e1) > math.fabs(e2):
                ep = e2
            else:
                ep = e1
        X = Xsh + ep * ax
        Y = Ysh + ep * ay
        Z = Zsh + ep * az
        co = [X, Y, Z]
        xrms += X
        yrms += Y
        zrms += Z
        n += 1
        coor.append(co)
        line += 1
    Xtrue = xrms/n
    Ytrue = yrms/n
    Ztrue = zrms/n
    e_2 = (a ** 2 - b ** 2) / a ** 2
    e_2s = (a ** 2 - b ** 2) / b ** 2
    lu = math.atan(Ytrue / Xtrue)
    lu = math.degrees(lu)
    tau = math.atan((a * Ztrue) / (b * math.sqrt(Xtrue ** 2 + Ytrue ** 2)))
    taus = math.sin(tau)
    tauc = math.cos(tau)
    fi = math.atan((Ztrue + e_2s * b * taus ** 3) / (math.sqrt(Xtrue ** 2 + Ytrue ** 2) - e_2 * a * tauc ** 3))
    fi = math.degrees(fi)
    #print(coor)
    print(fi, lu)
    return(Xtrue, Ytrue, Ztrue, coor, fi, lu)

def getsp3(file, date, directory = os.getcwd()):
    test = 1
    return test