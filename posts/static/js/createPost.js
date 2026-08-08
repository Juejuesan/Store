// ============================================
// ITEMS & SIZES SYSTEM
// ============================================
let sizeOptions = [];
let selectedSizes = {};

function loadSizes() {
    const categorySelect = document.getElementById('categorySelect');
    const categoryId = categorySelect.value;
    const selectedOption = categorySelect.options[categorySelect.selectedIndex];
    const sizeType = selectedOption.getAttribute('data-size-type');

    if (categoryId && sizeType !== 'none') {
        fetch('/posts/get-category-sizes/' + categoryId + '/')
            .then(response => response.json())
            .then(data => {
                sizeOptions = data.sizes;
                updateAllSizeCharts();
            })
            .catch(error => console.error('Error:', error));
    } else {
        sizeOptions = [];
        updateAllSizeCharts();
    }
}

function checkSizeVisibility() {
    const condition = document.getElementById('conditionSelect').value;
    const categorySelect = document.getElementById('categorySelect');
    const selectedOption = categorySelect.options[categorySelect.selectedIndex];
    const sizeType = selectedOption.getAttribute('data-size-type');

    if (condition === 'new' && sizeType && sizeType !== 'none') {
        loadSizes();
    } else {
        sizeOptions = [];
        updateAllSizeCharts();
    }
}

function addItem() {
    const existingItems = document.querySelectorAll('.item-section').length;
    
    if (existingItems >= 10) {
        showCustomAlert('You can only add up to 10 items per post.');
        return;
    }

    const container = document.getElementById('itemsContainer');
    
    let newIndex = 0;
    while (document.getElementById('item' + newIndex)) {
        newIndex++;
    }
    
    const itemNumber = existingItems + 1;

    const itemHTML =
        '<div class="glass-card item-section" id="item' + newIndex + '">' +
            '<div class="item-header">' +
                '<h3><i class="fa-solid fa-box"></i> Item ' + itemNumber + '</h3>' +
                (existingItems === 0 ? '' : '<button type="button" class="remove-item-btn" onclick="removeItem(' + newIndex + ')">' +
                    '<i class="fa-solid fa-trash"></i> Remove Item' +
                '</button>') +
            '</div>' +
            '<div class="product-grid">' +
                '<div class="input-card">' +
                    '<label><i class="fa-solid fa-tag"></i> Item Name *</label>' +
                    '<input type="text" name="item_name_' + newIndex + '" placeholder="e.g., Blue Cotton T-Shirt" required>' +
                '</div>' +
                '<div class="input-card">' +
                    '<label><i class="fa-solid fa-money-bill-wave"></i> Price (MMK) *</label>' +
                    '<input type="number" name="item_price_' + newIndex + '" placeholder="Enter price" required min="1">' +
                '</div>' +
            '</div>' +
            '<div class="description-card">' +
                '<label><i class="fa-solid fa-align-left"></i> Item Description</label>' +
                '<textarea name="item_description_' + newIndex + '" placeholder="Describe this item..."></textarea>' +
            '</div>' +
            '<label class="item-upload-area" for="fileInput' + newIndex + '">' +
                '<div class="upload-icon"><i class="fa-solid fa-cloud-arrow-up"></i></div>' +
                '<h3>Upload Photos</h3>' +
                '<p>Click to browse</p>' +
                '<span>Choose Files</span>' +
                '<input type="file" id="fileInput' + newIndex + '" name="images_' + newIndex + '" multiple accept="image/*" style="display:none" onchange="handleFileSelect(this, ' + newIndex + ')">' +
            '</label>' +
            '<div class="preview-grid" id="previewGrid' + newIndex + '"></div>' +
            '<div id="sizeChart' + newIndex + '" class="size-chart" style="display:none">' +
                '<label><i class="fa-solid fa-ruler"></i> Select Sizes</label>' +
                '<div class="size-buttons" id="sizeButtons' + newIndex + '"></div>' +
            '</div>' +
            '<div id="selectedSizes' + newIndex + '" class="selected-sizes" style="display:none">' +
                '<input type="hidden" name="size_count_' + newIndex + '" value="0">' +
            '</div>' +
            '<button type="button" class="add-sizes-btn" id="addMoreSizes' + newIndex + '" style="display:none" onclick="toggleSizeChart(' + newIndex + ')">' +
                '<i class="fa-solid fa-plus"></i> Add Sizes' +
            '</button>' +
        '</div>';

    container.insertAdjacentHTML('beforeend', itemHTML);
    updateAllSizeCharts();
    checkItemLimit();
    renumberItems();
}

function removeItem(index) {
    const allItems = document.querySelectorAll('.item-section');
    if (allItems.length <= 1) {
        showCustomAlert('You must have at least one item in your post.');
        return;
    }

    const item = document.getElementById('item' + index);
    if (item) item.remove();
    delete selectedSizes[index];
    checkItemLimit();
    renumberItems();
}

