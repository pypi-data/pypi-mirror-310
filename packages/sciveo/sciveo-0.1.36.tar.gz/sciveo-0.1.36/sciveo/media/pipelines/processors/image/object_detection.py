#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2024
#

import numpy as np
import cv2

from sciveo.tools.logger import *
from sciveo.tools.simple_counter import Timer
from sciveo.tools.common import *
from sciveo.media.pipelines.processors.base import *


class ObjectDetectorBase:
  def __init__(self, model_path, device='cpu', colors=None):
    self.model_path = model_path
    self.device = device
    if colors is None:
      self.colors = [
        (60, 180, 75),    # Green
        (255, 255, 255),   # White
        (245, 130, 48),   # Orange
        (255, 225, 25),   # Yellow
        (0, 130, 200),    # Blue
        (230, 25, 75),    # Red
        (145, 30, 180),   # Purple
        (70, 240, 240),   # Cyan
        (240, 50, 230),   # Magenta
        (210, 245, 60),   # Lime
        (250, 190, 212),  # Pink
        (0, 128, 128),    # Teal
        (220, 190, 255),  # Lavender
        (170, 110, 40),   # Brown
        (128, 0, 0),      # Maroon
        (0, 0, 128),      # Navy
        (128, 128, 0),    # Olive
        (255, 215, 180),  # Peach
        (255, 250, 200),  # Ivory
        (170, 255, 195),  # Mint
      ]
    else:
      self.colors = colors

  def resize(self, image, h):
    ratio = max(image.shape[0], image.shape[1]) / h
    h, w = int(image.shape[0] / ratio), int(image.shape[1] / ratio)
    return cv2.resize(image, (w, h))

  def load(self, image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

  def read_images(self, images_paths):
    X = []
    for image_path in images_paths:
      image = self.load(image_path)
      image = self.resize(image)
      X.append(image)
    return X

  def draw_label_inverted(self, frame, label_text, x_min, y_min, color, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.3, font_thickness=1):
    text_size = cv2.getTextSize(label_text, font, font_scale, font_thickness)[0]
    y_offset = text_size[1] + 4
    x_offset = text_size[0] + 4
    if y_min - y_offset >= 0:
      text_background_top_left = (x_min, y_min - y_offset)
      text_background_bottom_right = (x_min + x_offset, y_min)
    else:
      text_background_top_left = (x_min, y_min)
      text_background_bottom_right = (x_min + x_offset, y_min + y_offset)

    cv2.rectangle(frame, text_background_top_left, text_background_bottom_right, color, cv2.FILLED)
    cv2.putText(frame, label_text, (x_min + 2, text_background_bottom_right[1] - 2), font, font_scale, (0,0,0), font_thickness)

  def draw_object_rectangle_xyxy(self, frame, box, label, color, alpha=0.2, filled=True):
    (x1, y1, x2, y2) = box

    if filled:
      rectangle = np.zeros((y2 - y1, x2 - x1, 3), dtype=np.uint8)
      rectangle[:] = color
      frame[y1:y2, x1:x2] = cv2.addWeighted(rectangle, alpha, frame[y1:y2, x1:x2], 1 - alpha, 0)

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=1)

    self.draw_label_inverted(frame, label, x1, y1, color=color)

  def draw_object_rectangle_xywh(frame, box, label, color, alpha=0.2, filled=True):
    (x, y, w, h) = box
    (x1, y1, x2, y2) = x, y, x + w, y + h
    self.draw_object_rectangle_xyxy(frame, (x1, y1, x2, y2), label, color, alpha=alpha, filled=filled)


class ObjectDetectorYOLO(ObjectDetectorBase):
  def __init__(self, model_path="yolo11m.pt", device='cpu', colors=None):
    super().__init__(model_path, device=device, colors=colors)
    from ultralytics import YOLO
    self.model = YOLO(self.model_path)

  def predict_one(self, x, confidence_threshold=0.5):
    return self.model.predict(x, device=self.device, conf=confidence_threshold, verbose=False)

  def predict(self, X, max_n=64, confidence_threshold=0.5):
    predictions = []

    num_batches = math.ceil(len(X) / max_n)

    for batch_idx in range(num_batches):
      timer = Timer()
      start_idx = batch_idx * max_n
      end_idx = min((batch_idx + 1) * max_n, len(X))

      batch_images = X[start_idx:end_idx]
      batch_predictions = self.model.predict(batch_images, device=self.device, conf=confidence_threshold, verbose=False)
      predictions.extend(batch_predictions)

      elapsed = timer.stop()
      FPS = len(batch_images) / elapsed
      debug(f"batch {batch_idx} / {num_batches}", "elapsed", elapsed, "FPS", FPS, "len", len(batch_images))

    return predictions

  def resize(self, image):
    return super().resize(image, 640)

  def draw(self, image, detections, colors=None):
    if colors is None:
      colors = self.colors
    height, width = image.shape[:2]
    boxes = detections.boxes
    class_names = detections.names
    for i, box in enumerate(boxes):
      bbox = (np.array(box.xyxyn[0]) * np.array([width, height, width, height])).astype(int).tolist()

      confidence = box.conf[0].item()
      class_id = int(box.cls[0].item())
      label = class_names[class_id]
      label_text = f"{label} {int(confidence * 100)}%"

      color = colors[i % len(colors)]
      self.draw_object_rectangle_xyxy(image, bbox, label_text, color)


class ImageObjectDetectionProcessor(BaseProcessor):
  def __init__(self, processor_config, max_progress) -> None:
    super().__init__(processor_config, max_progress)
    self.default.update({"JPEG_QUALITY": 80, "min_confidence": 0.5, "model_type": 0, "height": 720})

  def init_run(self):
    TPU = os.environ.get("MEDIA_PROCESSING_BACKEND", "cpu")
    self.predictor = ObjectDetectorYOLO(model_path=["yolo11x.pt", "yolo11l.pt", "yolo11m.pt", "yolo11s.pt"][self["model_type"]], device=TPU)

  def process(self, media):
    try:
      self.media = media
      self.local_path = media["local_path"]

      tag = "object-detections"
      image = self.predictor.load(self.local_path)
      image_resized = self.predictor.resize(image)

      detections = self.predictor.predict_one([image_resized], confidence_threshold=self["min_confidence"])

      # image_resized = self.predictor.super().resize(image, h=self["height"])
      image_resized = cv2.cvtColor(image_resized, cv2.COLOR_RGB2BGR)
      self.predictor.draw(image_resized, detections[0])
      result_image_local_path = self.add_suffix_to_filename(self.local_path, tag)
      cv2.imwrite(result_image_local_path, image_resized, [cv2.IMWRITE_JPEG_QUALITY, self["JPEG_QUALITY"]])

      self.next_content(self.media, tag, result_image_local_path, w=image_resized.shape[1], h=image_resized.shape[0])
    except Exception as e:
      exception(e, self.media)
    return self.media

  def content_type(self):
    return "image"

  def name(self):
    return "image-object-detection"
