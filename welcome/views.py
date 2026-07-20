from django.shortcuts import render


def welcome_view(request):

    products = [
        {
            "name": "Wireless Headphone",
            "category": "Electronics",
            "price": "45.99",
            "image": "images/headphone.jpg",
            "rating": "4.8"
        },

        {
            "name": "Summer Dress",
            "category": "Fashion",
            "price": "29.99",
            "image": "images/dress.jpg",
            "rating": "4.6"
        },

        {
            "name": "Gaming Laptop",
            "category": "Computer",
            "price": "899.99",
            "image": "images/laptop.jpg",
            "rating": "4.9"
        },

        {
            "name": "Smart Watch",
            "category": "Accessories",
            "price": "59.99",
            "image": "images/watch.jpg",
            "rating": "4.7"
        }
    ]

    context = {
        "products": products
    }

    return render(
        request,
        "welcome.html",
        context
    )

def about(request):
    return render(request, "about.html")