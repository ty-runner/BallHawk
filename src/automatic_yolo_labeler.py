import os
import shutil
from pathlib import Path
import cv2
import numpy as np
from ultralytics import YOLO


def main():
    print("Starting the labeling process...")

    model = YOLO("yolov8x-seg.pt")
    data_dir = Path("./data")
    segmentation_labels_dir = Path("./labels/seg")
    bounding_box_labels_dir = Path("./labels/bbox")
    shutil.rmtree(segmentation_labels_dir)
    shutil.rmtree(bounding_box_labels_dir)

    os.makedirs(segmentation_labels_dir, exist_ok=True)
    os.makedirs(bounding_box_labels_dir, exist_ok=True)

    images = os.listdir(data_dir)
    images = [os.path.join(data_dir, image) for image in images]

    for image in images:
        result = model(image)[0]
        image_name = Path(result.path).stem

        # SEGMENTATION
        connected_mask = np.zeros((640, 640), dtype=np.uint8)
        if result.masks is not None:
            for mask in result.masks.data.cpu().numpy():
                connected_mask += mask.astype(np.uint8)

            connected_mask[connected_mask > 0] = 1

        H, W, _ = cv2.imread(image).shape
        connected_mask = cv2.resize(connected_mask, (W, H))
        cv2.imwrite(
            str(segmentation_labels_dir / (image_name + ".png")), connected_mask
        )

        # BOUNDING BOXES
        with open(bounding_box_labels_dir / (image_name + ".txt"), "a") as f:
            if result.boxes is not None:
                for box in result.boxes.xywhn.data.cpu().numpy():
                    x1, y1, w, h = box
                    f.write(f"0 {x1} {y1} {w} {h}\n")

    print("Labeling complete!")


if __name__ == "__main__":
    main()
