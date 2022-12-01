import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog


#functions:

def DecToBin8 (nombre):
    return format(nombre,'08b')

def DecToBin16 (nombre):
    B = '{0:016b}'.format(nombre)
    return B

def AfficheImage():

    cv2.imshow("imageA", imgA)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def Recepteur():
    global imgA
    #convertir imgA en YCbCr
    imgA = cv2.cvtColor(imgA, cv2.COLOR_BGR2YCrCb)
    
    #division de l'image en Y / Cb et Cr
    imgY = np.zeros(imgA.shape, imgA.dtype)
    imgCb = np.zeros(imgA.shape, imgA.dtype)
    imgCr = np.zeros(imgA.shape, imgA.dtype)
    imgY[:,:,0]=imgA[:,:,0]
    imgCb[:,:,1]=imgA[:,:,1]
    imgCr[:,:,2]=imgA[:,:,2]

    #convertion de Cb et Cr en binaire
    hA,wA,cA = imgA.shape
    CbEnBinaine=""
    CrEnBinaine=""
    for y in range(hA):
        for x in range(wA):
            CbEnBinaine=CbEnBinaine+str(DecToBin16(imgCb[y,x,1]))
            CrEnBinaine=CrEnBinaine+str(DecToBin16(imgCr[y,x,2]))
    #Récupération de la taille du message secret à partir de Cb
    tailleMessageEnBinaire=[]
    for compteurCb in range(7, 255, 16):
        tailleMessageEnBinaire.append(CbEnBinaine[compteurCb])
        tailleMessageEnBinaire.append(CbEnBinaine[compteurCb+1])
    tailleMessageEnBinaire=''.join(tailleMessageEnBinaire)
    tailleMessage=int(tailleMessageEnBinaire,2)
    #print(tailleMessage)

    #Recuperation du message
    messageEnBinaire=[]
    if (tailleMessage)>((len(CbEnBinaine))-256):
        for compteurCb in range(263, len(CbEnBinaine), 16):
            messageEnBinaire.append(CbEnBinaine[compteurCb])
            messageEnBinaire.append(CbEnBinaine[compteurCb+1])
        for compteurCr in range(7, tailleMessage*8+256, 16):
            messageEnBinaire.append(CrEnBinaine[compteurCr])
            messageEnBinaire.append(CrEnBinaine[compteurCr+1])
    else:
        for compteurCb in range(263, tailleMessage*8+256, 16):
            messageEnBinaire.append(CbEnBinaine[compteurCb])
            messageEnBinaire.append(CbEnBinaine[compteurCb+1])
    messageEnBinaire=''.join(messageEnBinaire)


    #convertion du message en decimal
    message=[]
    for i in range (0, len(messageEnBinaire), 8):
        message.append(int(messageEnBinaire[i:i+8], 2))

    #creation de l'image qui contient le text secret
    imgB = np.zeros((150,250,3), np.uint8)
    i=0
    for y in range(150):
        for x in range(250):
            imgB[y,x,0]=message[i]
            imgB[y,x,1]=message[i] 
            imgB[y,x,2]=message[i]
            i=i+1
    
    #re-convertion de l'image imgA en BGR
    #conversion de Cb et Cr et decimal
    compteur=0
    for y in range(hA):
        for x in range(wA):
            imgCb[y,x,1]=int(CbEnBinaine[compteur:compteur+16],2)
            imgCr[y,x,2]=int(CrEnBinaine[compteur:compteur+16],2)
            compteur=compteur+16
    #convertion de l'image
    imgA[:,:,1]=imgCb[:,:,1]
    imgA[:,:,2]=imgCr[:,:,2]
    imgA = cv2.cvtColor(imgA, cv2.COLOR_YCrCb2BGR)
    
    #affiche de imgB
    cv2.imshow("imageB", imgB)



#Partie interface
root = tk.Tk()
root.title('VISION Part 1')

canvas=tk.Canvas(root, width=800, height=400)
canvas.grid(columnspan=2, rowspan=4)

