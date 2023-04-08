from picamera2 import Picamera2, Preview
from time import sleep

def capture():
    #preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
    #picam2.configure(preview_config)

    #picam2.start_preview(Preview.QTGL)
    picam2 = Picamera2()
    picam2.start()
    sleep(0.5)

    metadata = picam2.capture_file('/home/DropBot/Desktop/scripts/dronepic.jpg')
    picam2.close()
    
def simple_capture():
    picam2.start_and_capture_file("dronepic.jpg")

if __name__ == "__main__":
    capture()
