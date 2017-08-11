

#include <Wire.h>
#include <Adafruit_SSD1306.h>

#include <HcSr04_3Lectores.h>

// pantalla lcd oled 0.91
#define OLED_RESET 4
Adafruit_SSD1306 display(OLED_RESET);

#if (SSD1306_LCDHEIGHT != 32)
#error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif


HcSr04_3Lectores HC(6, 7, 8, 9, 10, 11);

void setup() {
  
  Serial.begin(115200);
  while (!Serial); // Solo para el Leonardo

  pinMode(LED_BUILTIN, OUTPUT);

  
  Serial.println("START");

  // by default, we'll generate the high voltage from the 3.3v line internally! (neat!)
  // initialize with the I2C addr 0x3C (for the 128x32)
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.setTextColor(WHITE); // importante, color del texto
  display.setTextSize(4);
  display.setCursor(0, 0); // posicion (x,y)
  display.print("START");
  display.display();

  HC.init();
  HC.LOG_ACTIVO = false;


}


void loop() {

  HC.medirDistancias();
  if (HC.medicionFinalizada()) {
    logDisplay();

    Serial.print(HC.getSentido());
    Serial.print("##");
    Serial.print(HC.getVelocidad());
    Serial.print("##");
    Serial.print(HC.getTiempoUltimo());
    Serial.println("##");
    
    
    delay(100);
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  }

}



/*
   Imprime el sentido del movimiento en el display
   0 - izquierda a derecha
   1 - derecha a izquierda
*/
void logDisplay() {

  // Display IIC I2C 0.91" 128x32 OLED LCD Display
  // en tamaño de texto 1 tiene 4 lineas por 21 caracteres
  char str[21];
 
  display.clearDisplay();

    // invert the display
  display.invertDisplay(true);
  delay(200);
  display.invertDisplay(false);
  delay(200);
  
  display.setTextSize(1);
  display.setCursor(0, 0);  // coordenadas eje x, y
  
  switch (HC.getSentido()) {
    case 1:
      snprintf(str, 21, "%6d %12s", HC.getVelocidad(), ">>>>>>>>>>>>" );
      break;

    case 2:+
       snprintf(str, 21, "%6d %12s", HC.getVelocidad(), "<<<<<<<<<<<<");
      break;

    default:
      break;
  }

  display.println(str); 
  display.display();

}










