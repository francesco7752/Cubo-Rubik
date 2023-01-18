import time
import numpy as np
import cv2
from Server import start_server_process, get_control_instruction, put_output_image
import camera_stream
class ColorTrackingBehavior:
    def __init__(self):
        self.x= 80
        self.y = 30
        #self.xs = 10   #coordinate partenza scritte
        #self.ys = 0
        self.lato = 60
        self.spessore = 2
        self.distanza = 4
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.DevoElaborare = False
        self.nuovafinestra = np.zeros((240,320,3), np.uint8) # definisco la nuova finestra
    def quadrato (self,frame, x,y, lato, spessore):
        cv2.rectangle(frame, (x,y), (x+lato, y+lato), (255,255,255), spessore) # disegno il rettangolo
        sommaB = 0
        sommaG = 0
        sommaR = 0
        npixel = 0
        for i in range (x,x+lato):
            for j in range (y , y+lato):
                try:
                    pixel = frame[j, i]
                except:
                    print(x,y,i,j,lato)
                sommaB = sommaB + pixel[0]
                sommaG = sommaG + pixel[1]
                sommaR = sommaR + pixel[2]
                npixel = npixel + 1
        mediaB = int(sommaB/npixel)
        mediaG = int(sommaG/npixel)
        mediaR = int(sommaR / npixel)
        return mediaB, mediaG, mediaR

    def colore (self,mediaB, mediaG, mediaR) :
        if  mediaG > mediaR and mediaG > mediaB and ( mediaG - mediaR) > 30 and (mediaG - mediaB) > 30 : #verde
            return 0,255,0
        if  mediaB > mediaG and mediaB > mediaR and (mediaB - mediaR) > 30 and (mediaB - mediaG) > 30 : #blu
            return 255,0,0
        if mediaR > mediaG and mediaR > mediaB and ( mediaR - mediaB) > 30 and (mediaR - mediaG) > 30   and abs(mediaG - mediaB) < 30: #rosso
            return 0,0,255  
        if abs( mediaR - mediaB) < 30 and abs(mediaR - mediaG) < 30 and abs(mediaG - mediaB) < 30  : #bianco
            return 255,255,255
        if mediaB > 100   and mediaG > 100 and mediaR > 100 : #bianco
            return 255,255,255        
        if mediaG > mediaB and mediaR > mediaB and ( mediaR - mediaB) > 30 and (mediaG - mediaB) > 30 and mediaG >= 180 and mediaB < 100 : #giallo      
            return 0,255,255

        # colore non classificato, ritorna l'arancio
        return 14,75,255  

    def elabora (self,frame, nuovafinestra) :
        if self.DevoElaborare == False:
            frame = np.concatenate((frame, nuovafinestra), axis=1)
            return frame
        nuovafinestra.fill(0) # imposto a zero (nero) la nuovafinestra
        print("frame", frame.shape)
        print ("nuovafinestra", nuovafinestra.shape)
        Stringa = "        B -- G -- R"
        xx = self.x
        yy = self.y 
        
        xxq = xx-50
        yyq = yy  
        xxs = xx + 2*self.lato -50
        latoq = int(self.lato/2)  

        cv2.putText(nuovafinestra, Stringa, (xxs ,yy-40), self.font,1,(255, 255, 255), 1, cv2.LINE_AA)


      
        
        mediaB, mediaG, mediaR = self.quadrato(frame, xx, yy, self.lato, self.spessore)
        coloreB, coloreG, coloreR = self.colore (mediaB, mediaG, mediaR)
        cv2.rectangle(nuovafinestra, (xxq,yyq), (xxq + latoq, yyq + latoq), (coloreB,coloreG,coloreR), -1)  # con -1 gli diciamo di riempire la figura
        cv2.putText(nuovafinestra, "1", (xxq,yyq-10), self.font,1,(255, 255, 255), 1, cv2.LINE_AA)  
        Stringa = "1 -> " + str(mediaB) + "-" + str(mediaG) + "-" + str(mediaR)
        cv2.putText(nuovafinestra, Stringa, (xxs ,yyq-10),self.font,1,(255, 255, 255), 1, cv2.LINE_AA) 
        
        xxq = xxq+latoq+self.spessore
        xx = xx+self.spessore+self.lato
        
        mediaB, mediaG, mediaR = self.quadrato(frame, xx, yy, self.lato, self.spessore)
        coloreB, coloreG, coloreR = self.colore (mediaB, mediaG, mediaR)
        cv2.rectangle(nuovafinestra, (xxq,yyq), (xxq + latoq, yyq + latoq), (coloreB,coloreG,coloreR), -1)  # con -1 gli diciamo di riempire la figura
        cv2.putText(nuovafinestra, "2", (xxq,yyq-10), self.font,1,(255, 255, 255), 1, cv2.LINE_AA)  
        Stringa = "2 -> " + str(mediaB) + "-" + str(mediaG) + "-" + str(mediaR)
        cv2.putText(nuovafinestra, Stringa, (xxs ,yyq+10),self.font,1,(255, 255, 255), 1, cv2.LINE_AA) 
        
        xxq = xxq+latoq+self.spessore
        xx = xx+self.spessore+self.lato
        
        mediaB, mediaG, mediaR = self.quadrato(frame, xx, yy, self.lato, self.spessore)
        coloreB, coloreG, coloreR = self.colore (mediaB, mediaG, mediaR)
        cv2.rectangle(nuovafinestra, (xxq,yyq), (xxq + latoq, yyq + latoq), (coloreB,coloreG,coloreR), -1)  # con -1 gli diciamo di riempire la figura
        cv2.putText(nuovafinestra, "3", (xxq,yyq-10), self.font,1,(255, 255, 255), 1, cv2.LINE_AA)  
        Stringa = "3 -> " + str(mediaB) + "-" + str(mediaG) + "-" + str(mediaR)
        cv2.putText(nuovafinestra, Stringa, (xxs ,yyq+30),self.font,1,(255, 255, 255), 1, cv2.LINE_AA)

        xx = self.x
        yy = self.y + self.lato+self.spessore
        yyq = yy

        xxq = xx-50
        xxs = xx + 2*self.lato -50

        mediaB, mediaG, mediaR = self.quadrato(frame, xx, yy, self.lato, self.spessore)
        coloreB, coloreG, coloreR = self.colore (mediaB, mediaG, mediaR)
        cv2.rectangle(nuovafinestra, (xxq,yyq), (xxq + latoq, yyq + latoq), (coloreB,coloreG,coloreR), -1)  # con -1 gli diciamo di riempire la figura
        cv2.putText(nuovafinestra, "4", (xxq,yyq-10), self.font,1,(255, 255, 255), 1, cv2.LINE_AA)  
        Stringa = "4 -> " + str(mediaB) + "-" + str(mediaG) + "-" + str(mediaR)
        cv2.putText(nuovafinestra, Stringa, (xxs ,yyq-10),self.font,1,(255, 255, 255), 1, cv2.LINE_AA) 
        
        xxq = xxq+latoq+self.spessore
        xx = xx+self.spessore+self.lato
        
        mediaB, mediaG, mediaR = self.quadrato(frame, xx, yy, self.lato, self.spessore)
        coloreB, coloreG, coloreR = self.colore (mediaB, mediaG, mediaR)
        cv2.rectangle(nuovafinestra, (xxq,yyq), (xxq + latoq, yyq + latoq), (coloreB,coloreG,coloreR), -1)  # con -1 gli diciamo di riempire la figura
        cv2.putText(nuovafinestra, "5", (xxq,yyq-10), self.font,1,(0, 0, 255), 1, cv2.LINE_AA)  
        Stringa = "5 -> " + str(mediaB) + "-" + str(mediaG) + "-" + str(mediaR)
        cv2.putText(nuovafinestra, Stringa, (xxs ,yyq+10),self.font,1,(255, 255, 255), 1, cv2.LINE_AA) 
        
        xxq = xxq+latoq+self.spessore
        xx = xx+self.spessore+self.lato
        
        mediaB, mediaG, mediaR = self.quadrato(frame, xx, yy, self.lato, self.spessore)
        coloreB, coloreG, coloreR = self.colore (mediaB, mediaG, mediaR)
        cv2.rectangle(nuovafinestra, (xxq,yyq), (xxq + latoq, yyq + latoq), (coloreB,coloreG,coloreR), -1)  # con -1 gli diciamo di riempire la figura
        cv2.putText(nuovafinestra, "6", (xxq,yyq-10), self.font,1,(0, 0, 255), 1, cv2.LINE_AA)  
        Stringa = "6 -> " + str(mediaB) + "-" + str(mediaG) + "-" + str(mediaR)
        cv2.putText(nuovafinestra, Stringa, (xxs ,yyq+30),self.font,1,(255, 255, 255), 1, cv2.LINE_AA)

        xx = self.x
        yy = self.y + 2*self.lato+ 2*self.spessore
        yyq = yy
        
        xxq = xx-50
        xxs = xx + 2*self.lato -50

        mediaB, mediaG, mediaR = self.quadrato(frame, xx, yy, self.lato, self.spessore)
        coloreB, coloreG, coloreR = self.colore (mediaB, mediaG, mediaR)
        cv2.rectangle(nuovafinestra, (xxq,yyq), (xxq + latoq, yyq + latoq), (coloreB,coloreG,coloreR), -1)  # con -1 gli diciamo di riempire la figura
        cv2.putText(nuovafinestra, "7", (xxq,yyq-10), self.font,1,(255, 255, 255), 1, cv2.LINE_AA)  
        Stringa = "7 -> " + str(mediaB) + "-" + str(mediaG) + "-" + str(mediaR)
        cv2.putText(nuovafinestra, Stringa, (xxs ,yyq-10),self.font,1,(255, 255, 255), 1, cv2.LINE_AA) 
        
        xxq = xxq+latoq+self.spessore
        xx = xx+self.spessore+self.lato
        
        mediaB, mediaG, mediaR = self.quadrato(frame, xx, yy, self.lato, self.spessore)
        coloreB, coloreG, coloreR = self.colore (mediaB, mediaG, mediaR)
        cv2.rectangle(nuovafinestra, (xxq,yyq), (xxq + latoq, yyq + latoq), (coloreB,coloreG,coloreR), -1)  # con -1 gli diciamo di riempire la figura
        cv2.putText(nuovafinestra, "8", (xxq,yyq-10), self.font,1,(255, 255, 255), 1, cv2.LINE_AA)  
        Stringa = "8 -> " + str(mediaB) + "-" + str(mediaG) + "-" + str(mediaR)
        cv2.putText(nuovafinestra, Stringa, (xxs ,yyq+10),self.font,1,(255, 255, 255), 1, cv2.LINE_AA) 
        
        xxq = xxq+latoq+self.spessore
        xx = xx+self.spessore+self.lato
        
        mediaB, mediaG, mediaR = self.quadrato(frame, xx, yy, self.lato, self.spessore)
        coloreB, coloreG, coloreR = self.colore (mediaB, mediaG, mediaR)
        cv2.rectangle(nuovafinestra, (xxq,yyq), (xxq + latoq, yyq + latoq), (coloreB,coloreG,coloreR), -1)  # con -1 gli diciamo di riempire la figura
        cv2.putText(nuovafinestra, "9", (xxq,yyq-10), self.font,1,(255, 255, 255), 1, cv2.LINE_AA)  
        Stringa = "9 -> " + str(mediaB) + "-" + str(mediaG) + "-" + str(mediaR)
        cv2.putText(nuovafinestra, Stringa, (xxs ,yyq+30),self.font,1,(255, 255, 255), 1, cv2.LINE_AA)




        frame = np.concatenate((frame, nuovafinestra), axis=1)
        self.DevoElaborare = False
        return frame


    def process_frame(self, frame):
        xx = self.x
        yy = self.y
        cv2.rectangle(frame, (xx,yy), (xx+self.lato, yy+self.lato), (255,255,255), self.spessore) # disegno il rettangolo i alto a sinistra
        xx = self.x+self.spessore+self.lato
        cv2.rectangle(frame, (xx,yy), (xx+self.lato, yy+self.lato), (255,255,255), self.spessore)
        xx = xx+self.spessore+self.lato
        cv2.rectangle(frame, (xx,yy), (xx+self.lato, yy+self.lato), (255,255,255), self.spessore)

        xx = self.x
        yy = yy + self.spessore + self.lato
        cv2.rectangle(frame, (xx,yy), (xx+self.lato, yy+self.lato), (255,255,255), self.spessore) 
        xx = self.x+self.spessore+self.lato
        cv2.rectangle(frame, (xx,yy), (xx+self.lato, yy+self.lato), (255,255,255), self.spessore)
        xx = xx+self.spessore+self.lato
        cv2.rectangle(frame, (xx,yy), (xx+self.lato, yy+self.lato), (255,255,255), self.spessore)

        xx = self.x
        yy = yy + self.spessore + self.lato
        cv2.rectangle(frame, (xx,yy), (xx+self.lato, yy+self.lato), (255,255,255), self.spessore)
        xx = self.x+self.spessore+self.lato
        cv2.rectangle(frame, (xx,yy), (xx+self.lato, yy+self.lato), (255,255,255), self.spessore)
        xx = xx+self.spessore+self.lato
        cv2.rectangle(frame, (xx,yy), (xx+self.lato, yy+self.lato), (255,255,255), self.spessore) 

        frame = self.elabora(frame, self.nuovafinestra)
        #display_frame = np.concatenate((frame, nuovafinestra), axis=1)
        #encoded_bytes = camera_stream.get_encoded_bytes_for_frame(display_frame)
        encoded_bytes = camera_stream.get_encoded_bytes_for_frame(frame)
        put_output_image(encoded_bytes)
        return 
    def process_control(self,frame):
        instruction = get_control_instruction()
        if instruction:
            command = instruction['command']
            print (command)
            if command == "start":
                self.DevoElaborare = True
            elif command == "stop":
                self.running = False
            if command == "exit":
                print("fermo v4")
                exit()    
    def controlled_image_server_behavior(self):
        camera = camera_stream.setup_camera()
        time.sleep(0.1)

        for frame in camera_stream.start_stream(camera):
            self.process_frame(frame)
            self.process_control(frame)

behavior = ColorTrackingBehavior()
#nuovafinestra = np.zeros((320,240,3), np.uint8) # definisco la nuova finestra
process = start_server_process('Calibrazione_Colori.html')

try:
    behavior.controlled_image_server_behavior()
finally:
    process.terminate()