function renumberItems() {
    const allItems = document.querySelectorAll('.item-section');

    allItems.forEach(function(item, i) {
        const itemNumber = i + 1;

        // Update item heading
        const header = item.querySelector('.item-header h3');
        if (header) {
            header.innerHTML =
                '<i class="fa-solid fa-box"></i> Item ' + itemNumber;
        }

        // Handle remove button
        const removeBtn = item.querySelector('.remove-item-btn');

        if (i === 0) {
            // First item can NEVER be removed
            if (removeBtn) {
                removeBtn.style.display = 'none';
            }
        } else {
            // Item 2, 3, 4... can be removed
            if (removeBtn) {
                removeBtn.style.display = 'flex';
            } else {
                // Create remove button if it doesn't exist
                const headerDiv = item.querySelector('.item-header');

                if (headerDiv) {
                    const index = item.id.replace('item', '');

                    headerDiv.insertAdjacentHTML(
                        'beforeend',
                        '<button type="button" class="remove-item-btn" ' +
                        'onclick="removeItem(' + index + ')">' +
                        '<i class="fa-solid fa-trash"></i> Remove Item' +
                        '</button>'
                    );
                }
            }
        }
    });
}

function checkItemLimit() {
    const addBtn = document.querySelector('.add-item-btn');
    const existingItems = document.querySelectorAll('.item-section').length;
    if (addBtn) {
        if (existingItems >= 10) {
            addBtn.style.display = 'none';
        } else {
            addBtn.style.display = 'inline-flex';
        }
    }
}

function handleFileSelect(input, itemIdx) {
    const files = input.files;
    const previewGrid = document.getElementById('previewGrid' + itemIdx);
    previewGrid.innerHTML = '';

    for (let i = 0; i < files.length; i++) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const html = '<div class="preview-card"><div class="image-frame">' +
                '<img src="' + e.target.result + '" alt="Preview">' +
                (i === 0 ? '<div class="cover-tag"><i class="fa-solid fa-star"></i> Cover</div>' : '') +
                '</div></div>';
            previewGrid.insertAdjacentHTML('beforeend', html);
        };
        reader.readAsDataURL(files[i]);
    }
}

function updateAllSizeCharts() {
    const condition = document.getElementById('conditionSelect').value;

    const allItems = document.querySelectorAll('.item-section');
    allItems.forEach(function(item) {
        const itemId = item.id.replace('item', '');
        const sizeChart = document.getElementById('sizeChart' + itemId);
        const addMoreBtn = document.getElementById('addMoreSizes' + itemId);
        if (sizeChart && addMoreBtn) {
            if (condition === 'new' && sizeOptions.length > 0) {
                sizeChart.style.display = 'block';
                addMoreBtn.style.display = 'inline-flex';
                populateSizeButtons(itemId);
            } else {
                sizeChart.style.display = 'none';
                addMoreBtn.style.display = 'none';
                document.getElementById('selectedSizes' + itemId).style.display = 'none';
                if (selectedSizes[itemId]) selectedSizes[itemId] = [];
            }
        }
    });
}

function populateSizeButtons(itemIdx) {
    const sizeButtons = document.getElementById('sizeButtons' + itemIdx);
    if (!sizeButtons) return;
    sizeButtons.innerHTML = '';

    sizeOptions.forEach(function(size) {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'size-btn';
        button.textContent = size;
        if (selectedSizes[itemIdx] && selectedSizes[itemIdx].find(function(s) { return s.size === size; })) {
            button.classList.add('active');
        }
        button.onclick = function() { toggleSize(itemIdx, size, button); };
        sizeButtons.appendChild(button);
    });
}

function toggleSize(itemIndex, size, button) {
    if (!selectedSizes[itemIndex]) {
        selectedSizes[itemIndex] = [];
    }

    const sizeRows = document.querySelectorAll('#selectedSizes' + itemIndex + ' .size-row');
    sizeRows.forEach(function(row, idx) {
        const qtyInput = row.querySelector('.quantity-input');
        const priceInput = row.querySelector('.price-input');
        if (selectedSizes[itemIndex][idx]) {
            if (qtyInput) selectedSizes[itemIndex][idx].quantity = parseInt(qtyInput.value) || 0;
            if (priceInput) selectedSizes[itemIndex][idx].price = parseInt(priceInput.value) || 0;
        }
    });

    const index = selectedSizes[itemIndex].findIndex(function(s) { return s.size === size; });

    if (index === -1) {
        selectedSizes[itemIndex].push({size: size, quantity: 0, price: 0});
        button.classList.add('active');
    } else {
        selectedSizes[itemIndex].splice(index, 1);
        button.classList.remove('active');
    }

    updateSelectedSizesDisplay(itemIndex);
}

