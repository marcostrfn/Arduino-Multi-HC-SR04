
from time import sleep
import serial
import subprocess
import sys

if len(sys.argv) == 2:
	PUERTO = sys.argv[1]
else:
	print 'Error argumentos'
	sys.exit()
	
	
# volumen de windows 0 - 65535
# Set the volume to the highest value nircmd.exe setsysvolume 65535 


MINIMO = 0
MAXIMO = 65535
ACTUAL = 0
MUTE = False

ACTUAL = MAXIMO / 3
subprocess.call(['nircmd.exe', 'setsysvolume', str(MAXIMO/3) ], shell=False)


def izquierda2derecha(tiempo, tiempo_ultimo):
    global MINIMO, MAXIMO, ACTUAL, MUTE
	
    tiempo_movimiento = int(tiempo) - int(tiempo_ultimo)
    print 'tiempo_movimiento', tiempo_movimiento
    print 'tiempo_ultimo', tiempo_ultimo
    
    print "subir volumen "
    
    if tiempo_movimiento > 700:
        volumen = 5000
    else:
        volumen = 20000
    
    if (tiempo_ultimo > 1000):
        print "unmute"
        MUTE = False
        subprocess.call(['nircmd.exe', 'mutesysvolume', '0'], shell=False)
    else:
        if MUTE: return 
        print "Subo", volumen
        ACTUAL = ACTUAL + volumen
        if ACTUAL > MAXIMO:
            ACTUAL = MAXIMO
        
        print "ACTUAL ", ACTUAL
        subprocess.call(['nircmd.exe', 'setsysvolume', str(ACTUAL)], shell=False)       
        # subprocess.call(['nircmd.exe', 'changesysvolume', str(volumen)], shell=False)
        # subprocess.call(['nircmd.exe', 'cmdwait', '2000', 'savescreenshot', 'captura.png'], shell=False)    
    
    
def derecha2izquierda(tiempo, tiempo_ultimo):
    global MINIMO, MAXIMO, ACTUAL, MUTE
	
    tiempo_movimiento = int(tiempo) - int(tiempo_ultimo)
    print 'tiempo_movimiento', tiempo_movimiento
    print 'tiempo_ultimo', tiempo_ultimo

    
    print "bajar volumen"
    
    if tiempo_movimiento > 700:
        volumen = -5000
    else:
        volumen = -20000

    
    if (tiempo_ultimo > 1000):
        print "mute"
        MUTE = True
        subprocess.call(['nircmd.exe', 'mutesysvolume', '1'], shell=False)
    else:          
        if MUTE: return
        print "bajo", volumen
        ACTUAL = ACTUAL + volumen
        if ACTUAL < MINIMO:
            ACTUAL = MINIMO
        
        print "ACTUAL ", ACTUAL
        subprocess.call(['nircmd.exe', 'setsysvolume', str(ACTUAL)], shell=False)
        
        #subprocess.call(['nircmd.exe', 'changesysvolume', str(volumen)], shell=False)
        # subprocess.call(['nircmd.exe', 'cmdwait', '2000', 'savescreenshot', 'captura.png'], shell=False)
    
    
ser = serial.Serial(PUERTO, 115200) # Establish the connection on a specific port
counter = 0


while True:
    try:        
        l = ser.readline() # Read the newest output from the Arduino        
        print l.rstrip()
        
        
        if (l.rstrip().endswith("##")):
            v = l.rstrip().split("##")
            sentido = v[0]
            tiempo = v[1]
            tiempo_ultimo = int(v[2])
            if sentido=="1":
                izquierda2derecha(tiempo, tiempo_ultimo)
            if sentido=="2":
                derecha2izquierda(tiempo, tiempo_ultimo)
        
    except KeyboardInterrupt:
        break

ser.close()
        
    