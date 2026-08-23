from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from posts.models import Post
from wishlist.models import Wishlist
from cart.models import StockHold

from image_search.search import search_similar_images


@login_required(login_url='welcome')
def home(request):

    search_query = request.GET.get('q', '').strip()

    # =====================================================
    # NORMAL APPROVED POSTS
    # =====================================================

    posts = Post.objects.filter(
        status='approved'
    ).select_related(
        'category',
        'user',
        'user__user',
    ).prefetch_related(
        'items',
        'items__images',
        'items__size_variants',
    ).order_by('-created_at')  # ADD THIS

    # =====================================================
    # NORMAL TEXT SEARCH
    # Search by item name or category name
    # =====================================================

    if search_query:

        posts = posts.filter(
            Q(items__name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        ).distinct()

    # =====================================================
    # PAGINATION
    # 20 POSTS PER PAGE
    # =====================================================

    paginator = Paginator(posts, 6)

    page_number = request.GET.get('page')

    posts = paginator.get_page(page_number)

    # =====================================================
    # IMAGE SEARCH
    # =====================================================

    image_results = None
    image_search = False
    searched = False

    if request.method == "POST":

        uploaded_image = request.FILES.get("image")

        if uploaded_image:

            searched = True
            image_search = True

            try:

                image_results = search_similar_images(
                    uploaded_image,
                    top_k=10
                )

            except Exception as e:

                print(
                    f"Image search error: {e}"
                )

                image_results = []

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        'posts': posts,

        'search_query': search_query,

        'image_results': image_results,

        'image_search': image_search,

        'searched': searched,

    }

    return render(
        request,
        'home/home.html',
        context
    )


def viewdetail(request, post_id):

    # =====================================================
    # GET MAIN POST
    # =====================================================

    post = get_object_or_404(
        Post,
        id=post_id,
        status="approved"
    )

    # =====================================================
    # GET SIMILAR POSTS
    # =====================================================

    similar_posts = Post.objects.filter(
        category=post.category,
        status="approved"
    ).exclude(
        id=post.id
    )[:3]

    # =====================================================
    # GET CURRENT USER'S WISHLIST POSTS
    # =====================================================

    wishlist_post_ids = []

    if request.user.is_authenticated:

        wishlist_post_ids = Wishlist.objects.filter(
            user=request.user
        ).values_list(
            "post_id",
            flat=True
        )

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        "post": post,

        "similar_posts": similar_posts,

        "wishlist_post_ids": wishlist_post_ids,

    }

    return render(
        request,
        "home/viewdetail.html",
        context
    )


def createPost(request):

    return render(
        request,
        "posts/createPost.html"
    )


def welcome(request):

    return render(
        request,
        "welcome/welcome.html"
    )