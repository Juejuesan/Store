import torch

from posts.models import ItemImage
from image_search.services import get_image_embedding


def search_similar_images(image, top_k=10):
    """
    Find visually similar products.

    Each Item is returned only once.

    Returns:
        [
            (item, similarity_score, best_matching_image),
            ...
        ]
    """

    # =====================================================
    # 1. Generate embedding for uploaded/search image
    # =====================================================

    query_embedding = get_image_embedding(image)

    if not isinstance(query_embedding, torch.Tensor):
        query_embedding = torch.tensor(
            query_embedding,
            dtype=torch.float32
        )

    query_embedding = query_embedding.float()

    # Normalize query
    query_embedding = (
        query_embedding /
        query_embedding.norm(p=2)
    )

    # =====================================================
    # 2. Get images that have embeddings
    # =====================================================

    item_images = ItemImage.objects.exclude(
        embedding__isnull=True
    ).select_related("item")

    # =====================================================
    # 3. Store the BEST image for each Item
    # =====================================================

    best_results = {}

    # =====================================================
    # 4. Compare query against every product image
    # =====================================================

    for item_image in item_images:

        if not item_image.embedding:
            continue

        try:

            # Convert stored list → tensor
            product_embedding = torch.tensor(
                item_image.embedding,
                dtype=torch.float32
            )

            # Normalize stored embedding
            product_embedding = (
                product_embedding /
                product_embedding.norm(p=2)
            )

            # ---------------------------------------------
            # Cosine similarity
            # ---------------------------------------------

            similarity = torch.dot(
                query_embedding,
                product_embedding
            )

            score = similarity.item()

            item_id = item_image.item_id

            # ---------------------------------------------
            # Keep only the BEST image for each Item
            # ---------------------------------------------

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
    # 5. Convert dictionary → list
    # =====================================================

    results = list(
        best_results.values()
    )

    # =====================================================
    # 6. Highest similarity first
    # =====================================================

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # =====================================================
    # 7. Return top products
    # =====================================================

    return results[:top_k]