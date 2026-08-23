from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from .form import PostForm
from .models import Category, Post, Item, SizeVariant, ItemImage


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def is_ajax(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def get_item_indexes(request):
    item_indexes = []
    for key in request.POST.keys():
        if key.startswith("item_name_"):
            index = key.replace("item_name_", "", 1)
            if index.isdigit() and index not in item_indexes:
                item_indexes.append(index)
    return item_indexes


def get_item_images(request, item_index):
    field_name = f"images_{item_index}"
    return request.FILES.getlist(field_name)


def form_error_messages(post_form):
    error_messages = []
    for field, errors in post_form.errors.items():
        for error in errors:
            if field == "__all__":
                error_messages.append(str(error))
            else:
                if field in post_form.fields:
                    field_name = post_form.fields[field].label or field.replace("_", " ").title()
                else:
                    field_name = field.replace("_", " ").title()
                error_messages.append(f"{field_name}: {error}")
    if not error_messages:
        error_messages.append("Please check the post information and try again.")
    return error_messages


def return_validation_error(request, message, post_form, categories):
    if is_ajax(request):
        return JsonResponse({"success": False, "errors": [message]}, status=400)
    return render(request, "posts/createPost.html", {
        "post_form": post_form,
        "categories": categories,
        "post_form_errors": [message],
        "show_post_form_error": True,
    })


def return_validation_errors(request, errors, post_form, categories):
    if is_ajax(request):
        return JsonResponse({"success": False, "errors": errors}, status=400)
    return render(request, "posts/createPost.html", {
        "post_form": post_form,
        "categories": categories,
        "post_form_errors": errors,
        "show_post_form_error": True,
    })


# =========================================================
# CREATE POST
# =========================================================

@login_required
def create_post(request):
    if request.user.profile.status == "Banned":
        messages.error(request, "Your account has been banned from creating posts.")
        return redirect("home")

    categories = Category.objects.all()

    if request.method == "GET":
        post_form = PostForm()
        return render(request, "posts/createPost.html", {
            "post_form": post_form,
            "categories": categories,
        })

    post_form = PostForm(request.POST)

    if not post_form.is_valid():
        error_messages = form_error_messages(post_form)
        if is_ajax(request):
            return JsonResponse({"success": False, "errors": error_messages}, status=400)
        return render(request, "posts/createPost.html", {
            "post_form": post_form,
            "categories": categories,
            "post_form_errors": error_messages,
            "show_post_form_error": True,
        })

    item_indexes = get_item_indexes(request)

    if not item_indexes:
        return return_validation_error(request, "Please add at least one item to your post.", post_form, categories)

    if len(item_indexes) > 10:
        return return_validation_error(request, "You can only add up to 10 items per post.", post_form, categories)

    category = post_form.cleaned_data.get("category")
    condition = post_form.cleaned_data.get("condition")
    category_supports_sizes = (category is not None and category.size_type != "none")
    is_new_post = (condition == "new")
    should_have_sizes = (category_supports_sizes and is_new_post)

    validation_errors = []

    for position, item_index in enumerate(item_indexes, start=1):
        item_name = request.POST.get(f"item_name_{item_index}", "").strip()
        if not item_name:
            validation_errors.append(f"Enter a name for Item {position}.")

        item_description = request.POST.get(f"item_description_{item_index}", "").strip()
        if not item_description:
            validation_errors.append(f"Enter a description for Item {position}.")

        item_images = get_item_images(request, item_index)
        if not item_images:
            validation_errors.append(f"Upload at least one image for Item {position}.")

        if len(item_images) > 5:
            validation_errors.append(f"You can upload a maximum of 5 images for Item {position}.")

        size_count_raw = request.POST.get(f"size_count_{item_index}", "0")
        try:
            size_count = int(size_count_raw or 0)
        except (TypeError, ValueError):
            size_count = 0

        if should_have_sizes:
            if size_count <= 0:
                validation_errors.append(f"Select at least one size for Item {position}.")

            selected_size_names = set()
            for j in range(size_count):
                size = request.POST.get(f"size_{item_index}_{j}", "").strip()
                quantity_raw = request.POST.get(f"quantity_{item_index}_{j}", "")
                price_raw = request.POST.get(f"size_price_{item_index}_{j}", "")

                if not size:
                    validation_errors.append(f"Size information is missing for Item {position}.")
                else:
                    if size in selected_size_names:
                        validation_errors.append(f'Size "{size}" is selected more than once in Item {position}.')
                    selected_size_names.add(size)

                try:
                    quantity = int(quantity_raw)
                    if quantity <= 0:
                        validation_errors.append(f'Enter a quantity greater than 0 for size "{size}" in Item {position}.')
                except (TypeError, ValueError):
                    validation_errors.append(f'Enter a valid quantity for size "{size}" in Item {position}.')

                try:
                    size_price = int(price_raw)
                    if size_price <= 0:
                        validation_errors.append(f'Enter a price greater than 0 for size "{size}" in Item {position}.')
                except (TypeError, ValueError):
                    validation_errors.append(f'Enter a valid price for size "{size}" in Item {position}.')

        else:
            raw_price = request.POST.get(f"item_price_{item_index}", "")
            raw_quantity = request.POST.get(f"simple_quantity_{item_index}", "")

            try:
                item_price = int(raw_price)
                if item_price <= 0:
                    validation_errors.append(f"Enter a price greater than 0 for Item {position}.")
            except (TypeError, ValueError):
                validation_errors.append(f"Enter a valid price for Item {position}.")

            try:
                simple_quantity = int(raw_quantity)
                if simple_quantity <= 0:
                    validation_errors.append(f"Enter a quantity greater than 0 for Item {position}.")
            except (TypeError, ValueError):
                validation_errors.append(f"Enter a valid quantity for Item {position}.")

    if validation_errors:
        return return_validation_errors(request, validation_errors, post_form, categories)

    try:
        with transaction.atomic():
            post = post_form.save(commit=False)
            post.user = request.user.profile
            post.save()

            for item_index in item_indexes:
                item_name = request.POST.get(f"item_name_{item_index}", "").strip()
                item_description = request.POST.get(f"item_description_{item_index}", "").strip()

                try:
                    size_count = int(request.POST.get(f"size_count_{item_index}", 0) or 0)
                except (TypeError, ValueError):
                    size_count = 0

                has_sizes_for_item = (should_have_sizes and size_count > 0)

                if has_sizes_for_item:
                    item_price = 0
                    simple_quantity = 0
                else:
                    item_price = int(request.POST.get(f"item_price_{item_index}"))
                    simple_quantity = int(request.POST.get(f"simple_quantity_{item_index}"))

                item = Item.objects.create(
                    post=post,
                    name=item_name,
                    description=item_description,
                    price=item_price,
                    simple_quantity=simple_quantity,
                )

                if has_sizes_for_item:
                    created_variant_prices = []
                    for j in range(size_count):
                        size = request.POST.get(f"size_{item_index}_{j}").strip()
                        quantity = int(request.POST.get(f"quantity_{item_index}_{j}"))
                        size_price = int(request.POST.get(f"size_price_{item_index}_{j}"))
                        SizeVariant.objects.create(item=item, size=size, quantity=quantity, price=size_price)
                        created_variant_prices.append(size_price)

                    if created_variant_prices:
                        item.price = min(created_variant_prices)
                        item.save(skip_has_sizes=True)

                item_images = get_item_images(request, item_index)
                for image in item_images:
                    ItemImage.objects.create(item=item, image=image)

    except Exception as error:
        print("CREATE POST ERROR:", error)
        error_message = "Something went wrong while creating your post. Please check your information and try again."
        if is_ajax(request):
            return JsonResponse({"success": False, "errors": [error_message]}, status=500)
        return render(request, "posts/createPost.html", {
            "post_form": post_form,
            "categories": categories,
            "post_form_errors": [error_message],
            "show_post_form_error": True,
        })

    success_message = "Your post has been submitted successfully and is waiting for admin approval."
    messages.success(request, success_message, extra_tags="post-pending")

    if is_ajax(request):
        return JsonResponse({"success": True, "message": success_message, "redirect_url": "/home/"})

    return redirect("home")


# =========================================================
# EDIT POST
# =========================================================

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user.profile)

    # Check if post can be edited
    if post.status not in ["approved", "pending"]:
        message = "This post cannot be edited."
        if is_ajax(request):
            return JsonResponse({"success": False, "message": message}, status=400)
        messages.error(request, message)
        return redirect("user:dashboard")

    if request.user.profile.status == "Banned":
        message = "Your account has been banned from editing posts."
        if is_ajax(request):
            return JsonResponse({"success": False, "message": message}, status=403)
        messages.error(request, message)
        return redirect("user:dashboard")

    categories = Category.objects.all()
    is_approved = post.status == "approved"

    if request.method == "POST":

        # For approved posts, only allow price/quantity changes
        if is_approved:
            # Don't validate PostForm for approved posts
            # Only update item prices and quantities
            try:
                with transaction.atomic():
                    for item in post.items.all():
                        item_id = str(item.id)

                        # Check if item has sizes
                        if item.has_sizes:
                            # Update size variant prices and quantities
                            for variant in item.size_variants.all():
                                variant_id = str(variant.id)

                                # Get new price and quantity from POST
                                new_price = request.POST.get(f"variant_price_{variant_id}", "")
                                new_quantity = request.POST.get(f"variant_quantity_{variant_id}", "")

                                try:
                                    if new_price:
                                        variant.price = int(new_price)
                                    if new_quantity:
                                        variant.quantity = int(new_quantity)
                                    variant.save()
                                except (TypeError, ValueError):
                                    pass

                            # Update item price to lowest variant price
                            prices = [v.price for v in item.size_variants.all() if v.price > 0]
                            if prices:
                                item.price = min(prices)
                                item.save(skip_has_sizes=True)
                        else:
                            # Update simple item price and quantity
                            new_price = request.POST.get(f"item_price_{item_id}", "")
                            new_quantity = request.POST.get(f"item_quantity_{item_id}", "")

                            try:
                                if new_price:
                                    item.price = int(new_price)
                                if new_quantity:
                                    item.simple_quantity = int(new_quantity)
                                item.save(skip_has_sizes=True)
                            except (TypeError, ValueError):
                                pass

                    post.refresh_from_db()

                success_message = "Prices and quantities updated successfully."
                messages.success(request, success_message)

                if is_ajax(request):
                    return JsonResponse({"success": True, "message": success_message})

                return redirect("user:dashboard")

            except Exception as error:
                print("EDIT POST ERROR:", repr(error))
                error_message = "Something went wrong while updating your post."
                if is_ajax(request):
                    return JsonResponse({"success": False, "message": error_message}, status=500)
                messages.error(request, error_message)
                return redirect("user:dashboard")

        else:
            # For pending posts - full edit
            post_form = PostForm(request.POST, instance=post)

            if not post_form.is_valid():
                errors = []
                for field, field_errors in post_form.errors.items():
                    for error in field_errors:
                        if field == "__all__":
                            errors.append(str(error))
                        else:
                            field_name = post_form.fields[
                                             field].label or field if field in post_form.fields else field.replace("_",
                                                                                                                   " ").title()
                            errors.append(f"{field_name}: {error}")
                if not errors:
                    errors.append("Please check your information and try again.")

                if is_ajax(request):
                    return JsonResponse({"success": False, "errors": errors, "message": errors[0]}, status=400)
                for error in errors:
                    messages.error(request, error)
            else:
                try:
                    with transaction.atomic():
                        updated_post = post_form.save(commit=False)
                        updated_post.user = request.user.profile
                        updated_post.save()

                        item_indexes = []
                        for key in request.POST.keys():
                            if key.startswith("item_name_"):
                                idx = key.replace("item_name_", "")
                                if idx not in item_indexes:
                                    item_indexes.append(idx)

                        items_list = list(post.items.all().order_by("id"))

                        for position, index in enumerate(item_indexes):
                            if position >= len(items_list):
                                continue

                            item = items_list[position]
                            item.name = request.POST.get(f"item_name_{index}", "").strip()
                            item.description = request.POST.get(f"item_description_{index}", "").strip()

                            try:
                                size_count = int(request.POST.get(f"size_count_{index}", 0) or 0)
                            except (TypeError, ValueError):
                                size_count = 0

                            category = updated_post.category
                            condition = updated_post.condition
                            should_have_sizes = (category and category.size_type != "none" and condition == "new")

                            if should_have_sizes and size_count > 0:
                                item.has_sizes = True
                                variant_prices = []
                                existing_variants = {variant.size: variant for variant in item.size_variants.all()}
                                submitted_sizes = []

                                for j in range(size_count):
                                    size = request.POST.get(f"size_{index}_{j}", "").strip()
                                    quantity_raw = request.POST.get(f"quantity_{index}_{j}", "0")
                                    price_raw = request.POST.get(f"size_price_{index}_{j}", "0")

                                    if not size:
                                        continue

                                    try:
                                        quantity = int(quantity_raw)
                                    except (TypeError, ValueError):
                                        quantity = 0

                                    try:
                                        size_price = int(price_raw)
                                    except (TypeError, ValueError):
                                        size_price = 0

                                    submitted_sizes.append(size)
                                    variant = existing_variants.get(size)

                                    if variant:
                                        variant.quantity = quantity
                                        variant.price = size_price
                                        variant.save()
                                    else:
                                        SizeVariant.objects.create(item=item, size=size, quantity=quantity,
                                                                   price=size_price)

                                    if size_price > 0:
                                        variant_prices.append(size_price)

                                item.size_variants.exclude(size__in=submitted_sizes).delete()

                                if variant_prices:
                                    item.price = min(variant_prices)
                                item.simple_quantity = 0

                            else:
                                item.has_sizes = False
                                try:
                                    item.price = int(request.POST.get(f"item_price_{index}", "0"))
                                except (TypeError, ValueError):
                                    item.price = 0
                                try:
                                    item.simple_quantity = int(request.POST.get(f"simple_quantity_{index}", "1"))
                                except (TypeError, ValueError):
                                    item.simple_quantity = 1
                                item.size_variants.all().delete()

                            item.save(skip_has_sizes=True)

                            for key in request.POST.keys():
                                if key.startswith("delete_image_"):
                                    image_id = key.replace("delete_image_", "")
                                    try:
                                        image = ItemImage.objects.get(id=image_id, item=item)
                                        image.delete()
                                    except ItemImage.DoesNotExist:
                                        pass

                            image_key = f"images_{index}"
                            for image in request.FILES.getlist(image_key):
                                if item.images.count() >= 5:
                                    break
                                ItemImage.objects.create(item=item, image=image)

                        post.refresh_from_db()

                except Exception as error:
                    print("EDIT POST ERROR:", repr(error))
                    error_message = "Something went wrong while updating your post. Please try again."
                    if is_ajax(request):
                        return JsonResponse({"success": False, "message": error_message, "errors": [str(error)]},
                                            status=500)
                    messages.error(request, error_message)

    else:
        post_form = PostForm(instance=post) if not is_approved else None

    items = post.items.prefetch_related("images", "size_variants").all()

    return render(request, "posts/editPost.html", {
        "post": post,
        "post_form": post_form,
        "categories": categories,
        "items": items,
        "is_approved": is_approved,
    })
