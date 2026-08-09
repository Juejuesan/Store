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

    const itemHTML =
        '<div class="glass-card item-section" id="item' + newIndex + '">' +
            '<div class="item-header">' +
                '<h3><i class="fa-solid fa-box"></i> Item</h3>' +
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
        const header = item.querySelector('.item-header h3');
        if (header) {
            header.innerHTML = '<i class="fa-solid fa-box"></i> Item';
        }
        const removeBtn = item.querySelector('.remove-item-btn');
        if (i === 0) {
            if (removeBtn) removeBtn.style.display = 'none';
        } else {
            if (removeBtn) {
                removeBtn.style.display = 'flex';
            } else {
                const headerDiv = item.querySelector('.item-header');
                if (headerDiv) {
                    const index = item.id.replace('item', '');
                    headerDiv.insertAdjacentHTML('beforeend',
                        '<button type="button" class="remove-item-btn" onclick="removeItem(' + index + ')">' +
                        '<i class="fa-solid fa-trash"></i> Remove Item</button>');
                }
            }
        }
    });
}

function checkItemLimit() {
    const addBtn = document.querySelector('.add-item-btn');
    const existingItems = document.querySelectorAll('.item-section').length;
    if (addBtn) {
        addBtn.style.display = existingItems >= 10 ? 'none' : 'inline-flex';
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

function saveAllQuantities(itemIdx) {
    const rows = document.querySelectorAll('#selectedSizes' + itemIdx + ' .size-row');
    rows.forEach(function(row, idx) {
        const qtyInput = row.querySelector('.quantity-input');
        const priceInput = row.querySelector('.price-input');
        if (selectedSizes[itemIdx] && selectedSizes[itemIdx][idx]) {
            if (qtyInput) selectedSizes[itemIdx][idx].quantity = parseInt(qtyInput.value) || 0;
            if (priceInput) selectedSizes[itemIdx][idx].price = parseInt(priceInput.value) || 0;
        }
    });
}

function toggleSize(itemIdx, size, button) {
    if (!selectedSizes[itemIdx]) selectedSizes[itemIdx] = [];
    saveAllQuantities(itemIdx);
    const index = selectedSizes[itemIdx].findIndex(function(s) { return s.size === size; });
    if (index === -1) {
        selectedSizes[itemIdx].push({size: size, quantity: 0, price: 0});
        button.classList.add('active');
    } else {
        selectedSizes[itemIdx].splice(index, 1);
        button.classList.remove('active');
    }
    updateSelectedSizesDisplay(itemIdx);
}

function updateSelectedSizesDisplay(itemIdx) {
    const div = document.getElementById('selectedSizes' + itemIdx);
    if (!div) return;
    if (!selectedSizes[itemIdx] || selectedSizes[itemIdx].length === 0) {
        div.innerHTML = '<input type="hidden" name="size_count_' + itemIdx + '" value="0">';
        div.style.display = 'none';
        return;
    }
    div.style.display = 'block';
    let html = '<h4><i class="fa-solid fa-circle-check"></i> Selected Sizes</h4>';
    html += '<input type="hidden" name="size_count_' + itemIdx + '" value="' + selectedSizes[itemIdx].length + '">';
    selectedSizes[itemIdx].forEach(function(sizeObj, j) {
        let qty = sizeObj.quantity || 0;
        let price = sizeObj.price || '';
        html += '<div class="size-row">' +
            '<span class="size-label">' + sizeObj.size + '</span>' +
            '<input type="number" class="quantity-input" name="quantity_' + itemIdx + '_' + j + '" placeholder="Qty" value="' + qty + '" min="0" required oninput="saveQuantity(' + itemIdx + ', ' + j + ', this.value)">' +
            '<input type="number" class="price-input" name="size_price_' + itemIdx + '_' + j + '" placeholder="Price" value="' + price + '" min="0" required oninput="saveSizePrice(' + itemIdx + ', ' + j + ', this.value)">' +
            '<input type="hidden" name="size_' + itemIdx + '_' + j + '" value="' + sizeObj.size + '">' +
            '<button type="button" class="remove-size-btn" onclick="removeSize(' + itemIdx + ', ' + j + ', \'' + sizeObj.size + '\')">' +
            '<i class="fa-solid fa-times"></i></button>' +
            '</div>';
    });
    div.innerHTML = html;
}

function saveQuantity(itemIdx, sizeIndex, value) {
    if (selectedSizes[itemIdx] && selectedSizes[itemIdx][sizeIndex]) {
        selectedSizes[itemIdx][sizeIndex].quantity = parseInt(value) || 0;
    }
}

function saveSizePrice(itemIdx, sizeIndex, value) {
    if (selectedSizes[itemIdx] && selectedSizes[itemIdx][sizeIndex]) {
        selectedSizes[itemIdx][sizeIndex].price = parseInt(value) || 0;
    }
}

function removeSize(itemIdx, sizeIndex, size) {
    saveAllQuantities(itemIdx);
    selectedSizes[itemIdx].splice(sizeIndex, 1);
    const sizeButtons = document.getElementById('sizeButtons' + itemIdx);
    if (sizeButtons) {
        const buttons = sizeButtons.getElementsByClassName('size-btn');
        for (let btn of buttons) {
            if (btn.textContent === size) { btn.classList.remove('active'); break; }
        }
    }
    updateSelectedSizesDisplay(itemIdx);
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

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Alert stays for 5 seconds
    setTimeout(function() {
        alert.style.opacity = '0';
        alert.style.transition = 'opacity .3s';
        setTimeout(function() { alert.remove(); }, 300);
    }, 5000);
}

// Store files per item
let itemFiles = {};

function handleFileSelect(input, itemIdx) {
    const files = Array.from(input.files);

    if (!itemFiles[itemIdx]) {
        itemFiles[itemIdx] = [];
    }

    if (itemFiles[itemIdx].length + files.length > 6) {
        showCustomAlert('You can upload a maximum of 6 images per item.');
        input.value = '';
        return;
    }

    files.forEach(function(file) {
        if (file.type.startsWith('image/')) {
            itemFiles[itemIdx].push(file);
        }
    });

    updatePreview(itemIdx);
    // DON'T clear input.value - let the browser keep the files
}

function updatePreview(itemIdx) {
    const previewGrid = document.getElementById('previewGrid' + itemIdx);
    if (!previewGrid) return;
    previewGrid.innerHTML = '';

    if (!itemFiles[itemIdx]) return;

    itemFiles[itemIdx].forEach(function(file, i) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const card = document.createElement('div');
            card.className = 'preview-card';
            card.innerHTML =
                '<div class="image-frame">' +
                    '<img src="' + e.target.result + '" alt="Preview">' +
                    (i === 0 ? '<div class="cover-tag"><i class="fa-solid fa-star"></i> Cover</div>' : '') +
                    '<button type="button" class="remove-image-btn" onclick="removeImage(' + itemIdx + ', ' + i + ')">' +
                        '<i class="fa-solid fa-xmark"></i>' +
                    '</button>' +
                '</div>';
            previewGrid.appendChild(card);
        };
        reader.readAsDataURL(file);
    });
}

