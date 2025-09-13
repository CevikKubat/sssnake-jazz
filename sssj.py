import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QFileDialog, QWidget, QPushButton, QMainWindow,
    QVBoxLayout, QHBoxLayout, QLabel, QDial
)
from PIL import Image
from scipy.io.wavfile import write


class KnobWithLabel(QWidget):
    def __init__(self, name, min_val, max_val, default_val):
        super().__init__()
        self.name = name
        self.label = QLabel(f"{name}: {default_val}")
        self.dial = QDial()
        self.dial.setRange(min_val, max_val)
        self.dial.setValue(default_val)
        self.dial.setNotchesVisible(False)
        self.dial.setFixedSize(100, 100)
        self.dial.setWrapping(False)
        self.dial.valueChanged.connect(self.update_label)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.dial)
        self.setLayout(layout)

    def update_label(self, value):
        self.label.setText(f"{self.name}: {value}")

    def value(self):
        return self.dial.value()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sssnake Jazz")
        self.setFixedSize(700, 400)
        self.img = None

        # Buttons
        self.load_button = QPushButton("Load Image")
        self.convert_button = QPushButton("Convert to Audio")
        self.load_button.clicked.connect(self.load_image)
        self.convert_button.clicked.connect(self.convert_to_audio)

        # Knobs with labels
        self.width_knob = KnobWithLabel("Width", 1, 2048, 500)
        self.height_knob = KnobWithLabel("Height", 1, 2048, 500)
        self.sample_rate_knob = KnobWithLabel("Sample Rate", 5513, 192000, 44100)

        # Layout for parameters
        param_layout = QHBoxLayout()
        param_layout.addWidget(self.width_knob)
        param_layout.addWidget(self.height_knob)
        param_layout.addWidget(self.sample_rate_knob)

        # Main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.load_button)
        main_layout.addLayout(param_layout)
        main_layout.addWidget(self.convert_button)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # Load Image 
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select an Image", "", "Image Files (*.png *.jpg *.bmp *.jpeg *.tiff *.gif)"
        )
        if file_path:
            self.img = Image.open(file_path).convert("RGB")
            self.file_name = file_path.split("/")[-1]
            self.file_name = self.file_name.split(".")[0]
            print(f"Loaded image: {file_path}")

    # Convert Image to Audio
    def convert_to_audio(self):
        if self.img is None:
            print("No image loaded!")
            return

        width = self.width_knob.value()
        height = self.height_knob.value()
        sample_rate = self.sample_rate_knob.value()

        # Resize and flatten
        img_resized = self.img.resize((width, height))
        pixels = np.array(img_resized).flatten()
        pixels = (pixels / 255.0) * 2 - 1
        audio_data = np.int16(pixels * 32767)

        write(f"output/{self.file_name}-sss.wav", sample_rate, audio_data)
        img_resized.save(f"output/{self.file_name}-sss.jpg")
        print(f"Audio saved as {self.file_name}-sss.wav at {sample_rate} Hz in output/.")


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
