from django.core.management.base import BaseCommand

from posts.models import ItemImage
from image_search.services import get_image_embedding

import torch


class Command(BaseCommand):
    help = "Generate CLIP embeddings for all product images"

    def handle(self, *args, **options):

        self.stdout.write(
            self.style.SUCCESS(
                "Starting image embedding generation..."
            )
        )

        images = ItemImage.objects.all()

        total = images.count()

        if total == 0:
            self.stdout.write(
                self.style.WARNING(
                    "No ItemImage records found."
                )
            )
            return

        self.stdout.write(
            f"Found {total} product images."
        )

        success_count = 0
        skipped_count = 0
        error_count = 0

        for index, item_image in enumerate(images, start=1):

            self.stdout.write(
                f"\n[{index}/{total}] "
                f"Processing: {item_image.image.name}"
            )

            # -------------------------------------------------
            # Skip images that already have embeddings
            # -------------------------------------------------

            if item_image.embedding:
                self.stdout.write(
                    self.style.WARNING(
                        "  → Embedding already exists. Skipping."
                    )
                )

                skipped_count += 1
                continue

            # -------------------------------------------------
            # Check image file
            # -------------------------------------------------

            if not item_image.image:
                self.stdout.write(
                    self.style.ERROR(
                        "  → No image file found."
                    )
                )

                error_count += 1
                continue

            try:

                # -------------------------------------------------
                # Open image
                # -------------------------------------------------

                with item_image.image.open("rb") as image_file:

                    # -------------------------------------------------
                    # Generate CLIP embedding
                    # -------------------------------------------------

                    embedding = get_image_embedding(
                        image_file
                    )

                # -------------------------------------------------
                # Convert Tensor → Python list
                # -------------------------------------------------

                embedding_list = (
                    embedding
                    .detach()
                    .cpu()
                    .tolist()
                )

                # -------------------------------------------------
                # Save embedding
                # -------------------------------------------------

                item_image.embedding = embedding_list

                item_image.save(
                    update_fields=["embedding"]
                )

                success_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        "  ✓ Embedding generated successfully."
                    )
                )

            except Exception as e:

                error_count += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"  ✗ Error: {e}"
                    )
                )

        # ---------------------------------------------------------
        # Summary
        # ---------------------------------------------------------

        self.stdout.write("\n")
        self.stdout.write("=" * 60)
        self.stdout.write("IMAGE EMBEDDING GENERATION COMPLETE")
        self.stdout.write("=" * 60)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully processed : {success_count}"
            )
        )

        self.stdout.write(
            self.style.WARNING(
                f"Skipped                : {skipped_count}"
            )
        )

        self.stdout.write(
            self.style.ERROR(
                f"Errors                 : {error_count}"
            )
        )

        self.stdout.write("=" * 60)