import time
import numpy as np
import cv2
from Server import start_server_process, get_control_instruction, put_output_image
import camera_stream
class ColorTrackingBehavior:
    def __init__(self):
        self.x= 50
        self.y = 50
        self.y1 = 180   #coordinate di partenza quadrati
        self.x1 = 200
        self.xs = 100   #coordinate partenza scritte
        self.ys = 120
        self.lato = 40
        self.spessore = 2
        self.font = cv2.FONT_HERSHEY_PLAIN
    def quadrato (frame, x,y, lato, spessore):
        cv2.rectangle(frame, (x,y), (x+lato, y+lato), (255,255,255), spessore) # disegno il rettangolo
        pixel = frame[int(x+lato/2), int(y+lato/2)]
        sommaB = 0
        sommaG = 0
        sommaR = 0
        npixel = 0
        for i in range (x,x+lato):
            for j in range (y , y+lato):
                pixel = frame[i, j]
                sommaB = sommaB + pixel[0]
                sommaG = sommaG + pixel[1]
                sommaR = sommaR + pixel[2]
                npixel = npixel + 1
        mediaB = int(sommaB/npixel)
        mediaG = int(sommaG/npixel)
        mediaR = int(sommaR / npixel)
        return mediaB, mediaG, mediaR

    def colore (mediaB, mediaG, mediaR) :
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
    def process_frame(self, frame):
        nuovafinestra.fill(0) # imposto a zero (nero) la nuovafinestra
        Stringa = "        B -- G -- R"
        cv2.putText(nuovafinestra, Stringa, (self.xs ,self.ys-100), self.font,1,(255, 255, 255), 1, cv2.LINE_AA)
        cv2.rectangle(frame, (self.x,self.y), (self.x+self.lato, self.y+self.lato), (255,255,255), self.spessore) # disegno il rettangolo i alto a sinistra
        cv2.rectangle(frame, (self.x1,self.y1), (self.x1+self.lato, self.y1+self.lato), (255,255,255), self.spessore) # disegno il rettangolo in basso a destra
        display_frame = np.concatenate((frame, nuovafinestra), axis=1)
        encoded_bytes = camera_stream.get_encoded_bytes_for_frame(display_frame)
        #encoded_bytes = camera_stream.get_encoded_bytes_for_frame(frame)
        put_output_image(encoded_bytes)
        return 
    def process_control(self):
        instruction = get_control_instruction()
        if instruction:
            command = instruction['command']
            print (command)
            if command == "start":
                self.running = True
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
            self.process_control()

behavior = ColorTrackingBehavior()
nuovafinestra = np.zeros((240,320,3), np.uint8) # definisco la nuova finestra
process = start_server_process('Calibrazione_Colori.html')

try:
    behavior.controlled_image_server_behavior()
finally:
    process.terminate()