# =========================================================
# GET CATEGORY SIZES
# =========================================================

@login_required
def get_category_sizes(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return JsonResponse({
        "sizes": category.get_sizes(),
        "size_label": category.size_label or "Size",
        "size_type": category.size_type,
    })


# =========================================================
# MY POSTS
# =========================================================

@login_required
def my_posts(request):
    posts = (
        Post.objects
        .filter(user=request.user.profile)
        .prefetch_related("items", "items__images", "items__size_variants")
        .order_by("-created_at")
    )
    return render(request, "posts/my_posts.html", {"posts": posts})


@login_required
def pending_post_detail(request, post_id):
    """View for pending post details"""
    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user.profile,  # Change from request.user to request.user.profile
        status='pending'
    )

    context = {
        'post': post,
    }
    return render(request, 'posts/pending_post.html', context)


@login_required
def sold_post_detail(request, post_id):
    """View for sold post details"""
    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user.profile,  # Change from request.user to request.user.profile
        status='sold'
    )

    context = {
        'post': post,
    }
    return render(request, 'posts/sold_post.html', context)


@login_required
def rejected_post_detail(request, post_id):
    """View for rejected post details"""
    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user.profile,  # Change from request.user to request.user.profile
        status='rejected'
    )

    context = {
        'post': post,
    }
    return render(request, 'posts/reject_post.html', context)
