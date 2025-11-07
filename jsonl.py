import os
import json
import random

# --- CONFIGURATION (MUST BE UPDATED LOCALLY) ---
# 1. Bucket and Prefixes: This is the exact GCS path where you WILL upload the files later.
# This structure must match where you plan to upload your 'images/' and 'masks/' folders.
GCS_BUCKET = "ds-ml-data"
GCS_IMAGE_PREFIX = "shipdata/images/"
GCS_MASK_PREFIX = "shipdata/masks/"

# 2. Local Directories: The folders where your files currently live
LOCAL_IMAGE_DIR = "images"
LOCAL_MASK_DIR = "masks" # Only used to verify mask folder exists

# 3. Output Configuration
OUTPUT_FILE_NAME = "segmentation_import_file.jsonl"
SEGMENTATION_LABEL = "ship_segment"
# --------------------------------------------------

def create_local_jsonl(gcs_bucket, gcs_img_prefix, gcs_mask_prefix, local_img_dir, local_mask_dir, output_file, label):
    """
    Generates a JSONL file locally, creating GCS paths based on the final upload location.
    """
    if not os.path.isdir(local_img_dir):
        print(f"Error: Image directory not found at '{local_img_dir}'")
        return
    if not os.path.isdir(local_mask_dir):
        print(f"Error: Mask directory not found at '{local_mask_dir}'")
        return

    # 1. List files from the local images directory
    file_names = [f for f in os.listdir(local_img_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    total_files = len(file_names)

    if total_files == 0:
        print(f"Error: Found 0 image files in '{local_img_dir}'. Check extensions.")
        return

    print(f"Found {total_files} image files. Generating JSONL...")

    # --- 2. Prepare Data Split (Random 80/10/10 split) ---
    indices = list(range(total_files))
    random.shuffle(indices)

    train_end = int(total_files * 0.8)
    val_end = train_end + int(total_files * 0.1)

    jsonl_data = []

    # 3. Write JSONL file
    with open(output_file, 'w') as f:
        for i in range(total_files):
            filename = file_names[indices[i]]

            # Check if mask file exists locally (optional but recommended check)
            if not os.path.exists(os.path.join(local_mask_dir, filename)):
                print(f"Warning: Mask not found for {filename}. Skipping.")
                continue

            # Assign ML use based on shuffled position
            if i < train_end:
                ml_use = "training"
            elif i < val_end:
                ml_use = "validation"
            else:
                ml_use = "test"

            # NOTE: These paths reference the future location in GCS
            data_item = {
                "imageGcsUri": f"gs://{gcs_bucket}/{gcs_img_prefix}{filename}",
                "segmentationAnnotation": {
                    "displayName": label,
                    "maskGcsUri": f"gs://{gcs_bucket}/{gcs_mask_prefix}{filename}"
                },
                "dataItemResourceLabels": {
                    "aiplatform.googleapis.com/ml_use": ml_use
                }
            }
            f.write(json.dumps(data_item) + '\n')
            jsonl_data.append(json.dumps(data_item))

    print("-" * 70)
    print(f"✅ Successfully created local file: {output_file} with {len(jsonl_data)} rows.")
    print("Next step: Upload your 'images', 'masks', and the 'jsonl' file to GCS.")
    print("-" * 70)

if __name__ == "__main__":
    create_local_jsonl(
        gcs_bucket=GCS_BUCKET,
        gcs_img_prefix=GCS_IMAGE_PREFIX,
        gcs_mask_prefix=GCS_MASK_PREFIX,
        local_img_dir=LOCAL_IMAGE_DIR,
        local_mask_dir=LOCAL_MASK_DIR,
        output_file=OUTPUT_FILE_NAME,
        label=SEGMENTATION_LABEL
    )