function removeSize(itemIndex, sizeIndex, size) {
    const sizeRows = document.querySelectorAll('#selectedSizes' + itemIndex + ' .size-row');
    sizeRows.forEach(function(row, idx) {
        const qtyInput = row.querySelector('.quantity-input');
        const priceInput = row.querySelector('.price-input');
        if (selectedSizes[itemIndex][idx]) {
            if (qtyInput) selectedSizes[itemIndex][idx].quantity = parseInt(qtyInput.value) || 0;
            if (priceInput) selectedSizes[itemIndex][idx].price = parseInt(priceInput.value) || 0;
        }
    });

    selectedSizes[itemIndex].splice(sizeIndex, 1);

    const sizeButtons = document.getElementById('sizeButtons' + itemIndex);
    if (sizeButtons) {
        const buttons = sizeButtons.getElementsByClassName('size-btn');
        for (let btn of buttons) {
            if (btn.textContent === size) {
                btn.classList.remove('active');
                break;
            }
        }
    }

    updateSelectedSizesDisplay(itemIndex);
}

function saveQuantity(itemIndex, sizeIndex, value) {
    if (selectedSizes[itemIndex] && selectedSizes[itemIndex][sizeIndex]) {
        selectedSizes[itemIndex][sizeIndex].quantity = parseInt(value) || 0;
    }
}

function saveSizePrice(itemIndex, sizeIndex, value) {
    if (selectedSizes[itemIndex] && selectedSizes[itemIndex][sizeIndex]) {
        selectedSizes[itemIndex][sizeIndex].price = parseInt(value) || 0;
    }
}

function updateSelectedSizesDisplay(itemIndex) {
    const selectedSizesDiv = document.getElementById('selectedSizes' + itemIndex);
    if (!selectedSizesDiv) return;

    if (!selectedSizes[itemIndex] || selectedSizes[itemIndex].length === 0) {
        selectedSizesDiv.innerHTML = '<input type="hidden" name="size_count_' + itemIndex + '" value="0">';
        selectedSizesDiv.classList.add('hidden');
        return;
    }

    selectedSizesDiv.classList.remove('hidden');

    let html = '<h4><i class="fa-solid fa-circle-check"></i> Selected Sizes</h4>';
    html += '<input type="hidden" name="size_count_' + itemIndex + '" value="' + selectedSizes[itemIndex].length + '">';

    selectedSizes[itemIndex].forEach(function(sizeObj, j) {
        let qty = sizeObj.quantity || 0;
        let price = sizeObj.price || '';
        html += '<div class="size-row">' +
            '<span class="size-label">' + sizeObj.size + '</span>' +
            '<div class="quantity-wrapper">' +
                '<input type="number" class="quantity-input" name="quantity_' + itemIndex + '_' + j + '" placeholder="Qty" value="' + qty + '" min="0" required oninput="saveQuantity(' + itemIndex + ', ' + j + ', this.value)">' +
                '<input type="number" class="price-input" name="size_price_' + itemIndex + '_' + j + '" placeholder="Price" value="' + price + '" min="0" required oninput="saveSizePrice(' + itemIndex + ', ' + j + ', this.value)">' +
            '</div>' +
            '<input type="hidden" name="size_' + itemIndex + '_' + j + '" value="' + sizeObj.size + '">' +
            '<button type="button" class="remove-size-btn" onclick="removeSize(' + itemIndex + ', ' + j + ', \'' + sizeObj.size + '\')">' +
                '<i class="fa-solid fa-times"></i>' +
            '</button>' +
        '</div>';
    });

    selectedSizesDiv.innerHTML = html;
}

function toggleSizeChart(itemIdx) {
    const chart = document.getElementById('sizeChart' + itemIdx);
    if (chart) {
        chart.style.display = chart.style.display === 'none' ? 'block' : 'none';
    }
}

function showCustomAlert(message) {
    const existing = document.querySelector('.custom-alert-limit');
    if (existing) existing.remove();

    const alert = document.createElement('div');
    alert.className = 'custom-alert custom-alert-limit';
    alert.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i> ' + message;
    alert.style.cssText = 'display:flex;align-items:center;gap:10px;padding:14px 20px;background:#fef2f2;color:#dc2626;border-left:4px solid #dc2626;border-radius:10px;font-weight:600;margin-bottom:15px;';

    const form = document.getElementById('createPostForm');
    form.insertBefore(alert, form.firstChild);

    setTimeout(function() {
        alert.style.opacity = '0';
        alert.style.transition = 'opacity .3s';
        setTimeout(function() { alert.remove(); }, 300);
    }, 3000);
}

// Mouse glow
document.addEventListener('mousemove', function(e) {
    const glow = document.getElementById('mouseGlow');
    if (glow) { glow.style.left = e.clientX + 'px'; glow.style.top = e.clientY + 'px'; }
});

// Add first item on load
addItem();