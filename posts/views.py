from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .form import PostForm
from .models import Category, Post, Item, SizeVariant, ItemImage


@login_required
def create_post(request):
    categories = Category.objects.all()
    print(f"=== CREATE POST VIEW CALLED ===")
    print(f"Categories count: {categories.count()}")
    print(f"User: {request.user}")

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user.profile
            post.save()

            # Process items
            item_count = int(request.POST.get('item_count', 0))

            for i in range(item_count):
                item_name = request.POST.get(f'item_name_{i}')
                item_description = request.POST.get(f'item_description_{i}')
                item_price = request.POST.get(f'item_price_{i}')

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

                        if size and quantity:
                            SizeVariant.objects.create(
                                item=item,
                                size=size,
                                quantity=quantity
                            )

                    # Process images
                    images = request.FILES.getlist(f'images_{i}')
                    for image in images:
                        ItemImage.objects.create(item=item, image=image)

            messages.success(request, 'Post created successfully!')
            return redirect('home')
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