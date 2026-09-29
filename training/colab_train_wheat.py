"""Google Colab training script for Kishan Mitra Wheat Phase 1.

Before running, place these files in Google Drive:
  MyDrive/KishanMitra/models/best_v2.pt
  MyDrive/KishanMitra/datasets/wheat_dataset.zip

Expected ZIP layout:
  wheat_dataset/
    images/train, images/val, images/test
    labels/train, labels/val, labels/test

Run this file from a Colab GPU runtime. It never overwrites best_v2.pt.
"""

import shutil
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path


def install_dependencies():
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-q", "ultralytics>=8.3,<9"]
    )


install_dependencies()

from google.colab import drive  # noqa: E402
from ultralytics import YOLO  # noqa: E402


CLASSES = [
    "healthy_wheat",
    "wheat_aphid",
    "wheat_pink_stem_borer",
    "wheat_armyworm",
    "wheat_brown_mite",
    "wheat_rust",
    "wheat_smut",
]

DRIVE_ROOT = Path("/content/drive/MyDrive/KishanMitra")
BASE_MODEL = DRIVE_ROOT / "models" / "best_v2.pt"
DATASET_ZIP = DRIVE_ROOT / "datasets" / "wheat_dataset.zip"
DRIVE_OUTPUT = DRIVE_ROOT / "models" / "wheat_v3"

WORK_ROOT = Path("/content/kishan_mitra_wheat")
EXTRACT_ROOT = WORK_ROOT / "dataset"
RUNS_ROOT = DRIVE_OUTPUT / "runs"
RUN_NAME = "wheat_v3"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def require_file(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"Required file is missing: {path}")


def locate_dataset_root(extract_root: Path) -> Path:
    candidates = [extract_root, *[p for p in extract_root.rglob("*") if p.is_dir()]]
    for candidate in candidates:
        if (candidate / "images" / "train").is_dir() and (candidate / "labels" / "train").is_dir():
            return candidate
    raise FileNotFoundError(
        "Could not find images/train and labels/train inside the dataset ZIP."
    )


def extract_zip_safely(zip_path: Path, destination: Path):
    destination_resolved = destination.resolve()
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            if destination_resolved not in target.parents and target != destination_resolved:
                raise ValueError(f"Unsafe path in dataset archive: {member.filename}")
        archive.extractall(destination)


def validate_dataset(dataset_root: Path):
    errors = []
    summary = {}
    class_counts = Counter()

    for split in ("train", "val", "test"):
        image_dir = dataset_root / "images" / split
        label_dir = dataset_root / "labels" / split

        if split in {"train", "val"} and not image_dir.is_dir():
            errors.append(f"Missing required image directory: {image_dir}")
            continue
        if not image_dir.is_dir():
            continue
        if not label_dir.is_dir():
            errors.append(f"Missing label directory: {label_dir}")
            continue

        images = sorted(p for p in image_dir.rglob("*") if p.suffix.lower() in IMAGE_EXTENSIONS)
        labeled_images = 0
        empty_labels = 0

        for image_path in images:
            relative = image_path.relative_to(image_dir).with_suffix(".txt")
            label_path = label_dir / relative
            if not label_path.exists():
                # Ultralytics treats a missing label as a background image.
                continue

            labeled_images += 1
            rows = [row.strip() for row in label_path.read_text(encoding="utf-8").splitlines() if row.strip()]
            if not rows:
                empty_labels += 1

            for line_number, row in enumerate(rows, start=1):
                fields = row.split()
                if len(fields) != 5:
                    errors.append(f"{label_path}:{line_number}: expected 5 values, found {len(fields)}")
                    continue
                try:
                    class_id = int(fields[0])
                    coordinates = [float(value) for value in fields[1:]]
                except ValueError:
                    errors.append(f"{label_path}:{line_number}: non-numeric YOLO label")
                    continue
                if not 0 <= class_id < len(CLASSES):
                    errors.append(f"{label_path}:{line_number}: invalid class id {class_id}")
                if any(value < 0 or value > 1 for value in coordinates):
                    errors.append(f"{label_path}:{line_number}: coordinates must be between 0 and 1")
                if coordinates[2] <= 0 or coordinates[3] <= 0:
                    errors.append(f"{label_path}:{line_number}: width and height must be positive")
                class_counts[class_id] += 1

        summary[split] = {
            "images": len(images),
            "images_with_label_files": labeled_images,
            "empty_label_files": empty_labels,
            "background_images": len(images) - labeled_images + empty_labels,
        }

    if not summary.get("train", {}).get("images"):
        errors.append("The training split contains no images.")
    if not summary.get("val", {}).get("images"):
        errors.append("The validation split contains no images.")

    print("\nDataset summary")
    for split, values in summary.items():
        print(f"  {split}: {values}")
    print("\nBounding-box counts")
    for class_id, class_name in enumerate(CLASSES):
        print(f"  {class_id}: {class_name}: {class_counts[class_id]}")

    missing_classes = [CLASSES[i] for i in range(len(CLASSES)) if class_counts[i] == 0]
    if missing_classes:
        errors.append(f"Classes with no bounding boxes: {', '.join(missing_classes)}")

    if errors:
        preview = "\n".join(f"- {message}" for message in errors[:100])
        raise ValueError(f"Dataset validation failed with {len(errors)} issue(s):\n{preview}")


