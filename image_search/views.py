from django.shortcuts import render

from image_search.search import search_similar_images


def image_search_view(request):

    results = []
    searched = False
    error = None

    if request.method == "POST":

        searched = True

        uploaded_image = request.FILES.get("image")

        if not uploaded_image:
            error = "Please select an image."

        else:
            try:

                results = search_similar_images(
                    uploaded_image,
                    top_k=10
                )

            except Exception as e:

                print("Image search error:", e)

                error = (
                    "Something went wrong while searching. "
                    "Please try another image."
                )

    context = {
        "results": results,
        "searched": searched,
        "error": error,
    }

    return render(
        request,
        "image_search/search.html",
        context
    )