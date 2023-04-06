from picamera2 import Picamera2, Preview
from time import sleep
import release

picam2 = Picamera2()

def capture():
    preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
    picam2.configure(preview_config)

    picam2.start_preview(Preview.QTGL)

    picam2.start()
    sleep(0.5)

    metadata = picam2.capture_file('/home/DropBot/Desktop/test.jpg')
    picam2.close()

if __name__ == "__main__":
    capture()