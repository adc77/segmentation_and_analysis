
"""
from models.segmentation_sam import SegmentationModel, EnsembleSegmentationModel
from utils.object_extraction import ObjectExtractor
from models.identification_model import IdentificationModel
import cv2
import os
import json

def main():
    # Initialize models
    seg_model = SegmentationModel()
    extractor = ObjectExtractor()
    id_model = IdentificationModel()

    # Path to input image
    input_image_path = "data/input_images/test_image6.jpg"

    # statement to see the full path being used
    print("Attempting to read image from:", os.path.abspath(input_image_path))

    # Perform segmentation
    image, masks = seg_model.segment_image(input_image_path)

    # Extract objects
    object_ids = extractor.extract_objects(image, masks)

    # Save metadata
    extractor.save_metadata()

    # Identify and describe objects
    descriptions = id_model.process_objects(extractor.output_dir)

    # Save descriptions
    with open('data/object_descriptions.json', 'w') as f:
        json.dump(descriptions, f, indent=2)

    print("Segmentation, extraction, and identification complete.")
    print(f"Extracted {len(object_ids)} objects.")
    print("Object descriptions saved to data/object_descriptions.json")

if __name__ == "__main__":
    main()

"""

from models.segmentation_sam import SegmentationModel, EnsembleSegmentationModel
from utils.object_extraction import ObjectExtractor
from models.identification_model import IdentificationModel
from models.text_extraction_model import TextExtractionModel
from models.summarization_model import SummarizationModel
import cv2
import os
import json

def main():
    # Initialize models
    seg_model = SegmentationModel()
    extractor = ObjectExtractor()
    id_model = IdentificationModel()
    text_model = TextExtractionModel()
    sum_model = SummarizationModel()  # No API key needed now

    # Path to input image
    input_image_path = "data/input_images/test_image7.jpg"

    # Perform segmentation
    image, masks = seg_model.segment_image(input_image_path)

    # statement to see the full path being used
    print("Attempting to read image from:", os.path.abspath(input_image_path))

    # adding to check
    # Visualize segmentation
    segmented_image = seg_model.visualize_segmentation(image, masks)

    # Save the segmented image
    output_path = "data/output/segmented_image.jpg"
    cv2.imwrite(output_path, cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR))

    print(f"Segmented image saved to {output_path}")

    # Extract and save individual objects
    for i, mask in enumerate(masks):
        object_image = image.copy()
        object_image[~mask] = 0

        object_path = f"data/segmented_objects/object_{i}.jpg"
        cv2.imwrite(object_path, cv2.cvtColor(object_image, cv2.COLOR_RGB2BGR))
        print(f"Object {i} saved to {object_path}")
    # adding to check

    # Extract objects
    object_ids = extractor.extract_objects(image, masks)

    # Save metadata
    extractor.save_metadata()

    #check
     # Identify and describe objects
    descriptions = id_model.process_objects(extractor.output_dir)
    #check

    # Identify objects
    identifications = id_model.process_objects(extractor.output_dir)

    # Extract text from objects
    text_data = text_model.process_objects(extractor.output_dir)

    # Summarize objects
    summaries = sum_model.process_objects(identifications, text_data)

    # Combine all data
    final_data = {}
    for object_id in object_ids:
        final_data[object_id] = {
            "identification": identifications.get(object_id, ""),
            "extracted_text": text_data.get(object_id, ""),
            "summary": summaries.get(object_id, "")
        }

    # check
    # Save descriptions
    with open('data/object_descriptions.json', 'w') as f:
        json.dump(descriptions, f, indent=2)
    #check
    
    # Save final data
    with open('data/object_analysis.json', 'w') as f:
        json.dump(final_data, f, indent=2)

    print("Segmentation, extraction, identification, text extraction, and summarization complete.")
    print(f"Analyzed {len(object_ids)} objects.")
    print("Object analysis saved to data/object_analysis.json")

if __name__ == "__main__":
    main()