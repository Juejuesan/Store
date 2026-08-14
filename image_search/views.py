from django.shortcuts import render

from image_search.search import search_similar_images


def image_search_view(request):

    results = []
    searched = False
    error_message = None

    if request.method == "POST":

        searched = True

        uploaded_image = request.FILES.get("image")

        if not uploaded_image:

            error_message = "Please select an image."

        else:

            try:

                results = search_similar_images(
                    uploaded_image,
                    top_k=10
                )

            except Exception as e:

                print(
                    "Image search error:",
                    e
                )

                error_message = (
                    "Something went wrong while "
                    "searching for similar products."
                )

    context = {
        "results": results,
        "searched": searched,
        "error_message": error_message,
    }

    return render(
        request,
        "image_search/search.html",
        context
    )