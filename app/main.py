from datetime import datetime as dt
import os
import time

from bokeh.models import (Plot, DataRange1d, Range1d, ColumnDataSource,
    DatetimeAxis, LinearAxis, SingleIntervalTicker as SITicker, BasicTickFormatter,
    Image, Rect, Step)
from bokeh.plotting import show, curdoc
from bokeh.themes import Theme
import cv2
from jinja2 import Environment, FileSystemLoader

APP_DIR = os.path.dirname(__file__)

env = Environment(loader=FileSystemLoader(os.path.join(APP_DIR, 'templates')))

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720


class FaceDetection(object):
    def __init__(self, face_cascade):
        self.face_cascade = face_cascade
        self.t0 = time.mktime(dt.now().timetuple()) * 1000

        ### Image Plot
        self.image_source = ColumnDataSource({"image": []})
        self.rect_source = ColumnDataSource({"x": [], "y": [], "w": [], "h": []})

        self.image_plot = Plot(
            name="image", width=CAMERA_WIDTH//2, height=CAMERA_HEIGHT//2,
            x_range=Range1d(0, CAMERA_WIDTH), y_range=Range1d(0, CAMERA_HEIGHT))
        self.image_plot.add_glyph(
            self.image_source,
            Image(image='image', x=0, y=0, dw=CAMERA_WIDTH, dh=CAMERA_HEIGHT))
        self.image_plot.add_glyph(
            self.rect_source,
            Rect(x='x', y='y', width='w', height='h'))

        ### Timeseries Plot
        self.ts_source = ColumnDataSource({"x": [], "y": []})

        self.ts_plot = Plot(
            name="ts", x_range=DataRange1d(), y_range=DataRange1d(),
            width=CAMERA_WIDTH//2, height=150)
        self.ts_plot.add_layout(DatetimeAxis(axis_label="time"), "below")
        self.ts_plot.add_layout(LinearAxis(axis_label="num faces", ticker=SITicker()), "left")
        self.ts_plot.add_glyph(
            self.ts_source,
            Step(x="x", y="y"))

    def update(self, video_capture):
        ret, frame = video_capture.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                    frame,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30))

            # invert the image for plotting
            frame = frame[::-1]

            # the faces rects origin is top left so we need to mangle
            rect_dict = dict(x=[], y=[], w=[], h=[])
            for x, y, w, h in faces:
                rect_dict["x"].append(x+w/2)
                rect_dict["y"].append(CAMERA_HEIGHT-y-h/2)
                rect_dict["w"].append(w)
                rect_dict["h"].append(h)

            self.rect_source.data = rect_dict
            self.image_source.data["image"] = [frame]
            self.ts_source.stream({
                "x": [time.mktime(dt.now().timetuple()) * 1000 - self.t0],
                "y": [len(faces)]
            })

video_capture = cv2.VideoCapture(0)
# set video capture properties for MacBook' iSight camera
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

# train our cascade classifier
face_cascade = cv2.CascadeClassifier(os.path.join(APP_DIR, 'data', 'haarcascade_frontalface_default.xml'))

face_detection = FaceDetection(face_cascade)

doc = curdoc()
doc.add_root(face_detection.image_plot)
doc.add_root(face_detection.ts_plot)
doc.add_periodic_callback(lambda: face_detection.update(video_capture), 100)
doc.template = env.get_template('index.html')
doc.theme = Theme(os.path.join(APP_DIR, "theme.yml"))
doc.title = "Face Detection"
