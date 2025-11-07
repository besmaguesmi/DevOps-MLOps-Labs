import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import torch
from sklearn.metrics import confusion_matrix, classification_report


def test_classifier(model, test_loader, plot_dir, backbone, freeze_backbone, class_names, device):
    """
    Evaluates the model on labeled data or runs inference on unlabeled data and saves the results.

    Parameters:
    -----------
    model : nn.Module
        The trained model to evaluate or use for inference.
    test_loader : DataLoader
        DataLoader for the test dataset.
    plot_dir : str
        Directory path to save evaluation plots (only used for evaluation).
    backbone : str
        Name of the model's backbone architecture.
    freeze_backbone : bool
        Whether to freeze the backbone layers during training.
    class_names : list
        List of class names (e.g., 'sea', 'forest').
    device : torch.device
        Device to run the evaluation on (e.g., 'cpu' or 'cuda').

    Returns:
    --------
    None
    """
    # Set the model to evaluation mode
    model.eval()
    # For evaluation, we need to track accuracy, confusion matrix, etc.
    correct_preds = 0
    incorrect_preds = 0
    total_samples = 0
    true_labels = []
    predictions = []

    # CUDA memory consumption (if using GPU)
    if device.type == 'cuda':
        torch.cuda.reset_max_memory_allocated(device)

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device).long()

            # Forward pass through the model
            output = model(images).to(device)

            # Get predictions
            _, pred = output.max(1)

            # Compute accuracy
            correct_preds += pred.eq(labels).sum().item()
            incorrect_preds += (pred != labels).sum().item()
            total_samples += labels.size(0)

            # Collect true labels and predictions for metrics
            true_labels.extend(labels.cpu().numpy())
            predictions.extend(pred.cpu().numpy())

    # Evaluation metrics
    accuracy = correct_preds / total_samples
    wrong_pred = incorrect_preds / total_samples

    logging.info(f"Mis-classification rate: {wrong_pred * 100:.2f}%, Accuracy: {accuracy * 100:.2f}%")

    # Confusion matrix and classification report
    cm = confusion_matrix(true_labels, predictions)
    class_report = classification_report(true_labels, predictions, output_dict=True)
    class_report_df = pd.DataFrame(class_report).transpose()
    logging.info("Confusion Matrix:\n%s", pd.DataFrame(cm))
    logging.info("Class Report:\n%s", class_report_df)

    # Plot confusion matrix
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, xticklabels=class_names, yticklabels=class_names)
    plt.ylabel('True Labels')
    plt.xlabel('Predicted Labels')
    plt.title('Confusion Matrix')
    plt.savefig(os.path.join(plot_dir, f"cm_{backbone}_freeze_backbone_{freeze_backbone}.png"))
    plt.show()
