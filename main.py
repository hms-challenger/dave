import os
import shutil
from converter import *
import PySimpleGUI as sg
import openpyxl
import csv
from itertools import zip_longest
import ftplib
# import getpass
from ftplib import FTP_TLS
from config import FTP_HOST, FTP_USER, FTP_PASS


sg.theme('BrownBlue')

folderToTracklist = os.path.join(os.path.join(os.path.expanduser('~')), 'Downloads')
desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

link = []
song = []
klasse = []

# gui layout
layout = [  [sg.Text('Pfad MIXFERTIG:')],
            [sg.Input(), sg.FolderBrowse('Browse', key='-dirNAS-', initial_folder=desktop, s=10)],
            [sg.Text('Schul-ID:')],
            [sg.InputText(key='-schoolID-')],
            [sg.Text('Schul-Name:')],
            [sg.InputText(key='-schoolName-')],
            [sg.Text('Pfad TRACKLIST ADMINTOOL:')], 
            [sg.Input(), sg.FileBrowse('Browse', key='-dirTL-', initial_folder=folderToTracklist, s=10)],
            [sg.Button('OK!', key="-START-", s=15), sg.Button('Cancel', s=15)] ]

window = sg.Window('DAVE', layout)

with open(("./dave_logo.txt"), 'r') as f:
    file_content = f.read()
    print(file_content,"\nWaiting for input...")

