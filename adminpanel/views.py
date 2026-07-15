from django.shortcuts import render


# ==========================
# Dashboard
# ==========================

def dashboard(request):

    context = {

        "total_users": 120,

        "total_sellers": 35,

        "pending_posts": 8,

        "pending_orders": 15,

        "revenue": "15,800,000 MMK",

        "recent_activities": [

            {
                "activity": "New Seller Registered",
                "user": "Ko Ko",
                "status": "Success",
                "time": "2 mins ago",
            },

            {
                "activity": "Product Submitted",
                "user": "Su Su",
                "status": "Pending",
                "time": "10 mins ago",
            },

            {
                "activity": "Wallet Top Up",
                "user": "Mg Mg",
                "status": "Completed",
                "time": "35 mins ago",
            },

            {
                "activity": "Account Warning",
                "user": "Aung Aung",
                "status": "Warning",
                "time": "1 hour ago",
            },

        ]

    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context
    )


# ==========================
# Pending Posts
# ==========================

def posts(request):

    pending_posts = [

        {
            "id": 1,
            "name": "Gaming Laptop",
            "seller": {"name": "Ko Ko"},
            "category": "Electronics",
            "price": "1500000",
            "quantity": 2,
            "created_at": "14 Jul 2026",
        },

        {
            "id": 2,
            "name": "Nike Shoes",
            "seller": {"name": "Su Su"},
            "category": "Fashion",
            "price": "220000",
            "quantity": 5,
            "created_at": "14 Jul 2026",
        },

        {
            "id": 3,
            "name": "iPhone 15",
            "seller": {"name": "Mg Mg"},
            "category": "Mobile",
            "price": "2800000",
            "quantity": 1,
            "created_at": "15 Jul 2026",
        },

    ]

    return render(
        request,
        "adminpanel/posts.html",
        {
            "pending_posts": pending_posts
        }
    )