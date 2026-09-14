import os
from glob import glob
from PIL import Image
import numpy as np
import torch
from torch.utils.data import Dataset
import albumentations as A
from albumentations.pytorch import ToTensorV2

def get_transforms(split="train", img_size=224):
    if split == "train":
        return A.Compose([
            A.Resize(img_size, img_size),
            A.HorizontalFlip(p=0.5),
            A.RandomRotate90(p=0.3),
            A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.1, rotate_limit=15, p=0.5),
            A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, p=0.5),
            A.ImageCompression(quality_range=(60, 100), p=0.5),
            A.GaussianBlur(blur_limit=(3, 7), p=0.3),
            A.CoarseDropout(num_holes_range=(1, 4), hole_height_range=(8, 32), hole_width_range=(8, 32), p=0.3),
            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ToTensorV2()
        ])
    else:
        return A.Compose([
            A.Resize(img_size, img_size),
            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ToTensorV2()
        ])

class DeepfakeFacesDataset(Dataset):
    """
    Dataset supporting folder structure:
      root_dir/
        real/ (label 0.0)
        fake/ (label 1.0)
    """
    def __init__(self, file_paths, labels, transform=None):
        self.file_paths = file_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        img_path = self.file_paths[idx]
        label = self.labels[idx]

        try:
            image = Image.open(img_path).convert("RGB")
            image_np = np.array(image)
        except Exception:
            # Fallback for corrupted image
            image_np = np.zeros((224, 224, 3), dtype=np.uint8)

        if self.transform:
            augmented = self.transform(image=image_np)
            image_tensor = augmented["image"]
        else:
            image_tensor = torch.tensor(image_np).permute(2, 0, 1).float() / 255.0

        return image_tensor, torch.tensor(label, dtype=torch.float32)

def create_dataset_splits(data_dir: str, val_split=0.15, test_split=0.10, seed=42):
    valid_exts = ("*.jpg", "*.jpeg", "*.png", "*.webp")
    real_files = []
    fake_files = []

    for ext in valid_exts:
        real_files.extend(glob(os.path.join(data_dir, "real", "**", ext), recursive=True))
        real_files.extend(glob(os.path.join(data_dir, "real", ext)))
        fake_files.extend(glob(os.path.join(data_dir, "fake", "**", ext), recursive=True))
        fake_files.extend(glob(os.path.join(data_dir, "fake", ext)))

    real_files = sorted(list(set(real_files)))
    fake_files = sorted(list(set(fake_files)))

    print(f"Discovered: {len(real_files)} real images, {len(fake_files)} fake images.")

    all_files = real_files + fake_files
    all_labels = [0.0] * len(real_files) + [1.0] * len(fake_files)

    from sklearn.model_selection import train_test_split
    train_files, val_test_files, train_labels, val_test_labels = train_test_split(
        all_files, all_labels, test_size=(val_split + test_split), random_state=seed, stratify=all_labels
    )

    ratio = test_split / (val_split + test_split)
    val_files, test_files, val_labels, test_labels = train_test_split(
        val_test_files, val_test_labels, test_size=ratio, random_state=seed, stratify=val_test_labels
    )

    return (train_files, train_labels), (val_files, val_labels), (test_files, test_labels)
