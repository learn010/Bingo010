# import modules
import sys
from random import randint
from time import sleep
from gtts import gTTS
from playsound import playsound

# Set variables
Getrokken = []
bal = ''
first = True
answer = "p"


# yes no validator
def validyesno(question):
    global answer
    speech(question)
    answer = input().upper()
    if answer == "J" or answer == "N":
        return answer
    else:
        speech('Dat is geen geldig antwoord')
        return validyesno(question)


def validatethree(options, a, b, c, ):
    global val3
    speech(options)
    val3 = input().upper()
    if val3 == a or val3 == b or val3 == c:
        return val3
    else:
        speech(f"Dat is niet een van de opties, kies {a}, {b}, of {c}")
        validatethree(options, a, b, c)


# welkom wanna play
def beginnen():
    global answer
    speech('Hallo.')
    validyesno('Wil je bingo spelen?')
    if answer == 'J':
        start()
    else:
        dag()


# start and first 5 numbers are selected
def start():
    global Getrokken
    speech('Ok! Daar gaan we. \nIk heb er heel veel zin in, ik hoop jij ook.')
    sleep(.5)
    speech('Daar komt het eerste nummer! SPANNEND!')
    ball = randint(1, 76)
    sleep(1)
    eerste = 'Het eerste getal is: '
    speech(eerste + str(ball))
    Getrokken.append(ball)
    sleep(.2)
    speech('Ik trek gelijk nog vier getallen, om op gang te komen')
    sleep(.2)
    for i in range(1, 5):
        trekking()
    again()


# exit goodbye
def dag():
    speech('ok doei')
    sys.exit()


# select number
def trekking():
    global Getrokken
    global bal
    bal = randint(1, 76)
    if bal in Getrokken:  # check if the number is selected before
        trekking()
    else:
        show()


# print and speech out of the number with a announcement from list from txt file
def show():
    global bal
    global Getrokken
    trek_tekst = open('resources/trekking_tekst.txt', 'r').readlines()
    aant_tekst = int(len(trek_tekst)) - 1
    mix = randint(0, aant_tekst)
    sleep(1)
    string = trek_tekst[mix]
    string = string.rstrip('\n')
    output = f"{string} {str(bal)} "
    speech(output)
    Getrokken.append(bal)
    while len(Getrokken) <= 5:  # quick exit for the first 5 selections
        break
    else:
        again()


# ask for next number or claim bingo
def again():
    global first
    while first:
        first = False
        validatethree(
            'Na elk getrokken nummer heb je 3 opties \n(B) Bingo \n(N) voor een nieuw nummer of \n(Q) Stoppen ', 'B',
            'N', "Q")
        if val3 == 'B':
            controle()
        elif val3 == 'N':
            trekking()
        else:
            dag()
    else:
        validatethree('B,N of Q?', 'B', 'N', 'Q')
        if val3 == 'B':
            controle()
        elif val3 == 'N':
            trekking()
        else:
            dag()


# check if claimed bingo is valid, by printing the list sorted
def controle():
    global Getrokken
    Getrokken.sort()
    speech('Bingo!, Bingo?, laten we dat even controleren.')
    sleep(.3)
    speech('tot nu toe, zijn de volgende nummers gevallen:')
    speech(str(Getrokken))
    sleep(3)
    validyesno('En? is het bingo?')
    if answer == "N":  # If bingo is not valid, generate a childrens song from the list
        speech('Dat wordt een liedje zingen')
        liedjes = open('resources/liedjes_lijst.txt', 'r').readlines()
        aant_lied = int(len(liedjes)) - 1
        mix = randint(0, aant_lied)
        sleep(2)
        speech('En het liedje dat we willen horen is...')
        speech(liedjes[mix])
        sleep(1)
        speech('Druk op enter om verder te gaan, en het volgende nummer te trekken.')
        input()
        trekking()
    elif answer == "J":
        bingo()
    else:
        speech('Dit kan niet kloppen')


# Bingo, wanna go again
def bingo():
    global Getrokken
    print('''
    ░░░░░░╔══╗░░░░░░░░░░╔╗░░░░░░░░░░░░░░░░░░
    ░░░░░░║╔╗║░░░░░░░░░░║║░░░░░░░░░░░░░░░░░░
    ░░░░░░║╚╝╚╦╦═╗╔══╦══╣║░░░░░░░░░░░░░░░░░░
    ░░░░░░║╔═╗╠╣╔╗╣╔╗║╔╗╠╝░░░░░░░░░░░░░░░░░░
    ░░░░░░║╚═╝║║║║║╚╝║╚╝╠╗░░░░░░░░░░░░░░░░░░
    ░░░░░░╚═══╩╩╝╚╩═╗╠══╩╝░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░╔═╝║░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░╚══╝░░░░░░░░░░░░░░░░░░░░░░
    ''')
    speech('BINGO!!!')
    sleep(5)
    validyesno('wil je nog een keer spelen? (j/n)')
    if answer == "J":
        sleep(1)
        start()
        Getrokken = []
    else:
        dag()


# text to speech function
def speech(quote='geen invoer'):
    print(quote)
    output = gTTS(text=quote, lang='nl', slow=False)
    output.save("resources/audio.mp3")
    playsound('resources/audio.mp3')


beginnen()
