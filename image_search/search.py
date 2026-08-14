import torch

from posts.models import ItemImage
from image_search.services import get_image_embedding


def search_similar_images(image, top_k=10):
    """
    Find visually similar products.

    Returns:

        [
            (Item, similarity_score, ItemImage),
            ...
        ]

    Only the best matching image for each Item is returned.
    """

    # =====================================================
    # Generate query embedding
    # =====================================================

    query_embedding = get_image_embedding(image)

    if not isinstance(query_embedding, torch.Tensor):
        query_embedding = torch.tensor(
            query_embedding,
            dtype=torch.float32
        )

    query_embedding = query_embedding.float()

    # Normalize query embedding
    query_embedding = (
        query_embedding /
        query_embedding.norm(p=2)
    )

    # =====================================================
    # Get images with embeddings
    # =====================================================

    item_images = (
        ItemImage.objects
        .select_related("item")
        .exclude(embedding__isnull=True)
    )

    # =====================================================
    # Store best image for each Item
    # =====================================================

    best_results = {}

    # =====================================================
    # Compare images
    # =====================================================

    for item_image in item_images:

        if not item_image.embedding:
            continue

        try:

            product_embedding = torch.tensor(
                item_image.embedding,
                dtype=torch.float32
            )

            # Normalize stored embedding
            product_embedding = (
                product_embedding /
                product_embedding.norm(p=2)
            )

            # =================================================
            # Cosine similarity
            # =================================================

            similarity = torch.dot(
                query_embedding,
                product_embedding
            )

            score = similarity.item()

            item_id = item_image.item_id

            # =================================================
            # Keep only the best image for this Item
            # =================================================

            if (
                item_id not in best_results
                or score > best_results[item_id][1]
            ):

                best_results[item_id] = (
                    item_image.item,
                    score,
                    item_image
                )

        except Exception as e:

            print(
                f"Could not compare ItemImage "
                f"{item_image.id}: {e}"
            )

    # =====================================================
    # Convert dictionary to list
    # =====================================================

    results = list(
        best_results.values()
    )

    # =====================================================
    # Highest similarity first
    # =====================================================

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # =====================================================
    # Return top products
    # =====================================================

    return results[:top_k]