def Emetteur (texte):
    global imgA
    #recuperation du text
    #texte=input('Ecrivez le message:')

    #creation d'une image vide (blanche)
    imgB = np.zeros((150,250,3), np.uint8)
    imgB[:,:,:]=255

    #découpage du texte en ligne (avec 4 espaces dans chaque ligne)
    compteurEspace=0
    for i in range(len(texte)):
        if texte[i]==" ":
            compteurEspace+=1
            if compteurEspace==4:
                texte=texte[:i+1]+"\n"+texte[i+1:]
                compteurEspace=0
    textAffich=texte.split('\n')

    #ajout du message dans l'image vide
    y0,d=15,20
    for i,line in enumerate(textAffich):
        y=y0+i*d
        cv2.putText(img= imgB,text=line, 
        org=(0,y), 
        fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
        fontScale=0.5,
        color=(0,0,0),
        thickness=1,
        lineType=2)

    #convertion de l'image du message en binaire
    hB,wB,cB = imgB.shape
    imageDuTextEnBinaire=''
    i=0
    for y in range(hB):
        for x in range(wB):
            imageDuTextEnBinaire=imageDuTextEnBinaire+str(DecToBin8(imgB[y,x,0]))
    tailleMessage=len(imageDuTextEnBinaire)
    #print(imageDuTextEnBinaire)
    #sauvegarde de la taille de l'image en binaire
    tailleMessageEnBinaire='{:032b}'.format(tailleMessage)

    #convertion de l'image imgA en YCbCr 16 bits
    imgA = cv2.cvtColor(imgA, cv2.COLOR_BGR2YCrCb)

    #division de l'image en Y / Cb et Cr
    imgY = np.zeros(imgA.shape, imgA.dtype)
    imgCb = np.zeros(imgA.shape, imgA.dtype)
    imgCr = np.zeros(imgA.shape, imgA.dtype)
    imgY[:,:,0]=imgA[:,:,0]
    imgCb[:,:,1]=imgA[:,:,1]
    imgCr[:,:,2]=imgA[:,:,2]

    #convertion de Cb et Cr en binaire
    hA,wA,cA = imgA.shape
    CbEnBinaine=""
    CrEnBinaine=""
    for y in range(hA):
        for x in range(wA):
            CbEnBinaine=CbEnBinaine+str(DecToBin16(imgCb[y,x,1]))
            CrEnBinaine=CrEnBinaine+str(DecToBin16(imgCr[y,x,2]))


    #Ajout de la taille du message secret à Cb
    compteurCb=7
    lstCb=list(CbEnBinaine)
    for i in range(0, 32,2):
        lstCb[compteurCb]=tailleMessageEnBinaire[i]
        lstCb[compteurCb+1]=tailleMessageEnBinaire[i+1]
        compteurCb=compteurCb+16

    #Ajout de imgB dans Cb et Cr
    compteurCb=263
    compteurCr=7
    lstCr=list(CrEnBinaine)
    for bit in range(0,tailleMessage,2):
        if compteurCb<len(CbEnBinaine):
            lstCb[compteurCb]=imageDuTextEnBinaire[bit]
            lstCb[compteurCb+1]=imageDuTextEnBinaire[bit+1]
            compteurCb=compteurCb+16
        elif compteurCr<len(CrEnBinaine):
            lstCr[compteurCr]=imageDuTextEnBinaire[bit]
            lstCr[compteurCr+1]=imageDuTextEnBinaire[bit+1]
            compteurCr=compteurCr+16
        else:
            print('DEPASSEMENT  !!!!')
    CbEnBinaine=''.join(lstCb)
    CrEnBinaine=''.join(lstCr)

    #re-convertion de l'image imgA en BGR
    #conversion de Cb et Cr et decimal
    compteur=0
    for y in range(hA):
        for x in range(wA):
            imgCb[y,x,1]=int(CbEnBinaine[compteur:compteur+16],2)
            imgCr[y,x,2]=int(CrEnBinaine[compteur:compteur+16],2)
            compteur=compteur+16
    #convertion de l'image
    imgA[:,:,1]=imgCb[:,:,1]
    imgA[:,:,2]=imgCr[:,:,2]
    imgA = cv2.cvtColor(imgA, cv2.COLOR_YCrCb2BGR)

    #changement du button recepteur
    changebuttonRec()


