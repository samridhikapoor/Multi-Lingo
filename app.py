from flask import Flask, render_template, jsonify, request
import os
import PyPDF2
from googletrans import Translator
import googletrans
import cv2
import pytesseract
from gtt import nischay


app = Flask(__name__)

#checking if images folder exist 
#if not then make one
if not os.path.isdir(os.path.join(os.getcwd(),'images')):
   os.mkdir(os.path.join(os.getcwd(),'images'))

#setting congfig of tesseract
custom_config = r'--oem 3 --psm 6'

#setting the correct path
#for Windows find it in the Programmne files
#This path is given for heroku dyno
pytesseract.pytesseract.tesseract_cmd = r'/app/.apt/usr/bin/tesseract'

#homepage route
@app.route("/", methods = ['POST', 'GET'])
def front():
    if request.method=='POST':
        #importing text from thr form
        text = request.form['text-to-translate']
        #importing lang from the form
        lang = request.form['select-language']
        #using google trans to convert 
        translator = Translator()
        translated = translator.translate(text,dest=lang)
        text=translated.text
        #calling nischay function 
        #from gtt.py 
        #for converting text to speech and playing it
        nischay(text,lang)
        return render_template('index.html', text=text)
    else:
        return render_template('index.html')


# display route
@app.route("/display", methods=['POST'])
def display():
    #requasting form data
    text=request.form['lan']
    file = request.files['myfile']
    pathOfFile = os.path.join(os.getcwd(), 'images', file.filename)
    file.save(pathOfFile)
    #using PyPDF2 to read pdf
    a=PyPDF2.PdfFileReader(os.path.join(os.getcwd(),'images',file.filename))
    stri=""
    #counting the pages in pdf
    count_page=a.getNumPages()
    if count_page>10:
     for i in range(0,5):
        stri+=a.getPage(i).extractText()
    else:
        for i in range(0,count_page):
         stri+=a.getPage(i).extractText()

    m=text
    #google trans to convert
    translator = Translator()
    translated = translator.translate(stri,dest=m)
    p=translated.text
    app_data={
    "TRANSLATED":p
    }
    #removing the pdf
    os.remove(pathOfFile)
    return render_template('display.html',app_data=app_data)
    

@app.route("/nischay", methods=["POST"])
def img_text():
    #requesting form data
    image=request.files['myfile']
    w=request.form['lan']
    pathofFile = os.path.join(os.getcwd(), 'images', image.filename)
    image.save(pathofFile)
    #using opencv to read the image
    img = cv2.imread(pathofFile)   
    # text in the images converted to text using TESSERACT-OCR
    text=pytesseract.image_to_string(img)
    translator=Translator()
    translation1=translator.translate(text,dest=w)

    app_data={
    "trn":translation1.text
    }
    os.remove(pathofFile)
    return render_template('nischay.html',app_data=app_data)
    
#Running the Flask app
if __name__=="__main__":
    app.run(debug=False)
