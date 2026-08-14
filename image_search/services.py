from PIL import Image
import torch

from transformers import CLIPModel, CLIPProcessor


# =========================================================
# CLIP MODEL
# =========================================================

MODEL_NAME = "openai/clip-vit-base-patch32"

_device = torch.device("cpu")

_processor = None
_model = None


def get_clip_model():
    """
    Load the CLIP processor and model only once.
    """

    global _processor
    global _model

    if _processor is None or _model is None:

        print("Loading CLIP model...")

        _processor = CLIPProcessor.from_pretrained(
            MODEL_NAME
        )

        _model = CLIPModel.from_pretrained(
            MODEL_NAME
        )

        _model.to(_device)
        _model.eval()

        print("CLIP model loaded successfully.")

    return _processor, _model


# =========================================================
# IMAGE EMBEDDING
# =========================================================

def get_image_embedding(image):
    """
    Convert an image into a normalized CLIP embedding.
    """

    processor, model = get_clip_model()

    # -----------------------------------------------------
    # Open image if necessary
    # -----------------------------------------------------

    if not isinstance(image, Image.Image):
        image = Image.open(image)

    image = image.convert("RGB")

    # -----------------------------------------------------
    # Prepare image for CLIP
    # -----------------------------------------------------

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(_device)
        for key, value in inputs.items()
    }

    # -----------------------------------------------------
    # Generate image features
    # -----------------------------------------------------

    with torch.no_grad():

        image_features = model.get_image_features(
            **inputs
        )

    # -----------------------------------------------------
    # Transformers 5.x compatibility
    #
    # Depending on the Transformers version,
    # get_image_features() may return:
    #
    # 1. Tensor
    # 2. BaseModelOutputWithPooling
    #
    # We handle both.
    # -----------------------------------------------------

    if not isinstance(image_features, torch.Tensor):

        if hasattr(image_features, "pooler_output"):
            image_features = image_features.pooler_output

        elif hasattr(image_features, "last_hidden_state"):
            image_features = image_features.last_hidden_state[:, 0]

        else:
            raise TypeError(
                "CLIP returned an unsupported output type: "
                f"{type(image_features)}"
            )

    # -----------------------------------------------------
    # Normalize embedding
    # -----------------------------------------------------

    image_features = image_features / image_features.norm(
        p=2,
        dim=-1,
        keepdim=True
    )

    return image_features.squeeze(0)