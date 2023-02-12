import fiftyone as fo
import fiftyone.zoo as foz

dataset = foz.load_zoo_dataset(
    "coco-2017",
    split="validation",
    label_types=["detections", "segmentations"],
    dataset_name="evaluate-detections-tutorial",
    classes=["sports ball"],
)

dataset.persistent = True

# Print some information about the dataset
print(dataset)

# Print a ground truth detection
sample = dataset.first()
print(sample.ground_truth.detections[0])