while True:
    event, values = window.read()

    dirNAS = values['-dirNAS-']
    schoolID = values['-schoolID-']
    schoolName = values['-schoolName-']
    tracklist = values['-dirTL-']
    cache_folder = desktop + "/cache_MM" + schoolID

    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        print("abort. see you next time!")
        break

    dirNAS = values['-dirNAS-']
    if dirNAS == "":
        print('Kein Pfad -> MIXFERTIG!')

    schoolID = values['-schoolID-']
    try:
        schoolID == int(schoolID)
        if schoolID == "":
            print('Keine Schul-ID!')
    except:
        print("Schul-ID kann nicht gelesen werden")

    schoolName = values['-schoolName-']
    if schoolName == "":
        print("Kein Schulname!")

    tracklist = values['-dirTL-']
    if tracklist == "":
            print('Keine Pfad -> Tracklist!')

    if event == '-START-' and dirNAS != "" and schoolID != "" and tracklist != "":

        try:
            print("Connecting to minimusiker ftp server!") 
            ftp = FTP_TLS(FTP_HOST, timeout=5)
            # passwd = getpass("Enter your password: ")
            ftp.login(FTP_USER, FTP_PASS)
            ftp.prot_p()  
            ftp.encoding = "utf-8"
            ftp.cwd("htdocs/hoerthin/mp3")
            print("Connection success! Directory: htdocs/hoerthin/mp3")
        except ftplib.all_errors as e:
            print('FTP error:', e)

        # # create cache folder on desktop with cache_schoolID
        try:
            os.mkdir(cache_folder)
        except OSError:
            print(cache_folder, "konnte nicht erstellt werden!")

        # # copy wav files to cache folder on desktop
        try:
            for file in os.listdir(dirNAS):
                if file.endswith(".wav") == True:
                    wav_file = dirNAS + "/" + file
                    shutil.copy(wav_file, cache_folder)       
        except:
            print("kein pfad vorhanden")

        print("\n-------------------------------------------------------------")
        print("wav check!!!")
        print("waiting for user input ...")
        print("-------------------------------------------------------------\n")
        userInput = input("go? [yes|no] ")

        if userInput == "no" or userInput == "No" or userInput == "NO" or userInput == "n":
            # # delete cache Folder 
            try:
                shutil.rmtree(cache_folder)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
            print("cache_folder on desktop deleted. see you next time!")
            break

        elif userInput == "yes" or userInput == "Yes" or userInput == "YES" or userInput == "y":
            # # Convert wav to mp3
            conv = mp3_converter(cache_folder, ".wav", "mp3")
            conv.lower_underscore()
            conv.mp3()

            # # Rename mp3s in cache_schoolID and move to /mp3
            mp3_folder = cache_folder + "/mp3"
            if not os.path.exists(mp3_folder):
                os.makedirs(mp3_folder)
            for filename in os.listdir(cache_folder):
                if (filename.endswith(".mp3")):
                    source = os.path.join(cache_folder, filename)
                    shutil.move(source, mp3_folder)
            os.listdir(mp3_folder)
            for f in os.listdir(mp3_folder):
                os.rename(os.path.join(mp3_folder, f), os.path.join(mp3_folder, f).replace('§', ' ').title().replace('.Mp3', '.mp3'))

            # # Rename wavs in cache_schoolID and move to /wav
            wav_folder = cache_folder + "/wav"
            if not os.path.exists(wav_folder):
                os.makedirs(wav_folder)
            for filename in os.listdir(cache_folder):
                if (filename.endswith(".wav")):
                    source = os.path.join(cache_folder, filename)
                    shutil.move(source, wav_folder)
            os.listdir(wav_folder)
            for f in os.listdir(wav_folder):
                os.rename(os.path.join(wav_folder, f), os.path.join(wav_folder, f).replace('§', ' ').title().replace('.Wav', '.wav'))

            # # zip mp3 files
            os.path.join(mp3_folder, shutil.make_archive("AlleLieder", 'zip', mp3_folder))
            shutil.move(("./AlleLieder.zip"), mp3_folder)

            # # build csv and txt with links to upload to dropbox
            while True:
                lines = os.listdir(mp3_folder)
                for mp3s in lines:
                    link.append("https://www.hoerthin.de/mp3/" + schoolID + "/" + mp3s.replace(" ", "%20"))
                link.sort()
                for i in song:
                    print(i)

                csvFile = schoolID + "_mp3Liste.csv"

                # # Excel Tabelle Admin-Tool lesen
                excel_file = openpyxl.load_workbook(tracklist)
                sheet_obj = excel_file.active
                m_row = sheet_obj.max_row

                # Tracklist-Daten
                # name = input("schoolID: ")
                txtFile = schoolID + "_tracklist.txt"
                txt_file = open(txtFile, "w")

                j = 1

                for i in range(2, m_row + 1):
                    cell_obj = sheet_obj.cell(row = i, column = 1)
                    song.append(cell_obj.value)
                    cell_obj2 = sheet_obj.cell(row = i, column = 2)
                    klasse.append(cell_obj2.value)
                    try:
                        full_row = str(j).zfill(2) + " " + cell_obj.value + " " + "(" + cell_obj2.value + ")\n" # optional for copy from txt-file, saved in original path
                        txt_file.write(str(full_row)) # write to .txt if 3 columns (titel + (klasse))
                    except:
                        full_row2 = str(j).zfill(2) + " " + cell_obj.value + "\n"
                        txt_file.write(str(full_row2)) # write to .txt if 2 columns (alle kinder singen alle songs)
                    
                    j += 1

                song.append("Alle Lieder")
                klasse.append(" ")
                link.append("https://www.hoerthin.de/mp3/Minimusikersong.mp3")
                song.append("Minimusikersong")
                klasse.append("Minimusiker")

                data = [link, song, klasse]
                export_data = zip_longest(*data, fillvalue = '')
                with open(csvFile, 'w', newline='') as file:
                    write = csv.writer(file)
                    write.writerows(export_data)

                break
            txt_file.close()
            file.close()

            # # upload files to mysql -> file using customer_id(schoolID), event_id
            # soon to come

            # # copy csv and txt files to dropbox
            shutil.move(("./" + txtFile), cache_folder)
            shutil.move(("./" + csvFile), cache_folder)

            # # rename cache_folder+schoolID to schoolID
            for foldername in os.listdir(desktop):
                if foldername.startswith("cache_"):
                    os.rename(os.path.join(desktop, foldername), os.path.join(desktop, foldername).replace(("cache_MM"+schoolID), ("MM"+schoolID+" "+schoolName)))

            # # duplicate full folder to dropbox
            command1 = """ osascript -e '
            set dropboxFolder to "Macintosh HD:Users:minimusiker:Dropbox:Apps:FileTrip_deinecd:Uploads:__Minimusiker - xxx:"
            set desktopFolder to (path to desktop)
            set theFolder to "MM"
            tell application "Finder"
                activate
                set matchingFolder to ((every folder in desktop) whose name begins with theFolder) as text
                duplicate (folder matchingFolder) to dropboxFolder
            end tell
            '"""
            
            os.system(command1)

            # # rename mp3Folder to ftpFolder (mp3 -> 1170)
            base = desktop + "/MM" + str(schoolID) + " " + schoolName
            mp3Folder = base + "/mp3"
            uploadFolder = base + "/" + str(schoolID)
            os.rename(os.path.join(base, mp3Folder), os.path.join(base, schoolID).replace('mp3', schoolID))

            # # upload mp3Folder to ftp server
            print("Creating mp3 folder on ftp server!")
            ftp.mkd(schoolID)
            ftp.cwd(schoolID)

            def uploadThis(uploadFolder):
                files = os.listdir(uploadFolder)
                os.chdir(uploadFolder)
                for f in files:
                    print("Uploading...", f)
                    if os.path.isfile(uploadFolder + r'/{}'.format(f)):
                        fh = open(f, 'rb')
                        ftp.storbinary('STOR %s' % f, fh)
                        fh.close()
                    elif os.path.isdir(uploadFolder + r'/{}'.format(f)):
                        ftp.mkd(f)
                        ftp.cwd(f)
                        uploadThis(uploadFolder + r'/{}'.format(f))
                ftp.cwd('..')
                os.chdir('..')

            uploadThis(uploadFolder)
            ftp.quit()

            # # delete cache Folder 
            try:
                shutil.rmtree(base)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
            print("Job done!")
            break

window.close()