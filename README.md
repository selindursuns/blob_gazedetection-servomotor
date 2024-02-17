# blob_gazedetection-servomotor
Gaze Detection Activating Servo Motors (Raspberry Pi 4+)

Blob is an gaze-activated entity that blows air into water when human eyes meet them. 
Whenever you look in the camera, the motor will start rotating.

![f83ac6cf-a166-4403-908c-c1eea6e1ff8b_rw_1200](https://github.com/selindursuns/blob_gazedetection-servomotor/assets/122591669/e743b833-d9e4-4a1d-956f-81b24b57b7e2)

You need:
1. Air Pump + DC Motor 4.5 V (Adafruit)
2. Raspberry Pi 4 B
3. L9110s Motor Driver
4. Rasberry PiCamera (mini camera)
5. Vaze + Electronics Compartment

About the Order of Execution:

  1.  Make sure you install the OpenCV after installing Python.
      Some helpful resources: https://www.youtube.com/watch?v=jRKgEXiMtns&t=449s
                              https://www.youtube.com/watch?v=QzVYnG-WaM4&t=131s
  2. Autostart file allows Raspberry Pi to execute the code the moment board is turned on. This system will allow you to automaticly open the main code.
  3. Make sure you use the pin connections correctly between motor driver - motor - raspberry Pi. (If needed, See https://www.youtube.com/watch?app=desktop&v=Qp4wNdyC2Z0)
  4. Run the main code, and you are good to go! :)
                           
   Credits: Pysource for the .dat file.

   Made by: Selin Dursun (Harvard), Merve Akdogan(MIT), Yinghou Wang (Harvard)
