from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .form import PostForm
from .models import Category, Post, Item, SizeVariant, ItemImage


@login_required
def create_post(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user.profile
            post.save()

            # Find all item indexes from POST keys (item_name_0, item_name_1, ...)
            item_indexes = []
            for key in request.POST.keys():
                if key.startswith('item_name_'):
                    idx = key.replace('item_name_', '')
                    if idx not in item_indexes:
                        item_indexes.append(idx)

            # Precompute category/condition flags
            category_supports_sizes = post.category.size_type != 'none'
            is_new_post = post.condition == 'new'

            for i in item_indexes:
                item_name = request.POST.get(f'item_name_{i}')
                item_description = request.POST.get(f'item_description_{i}', '')

                # Per-item: check if the user actually selected sizes for this item
                size_count = int(request.POST.get(f'size_count_{i}', 0) or 0)
                has_sizes_for_item = category_supports_sizes and is_new_post and size_count > 0

                # If the item has sizes (user selected sizes), we'll set price/simple_quantity appropriately
                if has_sizes_for_item:
                    item_price = 0
                    simple_quantity = 0
                else:
                    # Read the regular (non-size) price/quantity from the submitted fields
                    # Note: frontend currently uses name="item_quantity_{index}" so read that
                    raw_price = request.POST.get(f'item_price_{i}', '0')
                    raw_qty = request.POST.get(f'item_quantity_{i}', '1')  # matches your frontend input name

                    try:
                        item_price = int(raw_price) if raw_price not in (None, '') else 0
                    except ValueError:
                        item_price = 0

                    try:
                        simple_quantity = int(raw_qty) if raw_qty not in (None, '') else 1
                    except ValueError:
                        simple_quantity = 1

                if item_name:
                    # Create item
                    item = Item.objects.create(
                        post=post,
                        name=item_name,
                        description=item_description,
                        price=item_price,
                        simple_quantity=simple_quantity,
                    )

                    # If sizes were selected for this item, create SizeVariant rows
                    if has_sizes_for_item:
                        created_variant_prices = []
                        for j in range(size_count):
                            size = request.POST.get(f'size_{i}_{j}')
                            qty_raw = request.POST.get(f'quantity_{i}_{j}', '0')
                            price_raw = request.POST.get(f'size_price_{i}_{j}', '0')

                            try:
                                qty = int(qty_raw) if qty_raw not in (None, '') else 0
                            except ValueError:
                                qty = 0
                            try:
                                size_price = int(price_raw) if price_raw not in (None, '') else 0
                            except ValueError:
                                size_price = 0

                            # Only create variants if size provided and maybe quantity > 0 (you can adjust rule)
                            if size:
                                SizeVariant.objects.create(
                                    item=item,
                                    size=size,
                                    quantity=qty,
                                    price=size_price,
                                )
                                created_variant_prices.append(size_price)

                        # Optionally update item.price to the minimum variant price (if you want item.price meaningful)
                        if created_variant_prices:
                            min_price = min([p for p in created_variant_prices if p is not None]) or 0
                            item.price = min_price
                            item.save(skip_has_sizes=True)

                    # Process images for this item
                    for key, files in request.FILES.lists():
                        # keys were appended as 'images_<index>' in your JS
                        if key == f'images_{i}' or key.startswith(f'images_{i}'):
                            for image in files:
                                ItemImage.objects.create(item=item, image=image)
                                # optional debug:
                                # print(f"DEBUG: Saved {image.name} for item index {i}")

            messages.success(request, 'Post created successfully!')
            return redirect('home')
        else:
            print(f"DEBUG: Form errors: {post_form.errors}")
    else:
        post_form = PostForm()

    return render(request, 'posts/createPost.html', {
        'post_form': post_form,
        'categories': categories,
    })

@login_required
def get_category_sizes(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return JsonResponse({
        'sizes': category.get_sizes(),
        'size_label': category.size_label or 'Size',
        'size_type': category.size_type,
    })