#recuperation du message
def affich_e():
    def Take_input():
        INPUT = inputtxt.get("1.0", "end-1c")
        return INPUT
    l = tk.Label(text = "Entrez le message secret :", font='Raleway', fg="black")
    inputtxt = tk.Text(root, height = 5,
                    width = 30)
    ok_btn = tk.Button(root, 
                    text="Valider", 
                    command=lambda:Emetteur(Take_input()), 
                    font='Raleway',
                    bg="#4D90FE", 
                    fg="white", 
                    height=1, 
                    width=10,
                    border=0)

    l.grid(columnspan=2, column=0, row=4)
    inputtxt.grid(columnspan=2, column=0, row=5)
    ok_btn.grid(columnspan=2, column=0, row=6, pady=(10,0))
    canvas=tk.Canvas(root,width=800, height=50)
    
    canvas.grid(columnspan=2)
    
#choisir l'image
def upload_image():
    global imgA
    f_types = [('PNG Files','*.png')]
    path = filedialog.askopenfilename(filetypes=f_types)
    imgA = np.asarray(Image.open(path))
    print(imgA.dtype)
    #cv2.imshow('image', imgA)
    if (imgA is None):
        print("Erreur de chargment")
        exit(0)
    imgA=cv2.resize(imgA,(600,330))
    imgA = np.uint16(imgA)*256
    #convertion à bgr manuellement:
    imgtmp = imgA.copy()
    imgA[:,:,0]=imgtmp[:,:,2]
    imgA[:,:,2]=imgtmp[:,:,0]
    # imgA = cv2.cvtColor(imgA, cv2.COLOR_RGB2BGR)
    changebuttonVoir()
    changebuttonEmmet()
    

#Buttons
Charger_button=E_button=tk.Button(root, 
                            text="Charger l'image", 
                            command=upload_image, 
                            font='Raleway', 
                            bg="#4D90FE", 
                            fg="white", 
                            height=3, 
                            width=40)
Charger_button.grid(columnspan=2, column=0, row=0)

Voir_button=tk.Button(root, 
                    text="Afficher l'image", 
                    font='Raleway', 
                    bg="#666666", 
                    fg="white", 
                    height=2, 
                    width=15)
Voir_button.grid(columnspan=2, column=0, row=1)

Emmet_button=tk.Button(root, 
                text="Emetteur", 
                font='Raleway', 
                bg="#666666", 
                fg="white", 
                height=2, 
                width=20)
Emmet_button.grid(column=0, row=3)

Recep_button=tk.Button(root, 
                    text='Recepteur', 
                    font='Raleway', 
                    bg="#666666", 
                    fg="white", 
                    height=2, 
                    width=20)
Recep_button.grid(column=1, row=3)

def changebuttonRec(bg="#4D90FE", command=Recepteur):
    Recep_button['bg'] = bg
    Recep_button['command'] = command

def changebuttonVoir(bg="#4D90FE", command=AfficheImage):
    Voir_button['bg'] = bg
    Voir_button['command'] = command

def changebuttonEmmet(bg="#4D90FE", command=affich_e):
    Emmet_button['bg'] = bg
    Emmet_button['command'] = command
    
#images
imageEmet=Image.open('Emetteur.png')
imageEmet=ImageTk.PhotoImage(imageEmet)
Emetteur_label=tk.Label(image=imageEmet)
Emetteur_label.image=imageEmet
Emetteur_label.grid(column=0, row=2)

imageRece=Image.open('Recepteur.png')
imageRece=ImageTk.PhotoImage(imageRece)
Recepteur_label=tk.Label(image=imageRece)
Recepteur_label.image=imageRece
Recepteur_label.grid(column=1, row=2)









root.mainloop()