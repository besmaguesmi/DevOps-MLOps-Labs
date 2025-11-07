import os

import matplotlib.pyplot as plt


def plot_loss_curves(train_losses, val_losses, filename, plot_dir):
    """
    Plots training and validation loss curves and saves the plot.

    Parameters:
    -----------
    train_losses : list or np.array
        Training loss values over epochs.
    val_losses : list or np.array
        Validation loss values over epochs.
    filename : str
        Name of the model's considering backbone used, included in the plot title.
    plot_dir : str
        Directory path to save the plotted loss curves.

    Returns:
    --------
    None
    """
    epochs = range(1, len(train_losses) + 1)
    # Plot losses
    plt.figure(figsize=(10, 2))
    plt.plot(epochs, train_losses, label='Train Loss')
    plt.plot(epochs, val_losses, label='Val Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, f"{filename}.png"))
    # plt.show()
