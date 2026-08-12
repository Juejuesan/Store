from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .form import PostForm
from .models import (
    Category,
    Post,
    Item,
    SizeVariant,
    ItemImage
)


# =========================================================
# CREATE POST
# =========================================================

@login_required
def create_post(request):
    # -----------------------------------------------------
    # BAN CHECK
    # Banned users cannot create posts
    # -----------------------------------------------------

    if request.user.profile.status == "Banned":
        messages.error(
            request,
            "Your account has been banned from creating posts."
        )

        return redirect("home")

    categories = Category.objects.all()

    # =====================================================
    # POST REQUEST
    # =====================================================

    if request.method == "POST":

        # -------------------------------------------------
        # SECOND BAN CHECK
        # Protect against direct POST requests
        # -------------------------------------------------

        if request.user.profile.status == "Banned":
            messages.error(
                request,
                "Your account has been banned from creating posts."
            )

            return redirect("home")

        post_form = PostForm(request.POST)

        # =================================================
        # FORM VALIDATION
        # =================================================

        if post_form.is_valid():

            post = post_form.save(
                commit=False
            )

            post.user = request.user.profile

            post.save()

            # =================================================
            # FIND ITEM INDEXES
            # =================================================

            item_indexes = []

            for key in request.POST.keys():

                if key.startswith("item_name_"):

                    idx = key.replace(
                        "item_name_",
                        ""
                    )

                    if idx not in item_indexes:
                        item_indexes.append(idx)

                        # =================================================
            # CATEGORY / CONDITION
            # =================================================

            category_supports_sizes = (
                    post.category.size_type != "none"
            )

            is_new_post = (
                    post.condition == "new"
            )

            # =================================================
            # PROCESS ITEMS
            # =================================================

            for i in item_indexes:

                item_name = request.POST.get(
                    f"item_name_{i}"
                )

                item_description = request.POST.get(
                    f"item_description_{i}",
                    ""
                )

                # -------------------------------------------------
                # SIZE COUNT
                # -------------------------------------------------

                try:

                    size_count = int(
                        request.POST.get(
                            f"size_count_{i}",
                            0
                        ) or 0
                    )

                except (ValueError, TypeError):

                    size_count = 0

                has_sizes_for_item = (
                        category_supports_sizes
                        and is_new_post
                        and size_count > 0
                )

                # =================================================
                # PRICE / QUANTITY
                # =================================================

                if has_sizes_for_item:

                    item_price = 0
                    simple_quantity = 0

                else:

                    raw_price = request.POST.get(
                        f"item_price_{i}",
                        "0"
                    )

                    raw_qty = request.POST.get(
                        f"item_quantity_{i}",
                        "1"
                    )

                    # -------------------------------------------------
                    # PRICE
                    # -------------------------------------------------

                    try:

                        item_price = (
                            int(raw_price)
                            if raw_price not in (None, "")
                            else 0
                        )

                    except (ValueError, TypeError):

                        item_price = 0

                        # -------------------------------------------------
                    # QUANTITY
                    # -------------------------------------------------

                    try:

                        simple_quantity = (
                            int(raw_qty)
                            if raw_qty not in (None, "")
                            else 1
                        )

                    except (ValueError, TypeError):

                        simple_quantity = 1

                        # =================================================
                # CREATE ITEM
                # =================================================

                if item_name:

                    item = Item.objects.create(

                        post=post,

                        name=item_name,

                        description=item_description,

                        price=item_price,

                        simple_quantity=simple_quantity,

                    )

                    # =================================================
                    # SIZE VARIANTS
                    # =================================================

                    if has_sizes_for_item:

                        created_variant_prices = []

                        for j in range(size_count):

                            size = request.POST.get(
                                f"size_{i}_{j}"
                            )

                            qty_raw = request.POST.get(
                                f"quantity_{i}_{j}",
                                "0"
                            )

                            price_raw = request.POST.get(
                                f"size_price_{i}_{j}",
                                "0"
                            )

                            # -------------------------------------------------
                            # QUANTITY
                            # -------------------------------------------------

                            try:

                                qty = (
                                    int(qty_raw)
                                    if qty_raw not in (None, "")
                                    else 0
                                )

                            except (ValueError, TypeError):

                                qty = 0

                                # -------------------------------------------------
                            # SIZE PRICE
                            # -------------------------------------------------

                            try:

                                size_price = (
                                    int(price_raw)
                                    if price_raw not in (None, "")
                                    else 0
                                )

                            except (ValueError, TypeError):

                                size_price = 0

                                # -------------------------------------------------
                            # CREATE SIZE VARIANT
                            # -------------------------------------------------

                            if size:
                                SizeVariant.objects.create(

                                    item=item,

                                    size=size,

                                    quantity=qty,

                                    price=size_price,

                                )

                                created_variant_prices.append(
                                    size_price
                                )

                                # =================================================
                        # SET ITEM MINIMUM PRICE
                        # =================================================

                        if created_variant_prices:

                            valid_prices = [
                                price
                                for price
                                in created_variant_prices
                                if price is not None
                            ]

                            if valid_prices:
                                item.price = min(
                                    valid_prices
                                )

                                item.save(
                                    skip_has_sizes=True
                                )

                                # =================================================
                    # ITEM IMAGES
                    # =================================================

                    for key, files in request.FILES.lists():

                        if (
                                key == f"images_{i}"
                                or key.startswith(
                            f"images_{i}"
                        )
                        ):

                            for image in files:
                                ItemImage.objects.create(

                                    item=item,

                                    image=image

                                )

                                # =================================================
            # SUCCESS
            # =================================================

            messages.success(
                request,
                "Post created successfully!"
            )

            return redirect("home")

            # =================================================
        # FORM ERRORS
        # =================================================

        else:

            print(
                "DEBUG: Form errors:",
                post_form.errors
            )

            # =====================================================
    # GET REQUEST
    # =====================================================

    else:

        post_form = PostForm()

        # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "posts/createPost.html",
        {
            "post_form": post_form,
            "categories": categories,
        }
    )


# =========================================================
# GET CATEGORY SIZES
# =========================================================

@login_required
def get_category_sizes(
        request,
        category_id
):
    category = get_object_or_404(
        Category,
        id=category_id
    )

    return JsonResponse({

        "sizes": category.get_sizes(),

        "size_label": (
                category.size_label
                or "Size"
        ),

        "size_type": category.size_type,

    })

# =========================================================
# MY POSTS
# =========================================================

@login_required
def my_posts(request):

    posts = Post.objects.filter(
        user=request.user.profile
    ).order_by("-created_at")

    return render(
        request,
        "posts/my_posts.html",
        {
            "posts": posts,
        }
    )
