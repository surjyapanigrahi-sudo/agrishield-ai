# Kishan Mitra Wheat Phase 1 — Google Colab

## 1. Prepare Google Drive

Create this structure:

```text
MyDrive/
└── KishanMitra/
    ├── datasets/
    │   └── wheat_dataset.zip
    └── models/
        └── best_v2.pt
```

The dataset ZIP must contain:

```text
wheat_dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

Each label row must use YOLO detection format:

```text
class_id x_center y_center width height
```

All coordinates must be normalized between 0 and 1.

## 2. Class IDs

Do not change this order after annotation begins:

```text
0 healthy_wheat
1 wheat_aphid
2 wheat_pink_stem_borer
3 wheat_armyworm
4 wheat_brown_mite
5 wheat_rust
6 wheat_smut
```

## 3. Start Colab

1. Open Google Colab.
2. Select **Runtime > Change runtime type**.
3. Choose a GPU runtime.
4. Upload `colab_train_wheat.py` to the Colab session.
5. Run:

```python
!python colab_train_wheat.py
```

The notebook will request access to Google Drive.

## 4. Output

Successful training writes:

```text
MyDrive/KishanMitra/models/wheat_v3/best_wheat_v3.pt
MyDrive/KishanMitra/models/wheat_v3/last_wheat_v3.pt
MyDrive/KishanMitra/models/wheat_v3/runs/wheat_v3/
```

The original `best_v2.pt` is read-only input and is never overwritten.
Checkpoints are written to Google Drive every five epochs. If Colab disconnects,
run the same script again and it will resume from `last.pt`.

## 5. Important checks

- Keep photos from the same farm, video, or burst in only one split.
- Do not put augmented copies of one image in different splits.
- Review bounding boxes manually before training.
- Keep a truly unseen test split.
- Do not deploy solely from overall mAP; inspect per-class recall and the confusion matrix.