function removeImage(itemIdx, fileIndex) {
    if (!itemFiles[itemIdx]) return;

    // Remove the file
    itemFiles[itemIdx].splice(fileIndex, 1);

    // Update preview
    updatePreview(itemIdx);

    // Sync files to input
    syncFilesToInput(itemIdx);
}

function syncFilesToInput(itemIdx) {
    const input = document.getElementById('fileInput' + itemIdx);
    if (!input) return;

    const dt = new DataTransfer();
    if (itemFiles[itemIdx]) {
        itemFiles[itemIdx].forEach(function(file) {
            dt.items.add(file);
        });
    }
    input.files = dt.files;
}

// Add CSS for remove button

// Mouse glow
document.addEventListener('mousemove', function(e) {
    const glow = document.getElementById('mouseGlow');
    if (glow) { glow.style.left = e.clientX + 'px'; glow.style.top = e.clientY + 'px'; }
});

// Form validation
document.getElementById('createPostForm').addEventListener('submit', function(e) {
    const items = document.querySelectorAll('.item-section');


    let allValid = true;

    items.forEach(function(item, index) {
        const itemNum = index + 1;
        const nameInput = item.querySelector('input[name^="item_name_"]');
        const priceInput = item.querySelector('input[name^="item_price_"]');
        const descInput = item.querySelector('textarea[name^="item_description_"]');
        const fileInput = item.querySelector('input[type="file"]');

        // Check name
        if (nameInput && !nameInput.value.trim()) {
            e.preventDefault();
            showCustomAlert('Please enter a name for Item ' + itemNum + '.');
            nameInput.focus();
            allValid = false;
            return false;
        }

        // Check price
        if (priceInput && (!priceInput.value || parseInt(priceInput.value) <= 0)) {
            e.preventDefault();
            showCustomAlert('Please enter a valid price for Item ' + itemNum + '.');
            priceInput.focus();
            allValid = false;
            return false;
        }

        // Check description
        if (descInput && !descInput.value.trim()) {
            e.preventDefault();
            showCustomAlert('Please enter a description for Item ' + itemNum + '.');
            descInput.focus();
            allValid = false;
            return false;
        }

        // Check image
        if (!itemFiles[itemNum - 1] || itemFiles[itemNum - 1].length === 0) {
            e.preventDefault();
            showCustomAlert('Please upload at least one image for Item .');
            allValid = false;
            return false;
        }
    });

    if (!allValid) return false;
});
// Add first item on load
addItem();