from ultralytics import YOLO

model = YOLO("yolov10n.pt")

result = model.train(data = "/disk2/ingrj/config.yaml",
                    project="runs/train",
                    name="pokus2",
                    epochs=90,
                    batch=16,
                    imgsz=960,
                    lr0=0.01,
                    scale=1.0,
                    optimizer='AdamW',
                    patience=20,
                    momentum=0.937,
                    weight_decay=0.0005,
                    fliplr=0.5,
                    flipud=0.5,
                    mosaic=1.0,
                    augment=True)