from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .form import PostForm
from .models import (
    Category,
    Item,
    ItemImage,
    Post,
    SizeVariant,
)


# =========================================================
# HELPERS
# =========================================================

def is_ajax(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def json_error(request, errors, status=400):
    return JsonResponse(
        {
            "success": False,
            "errors": errors,
        },
        status=status,
    )


def render_create_post_error(
    request,
    post_form,
    categories,
    errors,
):
    return render(
        request,
        "posts/createPost.html",
        {
            "post_form": post_form,
            "categories": categories,
            "post_form_errors": errors,
            "show_post_form_error": True,
        },
    )


def get_item_indexes(request):
    """
    Find item indexes from fields such as:

        item_name_0
        item_name_1
        item_name_2
    """

    indexes = set()

    for key in request.POST.keys():

        if key.startswith("item_name_"):

            index = key.replace("item_name_", "", 1)

            if index.isdigit():
                indexes.add(int(index))

    return sorted(indexes)


def get_item_images(request, item_index):
    """
    Get all uploaded images belonging to one item.
    """

    images = []

    for key, files in request.FILES.lists():

        if (
            key == f"images_{item_index}"
            or key.startswith(f"images_{item_index}")
        ):
            images.extend(files)

    return images


def get_integer(value, default=None):
    """
    Safely convert a value to integer.
    """

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# =========================================================
# CREATE POST
# =========================================================

@login_required
def create_post(request):

    # -----------------------------------------------------
    # BAN CHECK
    # -----------------------------------------------------

    if request.user.profile.status == "Banned":

        messages.error(
            request,
            "Your account has been banned from creating posts.",
        )

        return redirect("home")

    categories = Category.objects.all()

    # =====================================================
    # GET
    # =====================================================

    if request.method == "GET":

        return render(
            request,
            "posts/createPost.html",
            {
                "post_form": PostForm(),
                "categories": categories,
            },
        )

    # =====================================================
    # POST
    # =====================================================

    post_form = PostForm(request.POST)

    # -----------------------------------------------------
    # FORM VALIDATION
    # -----------------------------------------------------

    if not post_form.is_valid():

        errors = []

        for field, field_errors in post_form.errors.items():

            for error in field_errors:

                if field == "__all__":

                    errors.append(str(error))
                    continue

                if field in post_form.fields:

                    field_name = (
                        post_form.fields[field].label
                        or field.replace("_", " ").title()
                    )

                else:

                    field_name = field.replace(
                        "_",
                        " ",
                    ).title()

                errors.append(
                    f"{field_name}: {error}"
                )

        if not errors:

            errors.append(
                "Please check the post information and try again."
            )

        if is_ajax(request):

            return json_error(
                request,
                errors,
            )

        return render_create_post_error(
            request,
            post_form,
            categories,
            errors,
        )

    # -----------------------------------------------------
    # FIND ITEMS
    # -----------------------------------------------------

    item_indexes = get_item_indexes(request)

    if not item_indexes:

        error = "Please add at least one item to your post."

        if is_ajax(request):

            return json_error(
                request,
                [error],
            )

        return render_create_post_error(
            request,
            post_form,
            categories,
            [error],
        )

    # =====================================================
    # CATEGORY / CONDITION
    # =====================================================

    selected_category = post_form.cleaned_data.get("category")
    selected_condition = post_form.cleaned_data.get("condition")

    category_supports_sizes = (
        selected_category is not None
        and selected_category.size_type != "none"
    )

    is_new_post = selected_condition == "new"

    should_have_sizes = (
        category_supports_sizes
        and is_new_post
    )

    # =====================================================
    # VALIDATE ITEMS
    # =====================================================

    validation_errors = []

    for position, item_index in enumerate(
        item_indexes,
        start=1,
    ):

        # -------------------------------------------------
        # ITEM NAME
        # -------------------------------------------------

        item_name = request.POST.get(
            f"item_name_{item_index}",
            "",
        ).strip()

        if not item_name:

            validation_errors.append(
                f"Enter a name for Item {position}."
            )

        # -------------------------------------------------
        # ITEM DESCRIPTION
        # -------------------------------------------------

        item_description = request.POST.get(
            f"item_description_{item_index}",
            "",
        ).strip()

        if not item_description:

            validation_errors.append(
                f"Enter a description for Item {position}."
            )

        # -------------------------------------------------
        # IMAGES
        # -------------------------------------------------

        item_images = get_item_images(
            request,
            item_index,
        )

        if not item_images:

            validation_errors.append(
                f"Upload at least one image for Item {position}."
            )

        # -------------------------------------------------
        # SIZE COUNT
        # -------------------------------------------------

        size_count = get_integer(
            request.POST.get(
                f"size_count_{item_index}",
                0,
            ),
            default=0,
        )

        # =================================================
        # SIZE ITEM
        # =================================================

        if should_have_sizes:

            if size_count <= 0:

                validation_errors.append(
                    f"Select at least one size for Item {position}."
                )

            for size_index in range(size_count):

                size = request.POST.get(
                    f"size_{item_index}_{size_index}",
                    "",
                ).strip()

                quantity_raw = request.POST.get(
                    f"quantity_{item_index}_{size_index}",
                    "",
                )

                price_raw = request.POST.get(
                    f"size_price_{item_index}_{size_index}",
                    "",
                )

                # -----------------------------------------
                # SIZE
                # -----------------------------------------

                if not size:

                    validation_errors.append(
                        f"Size information is missing "
                        f"for Item {position}."
                    )

                # -----------------------------------------
                # QUANTITY
                # -----------------------------------------

                quantity = get_integer(
                    quantity_raw,
                )

                if quantity is None:

                    validation_errors.append(
                        f"Enter a valid quantity "
                        f'for size "{size}" '
                        f"in Item {position}."
                    )

                elif quantity <= 0:

                    validation_errors.append(
                        f"Enter a quantity greater than 0 "
                        f'for size "{size}" '
                        f"in Item {position}."
                    )

                # -----------------------------------------
                # PRICE
                # -----------------------------------------

                size_price = get_integer(
                    price_raw,
                )

                if size_price is None:

                    validation_errors.append(
                        f"Enter a valid price "
                        f'for size "{size}" '
                        f"in Item {position}."
                    )

                elif size_price <= 0:

                    validation_errors.append(
                        f"Enter a price greater than 0 "
                        f'for size "{size}" '
                        f"in Item {position}."
                    )

        # =================================================
        # SIMPLE ITEM
        # =================================================

        else:

            item_price = get_integer(
                request.POST.get(
                    f"item_price_{item_index}",
                    "",
                ),
            )

            simple_quantity = get_integer(
                request.POST.get(
                    f"simple_quantity_{item_index}",
                    "",
                ),
            )

            # ---------------------------------------------
            # PRICE
            # ---------------------------------------------

            if item_price is None:

                validation_errors.append(
                    f"Enter a valid price "
                    f"for Item {position}."
                )

            elif item_price <= 0:

                validation_errors.append(
                    f"Enter a price greater than 0 "
                    f"for Item {position}."
                )

            # ---------------------------------------------
            # QUANTITY
            # ---------------------------------------------

            if simple_quantity is None:

                validation_errors.append(
                    f"Enter a valid quantity "
                    f"for Item {position}."
                )

            elif simple_quantity <= 0:

                validation_errors.append(
                    f"Enter a quantity greater than 0 "
                    f"for Item {position}."
                )

    # =====================================================
    # RETURN VALIDATION ERRORS
    # =====================================================

    if validation_errors:

        if is_ajax(request):

            return json_error(
                request,
                validation_errors,
            )

        return render_create_post_error(
            request,
            post_form,
            categories,
            validation_errors,
        )

    # =====================================================
    # CREATE DATABASE RECORDS
    # =====================================================

    try:

        with transaction.atomic():

            # -------------------------------------------------
            # CREATE POST
            # -------------------------------------------------

            post = post_form.save(
                commit=False,
            )

            post.user = request.user.profile
            post.status = "pending"

            post.save()

            # -------------------------------------------------
            # CREATE ITEMS
            # -------------------------------------------------

            for item_index in item_indexes:

                item_name = request.POST.get(
                    f"item_name_{item_index}",
                    "",
                ).strip()

                item_description = request.POST.get(
                    f"item_description_{item_index}",
                    "",
                ).strip()

                size_count = get_integer(
                    request.POST.get(
                        f"size_count_{item_index}",
                        0,
                    ),
                    default=0,
                )

                has_sizes_for_item = (
                    should_have_sizes
                    and size_count > 0
                )

                # =================================================
                # SIMPLE ITEM
                # =================================================

                if not has_sizes_for_item:

                    item_price = int(
                        request.POST.get(
                            f"item_price_{item_index}",
                        )
                    )

                    simple_quantity = int(
                        request.POST.get(
                            f"simple_quantity_{item_index}",
                        )
                    )

                else:

                    item_price = 0
                    simple_quantity = 0

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

                    variant_prices = []

                    for size_index in range(size_count):

                        size = request.POST.get(
                            f"size_{item_index}_{size_index}",
                            "",
                        ).strip()

                        quantity = int(
                            request.POST.get(
                                f"quantity_{item_index}_{size_index}",
                            )
                        )

                        size_price = int(
                            request.POST.get(
                                f"size_price_{item_index}_{size_index}",
                            )
                        )

                        SizeVariant.objects.create(
                            item=item,
                            size=size,
                            quantity=quantity,
                            price=size_price,
                        )

                        variant_prices.append(
                            size_price
                        )

                    # ---------------------------------------------
                    # ITEM PRICE = LOWEST SIZE PRICE
                    # ---------------------------------------------

                    if variant_prices:

                        item.price = min(
                            variant_prices
                        )

                        item.save(
                            skip_has_sizes=True,
                        )

                # =================================================
                # CREATE ITEM IMAGES
                # =================================================

                for image in get_item_images(
                    request,
                    item_index,
                ):

                    ItemImage.objects.create(
                        item=item,
                        image=image,
                    )

    # =====================================================
    # DATABASE ERROR
    # =====================================================

    except Exception as error:

        print(
            "CREATE POST ERROR:",
            error,
        )

        error_message = (
            "Something went wrong while creating your post. "
            "Please check your information and try again."
        )

        if is_ajax(request):

            return json_error(
                request,
                [error_message],
                status=500,
            )

        return render_create_post_error(
            request,
            post_form,
            categories,
            [error_message],
        )

    # =====================================================
    # SUCCESS
    # =====================================================

    success_message = (
        "Your post has been submitted successfully "
        "and is waiting for admin approval."
    )

    messages.success(
        request,
        success_message,
        extra_tags="post-pending",
    )

    # -----------------------------------------------------
    # AJAX SUCCESS
    # -----------------------------------------------------

    if is_ajax(request):

        return JsonResponse(
            {
                "success": True,
                "message": success_message,
                "redirect_url": reverse("home"),
            }
        )

    # -----------------------------------------------------
    # NORMAL SUCCESS
    # -----------------------------------------------------

    return redirect("home")


# =========================================================
# GET CATEGORY SIZES
# =========================================================

@login_required
def get_category_sizes(
    request,
    category_id,
):

    category = get_object_or_404(
        Category,
        id=category_id,
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

    posts = (
        Post.objects
        .filter(
            user=request.user.profile,
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "posts/my_posts.html",
        {
            "posts": posts,
        },
    )