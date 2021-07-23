import PySimpleGUI as sg
import time
from codemap import CODE_MAP
from images import LOGO, play_btn_base64
from playsound import playsound


def morse(char):
    """ Takes a '.' or '-' and plays the dit or dah sound"""

    if char == '.':
        playsound('sounds/dit.wav')
        time.sleep(0.0005)
    elif char == '-':
        playsound('sounds/dah.wav')
        time.sleep(0.0005)
    elif char == '|':
        time.sleep(0.5)


def to_morse_code(text):
    """ Takes a character or a text and converts to the equivalent morse code. Uses the CODE_MAP dict"""

    translated_text = ''
    for char in text:
        if char in CODE_MAP:
            morse_code = CODE_MAP[char]
            translated_text += morse_code + ' '

    return translated_text


def to_text(code):
    """ Takes a '.' or '-' or a series or those characters and converts it to the equivalent english letter
    or word"""

    decoded = ''
    if ' ' in code:
        text_list = []
        morse_code_list = code.split(' ')
        for morse_code in morse_code_list:
            for key, value in CODE_MAP.items():
                if morse_code == value:
                    text_list.append(key)
        return ''.join(text_list)

# text = input('Type your text: ').upper()


def main():
    sg.theme('DarkGray9')
    layout = [[
              sg.Col([
                    [sg.Image(data=LOGO, size=(500, 150))],
                    [sg.Text('Text', size=(10, 1), justification='center'),
                     sg.Input(key='-TEXT-', enable_events=True)],
                    [sg.Text('Morse Code', size=(10, 1), justification='center'),
                     sg.Input(key='-MORSE_CODE-', enable_events=True)],
                    [sg.Text('*For Morse-to-Text, use spaces to separate letters and "|" to separate words',
                             justification='center', font=('mono', 8))],
                    [sg.Radio('Text-to-Morse     ', "RADIO1", key='rad1', default=True),
                     sg.Radio('Morse-to-Text            ', "RADIO1", key='rad2'),
                     sg.Button(image_data=play_btn_base64,
                               button_color=(sg.theme_background_color(), sg.theme_background_color()),
                               border_width=0, key='Play')
                     ]]),
              ]]

    window = sg.Window('Translator', layout, no_titlebar=False, grab_anywhere=True)

    output_code = ''
    while True:  # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if values['rad1']:
            if values['-TEXT-']:
                # Update the "output" text element to be the value of "input" element
                text = values['-TEXT-'].upper()
                output_code = to_morse_code(text)
                window['-MORSE_CODE-'].update(output_code)

        if values['rad2']:
            if values['-MORSE_CODE-']:
                # Update the "output" text element to be the value of "input" element
                output_code = to_text(values['-MORSE_CODE-'])
                window['-TEXT-'].update(output_code)

        if event in 'Play':
            # make sure output_code is in morse code
            text = values['-TEXT-'].upper() if window['-TEXT-'] else ''
            output_code = to_morse_code(text)
            time.sleep(1)
            # play sound
            for _ in output_code:
                morse(_)
    window.close()


if __name__ == '__main__':
    main()
