#Project Sangee

#pip install pyaudio, SpeechRecognition,gTTS, wikipedia

#Import
import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

# Ignore any warning  messages
warnings.filterwarnings('ignore')

# record audio and return it as a string
def recordAudio():

    #Record the audio
    r = sr.Recognizer() #Creating a recognizer object


    with sr.Microphone() as source:
        print('Say something!')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration = 1)
        audio = r.listen(source)

#    #Use Google's speech recognition
    data = ''
    try:
        data = r.recognize_google(audio, language = "en-IN")
        print('You said: '+ data + '/n')
    except sr.UnknownValueError: #Check for unknown errors
        print('Google Speech Recognition could not understand the audio, unknown error')
    except sr.RequestError as e:
        print('Request results from Google Speech Recognition service error '+e)

    return data
# A Function to get  the VA response
def assistantResponse(text):

    print(text)
    # convert text to speech
    myobj = gTTS(text= text, lang='en', slow=False)

    #save as audio
    myobj.save('assistant_response.mp3')

    #play
    os.system('start assistant_response.mp3')

# Wake word
def wakeWord(text):
    WAKE_WORDS = ['sangee', 'sangi']

    text = text.lower() #convert text to lower

    #check to see if the users wakeword

    for phrase in WAKE_WORDS:
        if phrase in text:
            return True

    return False

#to get date
def getDate():

    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day

    # Months list
    month_names = ['January','February', 'March', 'April', 'May', 'June', 'July',
                   'August','September', 'October', 'November', 'December']

    #Numbers list
    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th',
    '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd',
    '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']

    return 'Today is '+weekday+' '+ month_names[monthNum - 1]+' the '+ordinalNumbers[dayNum -1]+'.'


print(getDate())

#A function to greet random response
def greeting(text):

    #greeting inputs
    GREETING_INPUTS = ['hi', 'hey', 'hola', 'greetings', 'wassup', 'hello ']

    #Greet Responses
    GREETING_RESPONSES = ['howdy', 'whats good', 'hello', 'hey there']
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'

    return ''

# First and last name split
def getPerson(text):

    wordList = text.split()
    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i+1].lower() == 'is':
            return wordList[i+2] + ' '+ wordList[i+3]


while True:
        #record Audio
    text = recordAudio()
    response = ''

    #Wake word check
    if(wakeWord(text) == True):

        #check greetigs
        response = response + greeting(text)

        #Check date
        if('date' in text):
            get_date = getDate()
            response = response + ' ' +get_date

        #check time
        if('time' in text):
            now = datetime.datetime.now()
            meridiem =' '
            if now.hour >=12:
                meridiem = 'p.m'
                hour = now.hour - 12
            else:
                meridiem = 'a.m'
                hour = now.hour

            #convert minute
            if now.minute < 10:
                minute= '0' + str(now.minute)
            else:
                minute = str(now.minute)

            response = response + ' '+ 'It is '+ str(hour)+ ':'+ minute+ ' '+meridiem + ' .'

        #Check 'who is'
        if('who is' in text):

            person = getPerson(text)
            wiki = wikipedia.summary(person)
            response = response + ' '+ wiki

        #Have the assistant respond back using audio and text from response
        assistantResponse(response)
