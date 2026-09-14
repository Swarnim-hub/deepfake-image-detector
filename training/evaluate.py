import argparse
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from dataset import DeepfakeFacesDataset, get_transforms, create_dataset_splits
from train import DeepfakeModel
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="dataset")
    parser.add_argument("--model_path", type=str, default="../backend/models/best_model.pth")
    parser.add_argument("--batch_size", type=int, default=32)
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    _, _, (test_files, test_labels) = create_dataset_splits(args.data_dir)
    test_ds = DeepfakeFacesDataset(test_files, test_labels, transform=get_transforms("test"))
    test_loader = DataLoader(test_ds, batch_size=args.batch_size, shuffle=False)

    model = DeepfakeModel(model_name="efficientnet_b0", pretrained=False)
    checkpoint = torch.load(args.model_path, map_location=device)
    if "model_state_dict" in checkpoint:
        model.load_state_dict(checkpoint["model_state_dict"])
    else:
        model.load_state_dict(checkpoint)

    model.to(device)
    model.eval()

    all_preds = []
    all_probs = []
    all_targets = []

    with torch.no_grad():
        for images, labels in tqdm(test_loader, desc="Evaluating on Test Set"):
            images = images.to(device)
            outputs = model(images).squeeze(-1)
            probs = torch.sigmoid(outputs).cpu().numpy()
            preds = (probs >= 0.5).astype(float)

            all_probs.extend(probs)
            all_preds.extend(preds)
            all_targets.extend(labels.numpy())

    print("\n--- TEST METRICS REPORT ---")
    print(classification_report(all_targets, all_preds, target_names=["Real (0)", "Fake (1)"]))
    print(f"ROC-AUC Score: {roc_auc_score(all_targets, all_probs):.4f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(all_targets, all_preds))

if __name__ == "__main__":
    main()
