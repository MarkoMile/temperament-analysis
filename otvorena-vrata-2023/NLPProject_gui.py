################## IMPORTS & SETUP ##################

import tensorflow as tf
import tldextract
import unicodedata
import re
import numpy as np
import spacy
import tkinter
import customtkinter
import time
from PIL import Image

import os
os.environ["TOKENIZERS_PARALLELISM"] = "true"

nlp = spacy.load('en_core_web_md')

STOP_WORDS = nlp.Defaults.stop_words


def pogodiLicnost():

    try:
        formatted_text = input_text.get()
        global loading
        loading = False
        finishLabelImage.pack(pady=30)
        ################## FORMATIRANJE ##################

        URL_REGEX = r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))"""
        DOMAIN_REGEX = "^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)"
        COMMENT_REGEX = r"\[.*?\]"
        ELLIPSIS_REGEX = r"^(\ *\.{3}\ *)|(\ *\.{3}\ *)$"

        # Funkcije za formatiranje

        def urlReplace(stringToReplace):
            domain = tldextract.extract(stringToReplace.group())
            return domain.domain + '.' + domain.suffix

        def containsOnlyUrlsOrNumbers(post):
            splits = post.split()
            for str in splits:
                if (not re.search(URL_REGEX, str) and not re.search('^\d+$', str) and not re.search('^\.\.\.+$', str)):
                    return 1
            return 0

        def removeEllipsis(post):
            return re.sub(ELLIPSIS_REGEX, '', post)

        def removeWhitespace(post):
            post = " ".join(post.split())
            return post

        def removeAccentedChars(post):
            post = unicodedata.normalize('NFKD', post).encode(
                'ascii', 'ignore').decode('utf-8', 'ignore')
            return post

        def toLower(post):
            post = post.lower()
            return post

        def removeStopWords(post):
            post = " ".join([t for t in post.split() if t not in STOP_WORDS])
            return post

        def removeSpecialChars(post):  # ALSO REMOVES PUNCTUATION
            post = re.sub('[^A-Z a-z 0-9-]+', '', post)
            return post

        def removeAlphaNumeric(post):
            alphaNumRegex = r"\b([A-z]+[0-9]+[A-z0-9]*|[0-9]+[A-z]+[A-z0-9]*)\b"
            post = re.sub(alphaNumRegex, '', post)
            return post

        def removeNumbers(post):
            numberRegex = r"[0-9]+"
            floatRegex = r"([1-9][0-9]*[eE][1-9][0-9]*|(([1-9][0-9]*\.)|(\.[0-9]+))([0-9]*)?([eE][\-\+]?[1-9][0-9]*)?)"
            post = re.sub(floatRegex, '', post)
            post = re.sub(numberRegex, '', post)
            return post

        def shortenRepeatingChars(post):
            # finds character groups of more than 3 consecutive chars
            repeatingCharRegex = r"(.)\1{3,}"
            post = re.sub(repeatingCharRegex, r"\1\1\1", post)
            return post

        def removeSingleChars(post):  # removes free single chars EXCEPT I or i
            singleCharRegex = r"(^| )[^Ii](( )[^Ii])*( |$)"
            post = re.sub(singleCharRegex, '', post)
            return post

        # Formatiranje unetog teksta

        formatted_text = removeWhitespace(formatted_text)
        formatted_text = removeEllipsis(formatted_text)
        formatted_text = removeAccentedChars(formatted_text)
        formatted_text = re.sub(URL_REGEX, urlReplace, formatted_text)
        formatted_text = removeSpecialChars(formatted_text)
        formatted_text = removeStopWords(formatted_text)
        formatted_text = removeAlphaNumeric(formatted_text)
        formatted_text = removeNumbers(formatted_text)
        formatted_text = toLower(formatted_text)
        formatted_text = shortenRepeatingChars(formatted_text)
        formatted_text = removeSingleChars(formatted_text)
        formatted_text = removeWhitespace(formatted_text)

        # Pretvaranje u LEME
        # (nlp tokenization with spaCy)

        def convertToLemmas(post):
            doc = nlp(post)
            lemmaList = []
            for token in doc:
                lemma = str(token.lemma_)
                if lemma == '-PRON-' or lemma == 'be':
                    lemma = token.text
                lemmaList.append(lemma)
            new_post = (" ".join(lemmaList))
            return new_post

        formatted_text = convertToLemmas(formatted_text)

        # Pretvaranje u vektore

        sequence_length = 1703
        max_features = 2000
        oov_token = '<UNK>'
        pad_type = 'post'
        trunc_type = 'post'

        tokenizer = tf.keras.preprocessing.text.Tokenizer(
            num_words=max_features, oov_token=oov_token)
        tokenizer.fit_on_texts([formatted_text])
        word_index = tokenizer.word_index
        vectorList = tokenizer.texts_to_sequences([formatted_text])
        vectorList = tf.keras.utils.pad_sequences(
            vectorList, padding=pad_type, truncating=trunc_type, maxlen=sequence_length, dtype='int32')

        if ((len(formatted_text) > 0)):

            ################## NN PREDIKCIJA ##################
            model = tf.keras.models.load_model('saved_models/fullSet_nospacy')
            predict = model.predict(vectorList)
            print(predict)
            unMappedValue = np.argmax(predict, axis=1)[0]

            match (unMappedValue):
                case 0:
                    mappedValue = "Guardian (ISTJ, ISFJ, ESTJ, ESFJ)"
                    imageValue = image0
                case 1:
                    mappedValue = "Artisan (ISTP, ISFP, ESTP, ESFP)"
                    imageValue = image1
                case 2:
                    mappedValue = "Idealist (INFJ, INFP, ENFP, ENFJ)"
                    imageValue = image2
                case 3:
                    mappedValue = "Rationalist (INTJ, INTP, ENTP, ENTJ)"
                    imageValue = image3
                case _:
                    mappedValue = "error"
                    imageValue = errorImage


            finishLabel.configure(
                text="Success! I have guessed your personality type:", text_color="green")
            finishLabelType.configure(text=mappedValue, text_color="black")
            finishLabelImage.configure(image=imageValue)

        else:
            mappedValue = "error"
            imageValue = errorImage
            finishLabel.configure(
                text="Uh oh, you have to insert text!", text_color="red")
            finishLabelImage.configure(image=imageValue)
    except:
        finishLabel.configure(
            text="Uh oh, an error occured.", text_color="red")
        finishLabelType.configure(text="", text_color="black")
        finishLabelImage.configure(image=imageValue)
        print("doslo je do greske; lele")


def loadingEffect():
    global loading
    loading = True
    finishLabelImage.pack_forget()
    finishLabel.configure(text="")
    finishLabelType.configure(text="")
    app.after(0, update, 0)
    app.after(1000, pogodiLicnost)

################## TKINTER ##################


# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("720x580")
app.resizable(False, False)
app.title("Personality classification program")

# CTk variables
my_font_normal = customtkinter.CTkFont(family="Roboto", size=16)
my_font_big = customtkinter.CTkFont(family="Roboto", size=22, weight='bold')

# Images
image0 = customtkinter.CTkImage(
    light_image=Image.open("./imgs/sentinel-SVG.png"), dark_image=Image.open("./imgs/sentinel-SVG.png"), size=(640, 200))
image1 = customtkinter.CTkImage(
    light_image=Image.open("./imgs/explorer-SVG.png"), dark_image=Image.open("./imgs/explorer-SVG.png"), size=(640, 200))
image2 = customtkinter.CTkImage(
    light_image=Image.open("./imgs/diplomat-SVG.png"), dark_image=Image.open("./imgs/diplomat-SVG.png"), size=(640, 200))
image3 = customtkinter.CTkImage(
    light_image=Image.open("./imgs/analyst-SVG.png"), dark_image=Image.open("./imgs/analyst-SVG.png"), size=(640, 200))
errorImage = customtkinter.CTkImage(
    light_image=Image.open("./imgs/error.png"), dark_image=Image.open("./imgs/error.png"), size=(600*0.5, 450*0.5))


# UI elements

# loading Gif
loading = False

frameCnt = 39
frames = [tkinter.PhotoImage(file='./imgs/loading-transparent.gif', format='gif -index %i' % (i))
          for i in range(frameCnt)]


def update(ind):
    global loading
    if (loading):
        finishLabelLoading.place(x=280, y=290)
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        finishLabelLoading.configure(image=frame)
        app.after(25, update, ind)
    else:
        finishLabelLoading.place_forget()


app.after(0, update, 0)

# 16personalities image
logoImage = customtkinter.CTkImage(
    light_image=Image.open("./imgs/16Personalities.png"), dark_image=Image.open("./imgs/16Personalities.png"), size=(244, 50))
# Keirsey image
logoImage1 = customtkinter.CTkImage(
    light_image=Image.open("./imgs/keirsey.png"), dark_image=Image.open("./imgs/keirsey.png"), size=(163, 50))


logoLabelImage = customtkinter.CTkLabel(
    app, text="", image=logoImage)
logoLabelImage.pack(anchor="w",pady=10,padx=10)
logoLabelImage1 = customtkinter.CTkLabel(
    app, text="", image=logoImage1)
logoLabelImage1.place(x=720-170,y=10)

# Label
title = customtkinter.CTkLabel(app, text="Insert some text:")
title.pack(padx=10, pady=10)
# String input
input_text = tkinter.StringVar()
input = customtkinter.CTkEntry(
    app, width=600, height=40, textvariable=input_text, justify="center")
input.pack()
# Button
button = customtkinter.CTkButton(
    app, text="Guess my personality type!", command=loadingEffect)
button.pack(padx=10, pady=10)
# Zavrsio predvidjanje
finishLabel = customtkinter.CTkLabel(
    app, text="", font=my_font_normal, height=40, anchor="s")
finishLabel.pack()
finishLabelType = customtkinter.CTkLabel(app, text="", font=my_font_big)
finishLabelType.pack()
finishLabelLoading = customtkinter.CTkLabel(
    app, text="", font=my_font_big, image=frames[2])
finishLabelLoading.place(x=280, y=290)
finishLabelImage = customtkinter.CTkLabel(app, text="")
finishLabelImage.pack(pady=30)

# Run app
app.mainloop()
