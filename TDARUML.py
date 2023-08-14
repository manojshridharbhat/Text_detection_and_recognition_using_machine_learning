import cv2
import tkinter as tk
from PIL import Image, ImageTk
import pytesseract
import nltk
from nltk.corpus import words

# Download the corpus of English words if not already present
# nltk.download('words')




class TextDetectionApp:
    def _init_(self):
        self.cam = cv2.VideoCapture(0)
        self.root = tk.Tk()
        self.root.title("Text Detection App")
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.root.configure(bg="silver")

        self.camera_label = tk.Label(self.root)
        self.camera_label.pack()
       

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.op_btn = tk.Button(self.button_frame, text="Output", command=self.display_text)
        self.op_btn.pack(side="right", padx=10, pady=10)
        self.capture_btn = tk.Button(self.button_frame, text="Capture", command=self.capture_image)
        self.capture_btn.pack(side="left", padx=10, pady=10)
       
        self.tts_btn = tk.Button(self.button_frame, text="Sound", command=self.tts)
        self.tts_btn.pack(side="right", padx=10, pady=10)

        self.output_text = tk.Text(self.root, height=5, width=50, bg="silver", fg="black")
        self.output_text.pack(padx=10, pady=10)
       

        self.exit_btn = tk.Button(self.root, text="Exit", command=self.on_exit)
        self.exit_btn.pack(side="bottom", padx=10, pady=10)

        self.img_counter = 0
        self.text = ""

        self.show_camera_feed()
        self.root.mainloop()

    def show_camera_feed(self):
        ret, frame = self.cam.read()
        if ret:
            frame = cv2.resize(frame, (500, 500))
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
            self.camera_label.after(10, self.show_camera_feed)

    def capture_image(self):
        ret, frame = self.cam.read()
        if ret:
            frame = cv2.resize(frame, (500, 500))
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            img_name = "opencv_frame_{}.png".format(self.img_counter)
            cv2.imwrite(img_name, frame)
            self.img_counter += 1
            self.detect_text(img_name)

    def detect_text(self, img_name):
        img = cv2.imread(img_name)
        # Convert the image to grayscale
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#         # Apply Gaussian blur to remove noise
#         img = cv2.GaussianBlur(img, (5, 5), 0)
#
#         # Apply adaptive thresholding to create a binary image
#         img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

        # Invert the binary image for better OCR results
#         img = cv2.bitwise_not(img)
#
        # Apply dilation to thicken the text
#         kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#         img = cv2.dilate(img, kernel, iterations=1)

        # Perform OCR using PyTesseract
        config = r'--oem 3 --psm 6'
        self.text = pytesseract.image_to_string(img, config=config)

        # Remove non-English words
        english_words = set(words.words())
        tokens = nltk.word_tokenize(self.text)
        self.text = ' '.join([word for word in tokens if word.lower() in english_words])

        # Store the detected text in a file called "text.txt"
        with open('text.txt', 'w') as f:
            f.write(self.text)

       
    def tts(self):
       
        import pyttsx3
# initialize Text-to-speech engine
        engine = pyttsx3.init()
# convert this text to speech


        file1 = open("text.txt","r")
# initialize list
        list1 = file1.read()
        file1.close()
        file1 = open("text.txt","w")
        list1=list1.replace('\n','      ')
        file1.writelines(list1)
        file1.close()

        file1 = open("text.txt","r")
        text=file1.readlines()
        file1.close()

        engine.setProperty("rate", 125)
#engine.setProperty("voice", voices[1].id)
        engine.say(text)
# play the speech
        engine.save_to_file(text, "python.mp3")
        engine.runAndWait()

    def display_text(self):
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert('1.0', self.text.replace('\n', ' '))

    def on_exit(self):
        self.cam.release()
        self.root.destroy()


if _name_ == '_main_':
    TextDetectionApp()