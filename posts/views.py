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

            # Get ALL item names from POST data
            item_names = []
            for key in request.POST.keys():
                if key.startswith('item_name_'):
                    index = key.replace('item_name_', '')
                    item_names.append(index)

            for i in item_names:
                item_name = request.POST.get(f'item_name_{i}')
                item_price = request.POST.get(f'item_price_{i}')
                item_description = request.POST.get(f'item_description_{i}', '')

                if item_name and item_price:
                    item = Item.objects.create(
                        post=post,
                        name=item_name,
                        description=item_description,
                        price=item_price,
                    )

                    # Process sizes for this item
                    size_count = int(request.POST.get(f'size_count_{i}', 0))

                    for j in range(size_count):
                        size = request.POST.get(f'size_{i}_{j}')
                        quantity = request.POST.get(f'quantity_{i}_{j}')
                        size_price = request.POST.get(f'size_price_{i}_{j}', 0)  # ADDED

                        if size and quantity:
                            SizeVariant.objects.create(
                                item=item,
                                size=size,
                                quantity=quantity,
                                price=size_price,  # ADDED
                            )

                    # Process images - find all matching file inputs
                    for key, files in request.FILES.lists():
                        if key.startswith('images_'):
                            file_index = key.replace('images_', '')
                            if file_index == i:
                                for image in files:
                                    ItemImage.objects.create(item=item, image=image)
                                    print(f"DEBUG: Saved {image.name} for item index {i}")

            messages.success(request, 'Post created successfully!')
            return redirect('home')
        else:
            print(f"DEBUG: Form errors: {post_form.errors}")
    else:
        post_form = PostForm()

    return render(request, 'createPost.html', {
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