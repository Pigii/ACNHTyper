import socket
import time


dc = [90, 415]  # default coordinates
dca = [95, 55]  # default coordinates advancement
usloc = "1234567890-qwertyuiop/asdfghjkl:'zxcvbnm,.?!aaaaaa     "  # us list of chars
uslocc = "#[]$%^&*()_QWERTYUIOP@ASDFGHJKL;\"ZXCVBNM<>+=aaaaaa     "  # us list of chars CAPITAL
uslocs = "1234567890-!@#$%^&*()_~`=\\+{}|[]a<>;:\"',.?/aaaaaaa     "  # us list of chars symbols
maxn = 16  # 16 is the max that the chat can handle if you put the biggest char. for example 24 is the max if you use no
# rmal sized chars. if someone is able to calculate this in some way please point it out.s


def sendCommand(switch, content):
    content += '\r\n'  # important for the parser on the switch side
    switch.sendall(content.encode())


def split(word):
    return [char for char in word]


def mainstuff(phrase, coordadv, defcoord):
    n = []
    dcclist = []
    uslocaaal = split(usloc)  # us list of chars as an actual list
    usloccaaal = split(uslocc)  # us list of chars CAPITAL as an actual list
    uslocsaaal = split(uslocs)  # us list of chars symbols as an actual list
    splitted = split(phrase)  # separates every letter
    for char in splitted:  # for every letter
        try:
            n.append(uslocaaal.index(char))  # add the placement number of the letter in n
        except ValueError:
            try:
                usloccaaal.index(char)
                n.append(45)
                n.append(usloccaaal.index(char))
            except ValueError:
                n.append(47)
                n.append(uslocsaaal.index(char))
                n.append(46)
    for number in n:  # for every number in n
        column = defcoord[1]
        row = defcoord[0]
        for i in range(int(number / 11)):  # if number is multiple of 11
            column += coordadv[1]  # count the row that the letter is in
        if number >= 11:
            temp = number - 11 * int(number / 11)
        else:
            temp = number
        for p in range(temp):
            row += coordadv[0]
        # print(f"columns {int(number / 11)} | rows {temp}")
        dcclist.append(row)
        dcclist.append(column)
    return dcclist


def send(switch, positions):
    sendCommand(switch, "click R")
    time.sleep(.7)
    for i in range(0, len(positions), 2):
        sendCommand(switch, "touch " + '{0} {1}'.format(positions[i], positions[i + 1]))
    sendCommand(switch, "click PLUS")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.203", 6000))
sendCommand(s, "configure pollRate 50")

while True:
    inp = input("Things you want to write:  ")
    inputs = [inp[i:i + maxn] for i in range(0, len(inp), maxn)]
    poopcode = 0
    for inp in inputs:
        poopcode += 1
        dcc = mainstuff(inp, dca, dc)
        send(s, dcc)
        sendCommand(s, "click PLUS")
        if not len(inputs) == 1 and not poopcode == len(inputs):
            time.sleep(2.8)