def write_dataset_yaml(dataset_root: Path) -> Path:
    yaml_path = WORK_ROOT / "wheat_data.yaml"
    names = "\n".join(f"  {index}: {name}" for index, name in enumerate(CLASSES))
    test_line = "test: images/test\n" if (dataset_root / "images" / "test").is_dir() else ""
    yaml_path.write_text(
        f"path: {dataset_root}\n"
        "train: images/train\n"
        "val: images/val\n"
        f"{test_line}"
        "names:\n"
        f"{names}\n",
        encoding="utf-8",
    )
    return yaml_path


def main():
    drive.mount("/content/drive")
    require_file(BASE_MODEL)
    require_file(DATASET_ZIP)

    if WORK_ROOT.exists():
        shutil.rmtree(WORK_ROOT)
    EXTRACT_ROOT.mkdir(parents=True)
    RUNS_ROOT.mkdir(parents=True)
    DRIVE_OUTPUT.mkdir(parents=True, exist_ok=True)

    print(f"Extracting {DATASET_ZIP}...")
    extract_zip_safely(DATASET_ZIP, EXTRACT_ROOT)

    dataset_root = locate_dataset_root(EXTRACT_ROOT)
    print(f"Dataset root: {dataset_root}")
    validate_dataset(dataset_root)
    data_yaml = write_dataset_yaml(dataset_root)

    run_dir = RUNS_ROOT / RUN_NAME
    resume_checkpoint = run_dir / "weights" / "last.pt"

    if resume_checkpoint.exists():
        print(f"Resuming interrupted training from {resume_checkpoint}")
        model = YOLO(str(resume_checkpoint))
        model.train(resume=True)
    else:
        # Fine-tune from v2 without overwriting the original file.
        model = YOLO(str(BASE_MODEL))
        model.train(
            data=str(data_yaml),
            epochs=100,
            imgsz=640,
            batch=-1,
            patience=20,
            device=0,
            workers=2,
            optimizer="auto",
            seed=42,
            deterministic=True,
            cache=False,
            pretrained=True,
            project=str(RUNS_ROOT),
            name=RUN_NAME,
            exist_ok=True,
            save_period=5,
            plots=True,
            verbose=True,
        )

    best_model = run_dir / "weights" / "best.pt"
    last_model = run_dir / "weights" / "last.pt"
    require_file(best_model)

    # Evaluate the best checkpoint, not merely the last epoch.
    best = YOLO(str(best_model))
    metrics = best.val(data=str(data_yaml), split="val", plots=True)
    print(f"Validation mAP50: {metrics.box.map50:.4f}")
    print(f"Validation mAP50-95: {metrics.box.map:.4f}")

    if (dataset_root / "images" / "test").is_dir():
        test_metrics = best.val(data=str(data_yaml), split="test", plots=True)
        print(f"Test mAP50: {test_metrics.box.map50:.4f}")
        print(f"Test mAP50-95: {test_metrics.box.map:.4f}")

    final_model = DRIVE_OUTPUT / "best_wheat_v3.pt"
    final_last = DRIVE_OUTPUT / "last_wheat_v3.pt"
    shutil.copy2(best_model, final_model)
    if last_model.exists():
        shutil.copy2(last_model, final_last)

    print("\nTraining complete")
    print(f"Best model: {final_model}")
    print(f"Training artifacts: {run_dir}")
    print("The original best_v2.pt was not modified.")


if __name__ == "__main__":
    main()
