import os
import struct
from itertools import cycle
from tkinter import filedialog
from math import floor

txt_file = ""
txt_file=filedialog.askopenfilename(initialdir=os.getcwd(), title="Choose TXT File" ,filetype=(('TXT file', '*.txt'),("ALL file",'*.*')))

if len(txt_file) != 0:
    txt_open = open(txt_file, "r")
    story_data= txt_open.readlines()
    txt_open.close()

    i=len(txt_file)- 1
    short_name_file = ""
    while i!= 0 and txt_file[i] != '.':
        i -= 1
    i -= 1
    while i!= 0 and txt_file[i] != '/':
        short_name_file = txt_file[i] + short_name_file
        i -= 1

    ROM_file = ""
    ROM_file=filedialog.askopenfilename(initialdir=os.getcwd(), title="Choose ROM File" ,filetype=(('SMS file', '*.sms'), ('BIN file', '*.bin'),("ALL file",'*.*')))

    if len(ROM_file) != 0:
        ROM_open = open(ROM_file, "rb")
        ROM_data = ROM_open.read()
        ROM_open.close()

        data_bin = bytearray()
        new_pointer = [19749]
        line_usage = []

        centered = ""
        while centered == "":
            centered = str(input("Cenetering text? (y/n)")).lower()
            if centered != "y" and centered != "n" :
                centered = ""

        c_lines = 0
        for n in range (0, len(story_data)):
            story_data[n] = story_data[n][:-1]
            if story_data[n] == "@":
                line_usage.append(c_lines)
                c_lines = 0
            else:
                c_lines += 2
        line_usage.append(c_lines)

        z = 0
        h_num = floor((24 - line_usage[z]) / 2)
        for n in range (0, len(story_data)):
            if story_data[n] == "@":
                data_bin += b'@'
                new_pointer.append(new_pointer[0] + len(data_bin))
                z += 1
                h_num = floor((24 - line_usage[z]) / 2)
            else:
                if story_data[n] == "":
                    h_num += 2
                else:
                    data_bin += b'\x01' + struct.pack("B", h_num)
                    if centered == "y":
                        data_bin += int((30 - len(story_data[n])) / 2) * b' '
                    for o in range(0,len(story_data[n])):
                        if story_data[n][o] == "'" :
                            data_bin += b'('
                        else:
                            data_bin += bytes(story_data[n][o].upper().encode("utf-8"))
                    h_num += 2
                    if n != len(story_data)-1:
                        if story_data[n+1] != "@":
                            data_bin += b'&'
        
        if len(data_bin) < 586:
            data_bin += b'@'
            data_bin += bytes(585 - len(data_bin))

        out_file = open(short_name_file + " Bin Data.bin", "wb+")
        out_file.write(data_bin)
        out_file.close()

        print("Bin Data Done")

        if len(data_bin) <= 585 :
            
            new_ROM_data = ROM_data[:19749] + data_bin + ROM_data[20334:]

            new_ROM_data = new_ROM_data[:20565] + struct.pack("<L", new_pointer[1])[:2] + new_ROM_data[20567:]
            new_ROM_data = new_ROM_data[:20620] + struct.pack("<L", new_pointer[2])[:2] + new_ROM_data[20622:]

            out_file = open("Taz-Mania SMS MOD + " + short_name_file + ".sms", "wb+")
            out_file.write(new_ROM_data)
            out_file.close()

            print("New ROM File Done")
        
        else:
            print("Thus you can't add it in the ROM but have a bin file!")
        
    else:
        print("No ROM file selected")

else:
    print("No file choosen")
