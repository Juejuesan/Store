from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction

from .form import PostForm

from .models import (
    Category,
    Post,
    Item,
    SizeVariant,
    ItemImage,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def is_ajax(request):
    """
    Check whether the request was sent through AJAX.
    """
    return request.headers.get(
        "X-Requested-With"
    ) == "XMLHttpRequest"


def get_item_indexes(request):
    """
    Get all item indexes from POST data.

    Example:
        item_name_0
        item_name_1
        item_name_2

    Returns:
        ['0', '1', '2']
    """

    item_indexes = []

    for key in request.POST.keys():

        if key.startswith("item_name_"):

            index = key.replace(
                "item_name_",
                "",
                1
            )

            if index.isdigit() and index not in item_indexes:

                item_indexes.append(index)

    return item_indexes


def get_item_images(request, item_index):
    """
    Get uploaded images for exactly one item.

    IMPORTANT:
    We use exact key matching so that:

        images_1

    does NOT accidentally include:

        images_10
        images_11
        etc.
    """

    field_name = f"images_{item_index}"

    return request.FILES.getlist(
        field_name
    )


def form_error_messages(post_form):
    """
    Convert Django form errors into readable messages.
    """

    error_messages = []

    for field, errors in post_form.errors.items():

        for error in errors:

            if field == "__all__":

                error_messages.append(
                    str(error)
                )

            else:

                if field in post_form.fields:

                    field_name = (
                        post_form
                        .fields[field]
                        .label
                        or field.replace(
                            "_",
                            " "
                        ).title()
                    )

                else:

                    field_name = (
                        field
                        .replace(
                            "_",
                            " "
                        )
                        .title()
                    )

                error_messages.append(
                    f"{field_name}: {error}"
                )

    if not error_messages:

        error_messages.append(
            "Please check the post information and try again."
        )

    return error_messages


def return_validation_error(
    request,
    message,
    post_form,
    categories
):
    """
    Return validation error either as AJAX JSON
    or normal HTML response.
    """

    if is_ajax(request):

        return JsonResponse(
            {
                "success": False,
                "errors": [message],
            },
            status=400
        )

    return render(
        request,
        "posts/createPost.html",
        {
            "post_form": post_form,
            "categories": categories,
            "post_form_errors": [message],
            "show_post_form_error": True,
        }
    )


def return_validation_errors(
    request,
    errors,
    post_form,
    categories
):
    """
    Return multiple validation errors.
    """

    if is_ajax(request):

        return JsonResponse(
            {
                "success": False,
                "errors": errors,
            },
            status=400
        )

    return render(
        request,
        "posts/createPost.html",
        {
            "post_form": post_form,
            "categories": categories,
            "post_form_errors": errors,
            "show_post_form_error": True,
        }
    )


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
            "Your account has been banned from creating posts."
        )

        return redirect("home")

    # -----------------------------------------------------
    # CATEGORIES
    # -----------------------------------------------------

    categories = Category.objects.all()

    # =====================================================
    # GET REQUEST
    # =====================================================

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

    # =====================================================
    # POST REQUEST
    # =====================================================

    post_form = PostForm(
        request.POST
    )

    # =====================================================
    # VALIDATE POST FORM
    # =====================================================

    if not post_form.is_valid():

        error_messages = form_error_messages(
            post_form
        )

        if is_ajax(request):

            return JsonResponse(
                {
                    "success": False,
                    "errors": error_messages,
                },
                status=400
            )

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

    # =====================================================
    # FIND ITEM INDEXES
    # =====================================================

    item_indexes = get_item_indexes(
        request
    )

    # -----------------------------------------------------
    # NO ITEMS
    # -----------------------------------------------------

    if not item_indexes:

        error_message = (
            "Please add at least one item to your post."
        )

        return return_validation_error(
            request,
            error_message,
            post_form,
            categories
        )

    # -----------------------------------------------------
    # MAXIMUM 10 ITEMS
    # -----------------------------------------------------

    if len(item_indexes) > 10:

        error_message = (
            "You can only add up to 10 items per post."
        )

        return return_validation_error(
            request,
            error_message,
            post_form,
            categories
        )

    # =====================================================
    # CATEGORY / CONDITION
    # =====================================================

    category = post_form.cleaned_data.get(
        "category"
    )

    condition = post_form.cleaned_data.get(
        "condition"
    )

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

    # =====================================================
    # VALIDATE EVERY ITEM
    # =====================================================

    validation_errors = []

    for position, item_index in enumerate(
        item_indexes,
        start=1
    ):

        # -------------------------------------------------
        # ITEM NAME
        # -------------------------------------------------

        item_name = request.POST.get(
            f"item_name_{item_index}",
            ""
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
            ""
        ).strip()

        if not item_description:

            validation_errors.append(
                f"Enter a description for Item {position}."
            )

        # -------------------------------------------------
        # IMAGE VALIDATION
        # -------------------------------------------------

        item_images = get_item_images(
            request,
            item_index
        )

        if not item_images:

            validation_errors.append(
                f"Upload at least one image for Item {position}."
            )

        # -------------------------------------------------
        # MAXIMUM 5 IMAGES
        # -------------------------------------------------

        if len(item_images) > 5:

            validation_errors.append(
                f"You can upload a maximum of 5 images "
                f"for Item {position}."
            )

        # -------------------------------------------------
        # SIZE COUNT
        # -------------------------------------------------

        size_count_raw = request.POST.get(
            f"size_count_{item_index}",
            "0"
        )

        try:

            size_count = int(
                size_count_raw or 0
            )

        except (
            TypeError,
            ValueError
        ):

            size_count = 0

        # =================================================
        # SIZE-BASED ITEM
        # =================================================

        if should_have_sizes:

            # ---------------------------------------------
            # AT LEAST ONE SIZE
            # ---------------------------------------------

            if size_count <= 0:

                validation_errors.append(
                    f"Select at least one size for Item {position}."
                )

            # ---------------------------------------------
            # VALIDATE EACH SIZE
            # ---------------------------------------------

            selected_size_names = set()

            for j in range(size_count):

                size = request.POST.get(
                    f"size_{item_index}_{j}",
                    ""
                ).strip()

                quantity_raw = request.POST.get(
                    f"quantity_{item_index}_{j}",
                    ""
                )

                price_raw = request.POST.get(
                    f"size_price_{item_index}_{j}",
                    ""
                )

                # -----------------------------------------
                # SIZE
                # -----------------------------------------

                if not size:

                    validation_errors.append(
                        f"Size information is missing "
                        f"for Item {position}."
                    )

                else:

                    # Prevent duplicate sizes
                    if size in selected_size_names:

                        validation_errors.append(
                            f'Size "{size}" is selected more '
                            f"than once in Item {position}."
                        )

                    selected_size_names.add(
                        size
                    )

                # -----------------------------------------
                # QUANTITY
                # -----------------------------------------

                try:

                    quantity = int(
                        quantity_raw
                    )

                    if quantity <= 0:

                        validation_errors.append(
                            f'Enter a quantity greater than 0 '
                            f'for size "{size}" '
                            f'in Item {position}.'
                        )

                except (
                    TypeError,
                    ValueError
                ):

                    validation_errors.append(
                        f'Enter a valid quantity '
                        f'for size "{size}" '
                        f'in Item {position}.'
                    )

                # -----------------------------------------
                # PRICE
                # -----------------------------------------

                try:

                    size_price = int(
                        price_raw
                    )

                    if size_price <= 0:

                        validation_errors.append(
                            f'Enter a price greater than 0 '
                            f'for size "{size}" '
                            f'in Item {position}.'
                        )

                except (
                    TypeError,
                    ValueError
                ):

                    validation_errors.append(
                        f'Enter a valid price '
                        f'for size "{size}" '
                        f'in Item {position}.'
                    )

        # =================================================
        # SIMPLE ITEM WITHOUT SIZES
        # =================================================

        else:

            raw_price = request.POST.get(
                f"item_price_{item_index}",
                ""
            )

            raw_quantity = request.POST.get(
                f"simple_quantity_{item_index}",
                ""
            )

            # ---------------------------------------------
            # PRICE
            # ---------------------------------------------

            try:

                item_price = int(
                    raw_price
                )

                if item_price <= 0:

                    validation_errors.append(
                        f"Enter a price greater than 0 "
                        f"for Item {position}."
                    )

            except (
                TypeError,
                ValueError
            ):

                validation_errors.append(
                    f"Enter a valid price "
                    f"for Item {position}."
                )

            # ---------------------------------------------
            # QUANTITY
            # ---------------------------------------------

            try:

                simple_quantity = int(
                    raw_quantity
                )

                if simple_quantity <= 0:

                    validation_errors.append(
                        f"Enter a quantity greater than 0 "
                        f"for Item {position}."
                    )

            except (
                TypeError,
                ValueError
            ):

                validation_errors.append(
                    f"Enter a valid quantity "
                    f"for Item {position}."
                )

    # =====================================================
    # RETURN VALIDATION ERRORS
    # =====================================================

    if validation_errors:

        return return_validation_errors(
            request,
            validation_errors,
            post_form,
            categories
        )

    # =====================================================
    # CREATE DATABASE RECORDS
    # =====================================================

    try:

        with transaction.atomic():

            # =================================================
            # CREATE POST
            # =================================================

            post = post_form.save(
                commit=False
            )

            post.user = (
                request.user.profile
            )

            post.save()

            # =================================================
            # CREATE ITEMS
            # =================================================

            for item_index in item_indexes:

                item_name = request.POST.get(
                    f"item_name_{item_index}",
                    ""
                ).strip()

                item_description = request.POST.get(
                    f"item_description_{item_index}",
                    ""
                ).strip()

                # -------------------------------------------------
                # SIZE COUNT
                # -------------------------------------------------

                try:

                    size_count = int(
                        request.POST.get(
                            f"size_count_{item_index}",
                            0
                        ) or 0
                    )

                except (
                    TypeError,
                    ValueError
                ):

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
                            f"item_price_{item_index}"
                        )
                    )

                    simple_quantity = int(
                        request.POST.get(
                            f"simple_quantity_{item_index}"
                        )
                    )

                # =================================================
                # CREATE ITEM
                # =================================================

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
                            f"size_{item_index}_{j}"
                        ).strip()

                        quantity = int(
                            request.POST.get(
                                f"quantity_{item_index}_{j}"
                            )
                        )

                        size_price = int(
                            request.POST.get(
                                f"size_price_{item_index}_{j}"
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
                    # ITEM PRICE = LOWEST SIZE PRICE
                    # -------------------------------------------------

                    if created_variant_prices:

                        item.price = min(
                            created_variant_prices
                        )

                        item.save(
                            skip_has_sizes=True
                        )

                # =================================================
                # CREATE ITEM IMAGES
                # =================================================

                item_images = get_item_images(
                    request,
                    item_index
                )

                for image in item_images:

                    ItemImage.objects.create(
                        item=item,
                        image=image
                    )

    # =====================================================
    # DATABASE ERROR
    # =====================================================

    except Exception as error:

        print(
            "CREATE POST ERROR:",
            error
        )

        error_message = (
            "Something went wrong while creating your post. "
            "Please check your information and try again."
        )

        if is_ajax(request):

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
        extra_tags="post-pending"
    )

    # =====================================================
    # AJAX SUCCESS
    # =====================================================

    if is_ajax(request):

        return JsonResponse(
            {
                "success": True,
                "message": success_message,
                "redirect_url": "/home/",
            }
        )

    # =====================================================
    # NORMAL SUCCESS
    # =====================================================

    return redirect(
        "home"
    )


# =========================================================
# EDIT POST
# =========================================================
# =========================================================
# EDIT POST
# =========================================================

@login_required
def edit_post(request, post_id):

    # -----------------------------------------------------
    # GET POST
    # -----------------------------------------------------

    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user.profile,
    )

    # -----------------------------------------------------
    # BAN CHECK
    # -----------------------------------------------------

    if request.user.profile.status == "Banned":

        message = (
            "Your account has been banned from editing posts."
        )

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "success": False,
                    "message": message,
                },
                status=403,
            )

        messages.error(request, message)
        return redirect("user:dashboard")

    # -----------------------------------------------------
    # APPROVED / PENDING ONLY
    # -----------------------------------------------------

    if post.status not in ["approved", "pending"]:

        message = "This post cannot be edited."

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "success": False,
                    "message": message,
                },
                status=400,
            )

        messages.error(request, message)
        return redirect("user:dashboard")

    categories = Category.objects.all()

    # =====================================================
    # POST REQUEST
    # =====================================================

    if request.method == "POST":

        post_form = PostForm(
            request.POST,
            instance=post,
        )

        # -------------------------------------------------
        # POST FORM VALIDATION
        # -------------------------------------------------

        if not post_form.is_valid():

            errors = []

            for field, field_errors in post_form.errors.items():

                for error in field_errors:

                    if field == "__all__":

                        errors.append(str(error))

                    else:

                        if field in post_form.fields:

                            field_name = (
                                post_form.fields[field].label
                                or field
                            )

                        else:

                            field_name = field.replace(
                                "_",
                                " "
                            ).title()

                        errors.append(
                            f"{field_name}: {error}"
                        )

            if not errors:

                errors.append(
                    "Please check your information and try again."
                )

            if request.headers.get(
                "X-Requested-With"
            ) == "XMLHttpRequest":

                return JsonResponse(
                    {
                        "success": False,
                        "errors": errors,
                        "message": errors[0],
                    },
                    status=400,
                )

            for error in errors:
                messages.error(request, error)

        else:

            try:

                # =================================================
                # DATABASE TRANSACTION
                # =================================================

                with transaction.atomic():

                    # -------------------------------------------------
                    # SAVE POST
                    # -------------------------------------------------

                    updated_post = post_form.save(
                        commit=False
                    )

                    updated_post.user = request.user.profile

                    # -------------------------------------------------
                    # APPROVED POST -> PENDING
                    # -------------------------------------------------

                    was_approved = (
                        post.status == "approved"
                    )

                    if was_approved:
                        updated_post.status = "pending"

                    updated_post.save()

                    # =================================================
                    # GET ITEM INDEXES
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
                    # UPDATE EXISTING ITEMS
                    # =================================================

                    existing_items = {
                        str(item.id): item
                        for item in post.items.all()
                    }

                    # -------------------------------------------------
                    # Match HTML index with existing item
                    # -------------------------------------------------

                    items_list = list(
                        post.items.all().order_by("id")
                    )

                    for position, index in enumerate(
                        item_indexes
                    ):

                        if position >= len(items_list):
                            continue

                        item = items_list[position]

                        # -------------------------------------------------
                        # ITEM NAME
                        # -------------------------------------------------

                        item.name = request.POST.get(
                            f"item_name_{index}",
                            ""
                        ).strip()

                        # -------------------------------------------------
                        # ITEM DESCRIPTION
                        # -------------------------------------------------

                        item.description = request.POST.get(
                            f"item_description_{index}",
                            ""
                        ).strip()

                        # -------------------------------------------------
                        # SIZE COUNT
                        # -------------------------------------------------

                        try:

                            size_count = int(
                                request.POST.get(
                                    f"size_count_{index}",
                                    0
                                ) or 0
                            )

                        except (
                            TypeError,
                            ValueError
                        ):

                            size_count = 0

                        # -------------------------------------------------
                        # DETERMINE WHETHER ITEM USES SIZES
                        # -------------------------------------------------

                        category = updated_post.category

                        condition = updated_post.condition

                        should_have_sizes = (
                            category
                            and category.size_type != "none"
                            and condition == "new"
                        )

                        # =================================================
                        # SIZE ITEM
                        # =================================================

                        if should_have_sizes and size_count > 0:

                            item.has_sizes = True

                            # Main price is lowest size price
                            variant_prices = []

                            # -------------------------------------------------
                            # Existing variants
                            # -------------------------------------------------

                            existing_variants = {
                                variant.size: variant
                                for variant in item.size_variants.all()
                            }

                            submitted_sizes = []

                            for j in range(size_count):

                                size = request.POST.get(
                                    f"size_{index}_{j}",
                                    ""
                                ).strip()

                                quantity_raw = request.POST.get(
                                    f"quantity_{index}_{j}",
                                    "0"
                                )

                                price_raw = request.POST.get(
                                    f"size_price_{index}_{j}",
                                    "0"
                                )

                                if not size:
                                    continue

                                try:
                                    quantity = int(
                                        quantity_raw
                                    )
                                except (
                                    TypeError,
                                    ValueError
                                ):
                                    quantity = 0

                                try:
                                    size_price = int(
                                        price_raw
                                    )
                                except (
                                    TypeError,
                                    ValueError
                                ):
                                    size_price = 0

                                submitted_sizes.append(size)

                                # -------------------------------------------------
                                # UPDATE OR CREATE SIZE VARIANT
                                # -------------------------------------------------

                                variant = existing_variants.get(
                                    size
                                )

                                if variant:

                                    variant.quantity = quantity
                                    variant.price = size_price

                                    variant.save()

                                else:

                                    SizeVariant.objects.create(
                                        item=item,
                                        size=size,
                                        quantity=quantity,
                                        price=size_price,
                                    )

                                if size_price > 0:
                                    variant_prices.append(
                                        size_price
                                    )

                            # -------------------------------------------------
                            # DELETE REMOVED SIZE VARIANTS
                            # -------------------------------------------------

                            item.size_variants.exclude(
                                size__in=submitted_sizes
                            ).delete()

                            # -------------------------------------------------
                            # ITEM PRICE = LOWEST SIZE PRICE
                            # -------------------------------------------------

                            if variant_prices:

                                item.price = min(
                                    variant_prices
                                )

                            item.simple_quantity = 0

                        # =================================================
                        # SIMPLE ITEM
                        # =================================================

                        else:

                            item.has_sizes = False

                            raw_price = request.POST.get(
                                f"item_price_{index}",
                                "0"
                            )

                            raw_quantity = request.POST.get(
                                f"simple_quantity_{index}",
                                "1"
                            )

                            try:
                                item.price = int(
                                    raw_price
                                )
                            except (
                                TypeError,
                                ValueError
                            ):
                                item.price = 0

                            try:
                                item.simple_quantity = int(
                                    raw_quantity
                                )
                            except (
                                TypeError,
                                ValueError
                            ):
                                item.simple_quantity = 1

                            # Remove old size variants
                            item.size_variants.all().delete()

                        # -------------------------------------------------
                        # SAVE ITEM
                        # -------------------------------------------------

                        item.save(
                            skip_has_sizes=True
                        )

                        # =================================================
                        # DELETE SELECTED EXISTING IMAGES
                        # =================================================

                        for key in request.POST.keys():

                            if key.startswith(
                                "delete_image_"
                            ):

                                image_id = key.replace(
                                    "delete_image_",
                                    ""
                                )

                                try:

                                    image = ItemImage.objects.get(
                                        id=image_id,
                                        item=item,
                                    )

                                    image.delete()

                                except ItemImage.DoesNotExist:

                                    pass

                        # =================================================
                        # ADD NEW IMAGES
                        # =================================================

                        image_key = f"images_{index}"

                        for image in request.FILES.getlist(
                            image_key
                        ):

                            # Maximum 5 new images per item
                            current_count = item.images.count()

                            if current_count >= 5:
                                break

                            ItemImage.objects.create(
                                item=item,
                                image=image,
                            )

                    # =================================================
                    # UPDATE POST STATUS BASED ON STOCK
                    # =================================================

                    if was_approved:

                        # Editing approved post always returns
                        # it to pending, so do NOT automatically
                        # change it back to approved here.

                        post.refresh_from_db()

                    else:

                        post.refresh_from_db()

                # =====================================================
                # SUCCESS MESSAGE
                # =====================================================

                if was_approved:

                    success_message = (
                        "Your post has been updated and "
                        "sent back for admin approval."
                    )

                else:

                    success_message = (
                        "Your post has been updated successfully."
                    )

                messages.success(
                    request,
                    success_message
                )

                # =====================================================
                # AJAX SUCCESS
                # =====================================================

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

                # =====================================================
                # NORMAL SUCCESS
                # =====================================================

                return redirect(
                    "user:dashboard"
                )

            except Exception as error:

                print(
                    "EDIT POST ERROR:",
                    repr(error)
                )

                error_message = (
                    "Something went wrong while updating "
                    "your post. Please try again."
                )

                if request.headers.get(
                    "X-Requested-With"
                ) == "XMLHttpRequest":

                    return JsonResponse(
                        {
                            "success": False,
                            "message": error_message,
                            "errors": [str(error)],
                        },
                        status=500,
                    )

                messages.error(
                    request,
                    error_message
                )

    # =====================================================
    # GET REQUEST
    # =====================================================

    else:

        post_form = PostForm(
            instance=post
        )

    # =====================================================
    # EXISTING ITEMS
    # =====================================================

    items = (
        post.items
        .prefetch_related(
            "images",
            "size_variants",
        )
        .all()
    )

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "posts/editPost.html",
        {
            "post": post,
            "post_form": post_form,
            "categories": categories,
            "items": items,
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
            user=request.user.profile
        )
        .prefetch_related(
            "items",
            "items__images",
            "items__size_variants",
        )
        .order_by(
            "-created_at"
        )
    )

    return render(
        request,
        "posts/my_posts.html",
        {
            "posts": posts,
        }
    )