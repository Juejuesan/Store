from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from unicodedata import category

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

    # =========================================================
    # GET REQUEST
    # =========================================================

    if request.method == "GET":

        post_form = PostForm()

        return render(
            request,
            "posts/createPost.html",
            {
                "post_form": post_form,
                "categories": categories,
            }
        )

    # =========================================================
    # POST REQUEST
    # =========================================================

    # -----------------------------------------------------
    # SECOND BAN CHECK
    # Protect against direct POST requests
    # -----------------------------------------------------

    if request.user.profile.status == "Banned":
        messages.error(
            request,
            "Your account has been banned from creating posts."
        )

        return redirect("home")

    post_form = PostForm(request.POST)

    # =========================================================
    # CHECK POST FORM
    # =========================================================

    if not post_form.is_valid():

        error_messages = []

        for field, errors in post_form.errors.items():

            for error in errors:

                if field == "__all__":

                    error_messages.append(str(error))

                else:

                    if field in post_form.fields:

                        field_name = (
                            post_form
                            .fields[field]
                            .label
                            or field.replace("_", " ").title()
                        )

                    else:

                        field_name = (
                            field
                            .replace("_", " ")
                            .title()
                        )

                    error_messages.append(
                        f"{field_name}: {error}"
                    )

        if not error_messages:

            error_messages.append(
                "Please check the post information and try again."
            )

        # -----------------------------------------------------
        # AJAX RESPONSE
        # -----------------------------------------------------

        if request.headers.get(
            "X-Requested-With"
        ) == "XMLHttpRequest":

            return JsonResponse(
                {
                    "success": False,
                    "errors": error_messages,
                },
                status=400
            )

        # -----------------------------------------------------
        # NORMAL RESPONSE
        # -----------------------------------------------------

        return render(
            request,
            "posts/createPost.html",
            {
                "post_form": post_form,
                "categories": categories,
                "post_form_errors": error_messages,
                "show_post_form_error": True,
            }
        )

    # =========================================================
    # FIND ITEM INDEXES
    # =========================================================

    item_indexes = []

    for key in request.POST.keys():

        if key.startswith("item_name_"):

            idx = key.replace(
                "item_name_",
                ""
            )

            if idx not in item_indexes:
                item_indexes.append(idx)

    # ---------------------------------------------------------
    # NO ITEMS
    # ---------------------------------------------------------

    if not item_indexes:

        error_message = (
            "Please add at least one item to your post."
        )

        if request.headers.get(
            "X-Requested-With"
        ) == "XMLHttpRequest":

            return JsonResponse(
                {
                    "success": False,
                    "errors": [error_message],
                },
                status=400
            )

        return render(
            request,
            "posts/createPost.html",
            {
                "post_form": post_form,
                "categories": categories,
                "post_form_errors": [error_message],
                "show_post_form_error": True,
            }
        )

    # =========================================================
    # PREPARE CATEGORY / CONDITION
    # =========================================================

    category = post_form.cleaned_data.get("category")
    condition = post_form.cleaned_data.get("condition")

    category_supports_sizes = (
        category is not None
        and category.size_type != "none"
    )

    is_new_post = (
        condition == "new"
    )

    should_have_sizes = (
        category_supports_sizes
        and is_new_post
    )

    # =========================================================
    # VALIDATE EVERY ITEM
    # BEFORE CREATING DATABASE RECORDS
    # =========================================================

    validation_errors = []

    for position, i in enumerate(
        item_indexes,
        start=1
    ):

        # -----------------------------------------------------
        # ITEM NAME
        # -----------------------------------------------------

        item_name = request.POST.get(
            f"item_name_{i}",
            ""
        ).strip()

        if not item_name:

            validation_errors.append(
                f"Enter a name for Item {position}."
            )

        # -----------------------------------------------------
        # ITEM DESCRIPTION
        # -----------------------------------------------------

        item_description = request.POST.get(
            f"item_description_{i}",
            ""
        ).strip()

        if not item_description:

            validation_errors.append(
                f"Enter a description for Item {position}."
            )

        # -----------------------------------------------------
        # IMAGE VALIDATION
        # -----------------------------------------------------

        item_images = []

        for key, files in request.FILES.lists():

            if (
                key == f"images_{i}"
                or key.startswith(f"images_{i}")
            ):

                item_images.extend(files)

        if not item_images:

            validation_errors.append(
                f"Upload at least one image for Item {position}."
            )

        # -----------------------------------------------------
        # SIZE COUNT
        # -----------------------------------------------------

        size_count_raw = request.POST.get(
            f"size_count_{i}",
            "0"
        )

        try:

            size_count = int(
                size_count_raw or 0
            )

        except (TypeError, ValueError):

            size_count = 0

        # =====================================================
        # SIZE-BASED ITEM
        # =====================================================

        if should_have_sizes:

            if size_count <= 0:

                validation_errors.append(
                    f"Select at least one size for Item {position}."
                )

            for j in range(size_count):

                size = request.POST.get(
                    f"size_{i}_{j}",
                    ""
                ).strip()

                quantity_raw = request.POST.get(
                    f"quantity_{i}_{j}",
                    ""
                )

                price_raw = request.POST.get(
                    f"size_price_{i}_{j}",
                    ""
                )

                # -------------------------------------------------
                # SIZE NAME
                # -------------------------------------------------

                if not size:

                    validation_errors.append(
                        f"Size information is missing for Item {position}."
                    )

                # -------------------------------------------------
                # QUANTITY
                # -------------------------------------------------

                try:

                    quantity = int(
                        quantity_raw
                    )

                    if quantity <= 0:

                        validation_errors.append(
                            f'Enter a quantity greater than 0 '
                            f'for size "{size}" in Item {position}.'
                        )

                except (TypeError, ValueError):

                    validation_errors.append(
                        f'Enter a valid quantity '
                        f'for size "{size}" in Item {position}.'
                    )

                # -------------------------------------------------
                # SIZE PRICE
                # -------------------------------------------------

                try:

                    size_price = int(
                        price_raw
                    )

                    if size_price <= 0:

                        validation_errors.append(
                            f'Enter a price greater than 0 '
                            f'for size "{size}" in Item {position}.'
                        )

                except (TypeError, ValueError):

                    validation_errors.append(
                        f'Enter a valid price '
                        f'for size "{size}" in Item {position}.'
                    )

        # =====================================================
        # SIMPLE ITEM WITHOUT SIZES
        # =====================================================

        else:

            raw_price = request.POST.get(
                f"item_price_{i}",
                ""
            )

            raw_quantity = request.POST.get(
                f"simple_quantity_{i}",
                ""
            )

            # -------------------------------------------------
            # PRICE
            # -------------------------------------------------

            try:

                item_price = int(
                    raw_price
                )

                if item_price <= 0:

                    validation_errors.append(
                        f"Enter a price greater than 0 "
                        f"for Item {position}."
                    )

            except (TypeError, ValueError):

                validation_errors.append(
                    f"Enter a valid price "
                    f"for Item {position}."
                )

            # -------------------------------------------------
            # QUANTITY
            # -------------------------------------------------

            try:

                simple_quantity = int(
                    raw_quantity
                )

                if simple_quantity <= 0:

                    validation_errors.append(
                        f"Enter a quantity greater than 0 "
                        f"for Item {position}."
                    )

            except (TypeError, ValueError):

                validation_errors.append(
                    f"Enter a valid quantity "
                    f"for Item {position}."
                )

    # =========================================================
    # RETURN VALIDATION ERRORS
    # =========================================================

    if validation_errors:

        if request.headers.get(
            "X-Requested-With"
        ) == "XMLHttpRequest":

            return JsonResponse(
                {
                    "success": False,
                    "errors": validation_errors,
                },
                status=400
            )

        return render(
            request,
            "posts/createPost.html",
            {
                "post_form": post_form,
                "categories": categories,
                "post_form_errors": validation_errors,
                "show_post_form_error": True,
            }
        )

    # =========================================================
    # EVERYTHING IS VALID
    # NOW CREATE THE POST
    # =========================================================

    try:

        with transaction.atomic():

            # -------------------------------------------------
            # CREATE POST
            # -------------------------------------------------

            post = post_form.save(
                commit=False
            )

            post.user = request.user.profile

            post.save()

            # -------------------------------------------------
            # CREATE ITEMS
            # -------------------------------------------------

            for i in item_indexes:

                item_name = request.POST.get(
                    f"item_name_{i}",
                    ""
                ).strip()

                item_description = request.POST.get(
                    f"item_description_{i}",
                    ""
                ).strip()

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

                except (TypeError, ValueError):

                    size_count = 0

                has_sizes_for_item = (
                    should_have_sizes
                    and size_count > 0
                )

                # -------------------------------------------------
                # PRICE / QUANTITY
                # -------------------------------------------------

                if has_sizes_for_item:

                    item_price = 0
                    simple_quantity = 0

                else:

                    item_price = int(
                        request.POST.get(
                            f"item_price_{i}"
                        )
                    )

                    simple_quantity = int(
                        request.POST.get(
                            f"simple_quantity_{i}"
                        )
                    )

                # -------------------------------------------------
                # CREATE ITEM
                # -------------------------------------------------

                item = Item.objects.create(
                    post=post,
                    name=item_name,
                    description=item_description,
                    price=item_price,
                    simple_quantity=simple_quantity,
                )

                # =================================================
                # CREATE SIZE VARIANTS
                # =================================================

                if has_sizes_for_item:

                    created_variant_prices = []

                    for j in range(size_count):

                        size = request.POST.get(
                            f"size_{i}_{j}"
                        )

                        quantity = int(
                            request.POST.get(
                                f"quantity_{i}_{j}"
                            )
                        )

                        size_price = int(
                            request.POST.get(
                                f"size_price_{i}_{j}"
                            )
                        )

                        SizeVariant.objects.create(
                            item=item,
                            size=size,
                            quantity=quantity,
                            price=size_price,
                        )

                        created_variant_prices.append(
                            size_price
                        )

                    # -------------------------------------------------
                    # SET ITEM PRICE TO LOWEST SIZE PRICE
                    # -------------------------------------------------

                    if created_variant_prices:

                        min_price = min(
                            created_variant_prices
                        )

                        item.price = min_price

                        item.save(
                            skip_has_sizes=True
                        )

                # =================================================
                # CREATE ITEM IMAGES
                # =================================================

                for key, files in request.FILES.lists():

                    if (
                        key == f"images_{i}"
                        or key.startswith(f"images_{i}")
                    ):

                        for image in files:

                            ItemImage.objects.create(
                                item=item,
                                image=image
                            )

    # =========================================================
    # DATABASE ERROR
    # =========================================================

    except Exception as error:

        print(
            "CREATE POST ERROR:",
            error
        )

        error_message = (
            "Something went wrong while creating your post. "
            "Please check your information and try again."
        )

        if request.headers.get(
            "X-Requested-With"
        ) == "XMLHttpRequest":

            return JsonResponse(
                {
                    "success": False,
                    "errors": [error_message],
                },
                status=500
            )

        return render(
            request,
            "posts/createPost.html",
            {
                "post_form": post_form,
                "categories": categories,
                "post_form_errors": [error_message],
                "show_post_form_error": True,
            }
        )

    # =========================================================
    # SUCCESS
    # =========================================================

    success_message = (
        "Your post has been submitted successfully "
        "and is waiting for admin approval."
    )

    messages.success(
        request,
        success_message,
        extra_tags="post-pending"
    )

    # =========================================================
    # AJAX SUCCESS
    # =========================================================

    if request.headers.get(
        "X-Requested-With"
    ) == "XMLHttpRequest":

        return JsonResponse(
            {
                "success": True,
                "message": success_message,
                "redirect_url": "/home/",
            }
        )

    # =========================================================
    # NORMAL SUCCESS
    # =========================================================

    return redirect("home")


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

    return JsonResponse(
        {
            "sizes": category.get_sizes(),

            "size_label": (
                category.size_label
                or "Size"
            ),

            "size_type": category.size_type,
        }
    )


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