// ============================================
// ITEMS & SIZES SYSTEM
// ============================================
let sizeOptions = [];
let selectedSizes = {};
let itemFiles = {};

function loadSizes() {
    const categorySelect = document.getElementById('categorySelect');
    const categoryId = categorySelect.value;
    const selectedOption = categorySelect.options[categorySelect.selectedIndex];
    const sizeType = selectedOption.getAttribute('data-size-type');
    if (categoryId && sizeType !== 'none') {
        fetch('/posts/get-category-sizes/' + categoryId + '/')
            .then(response => response.json())
            .then(data => { sizeOptions = data.sizes; updateAllSizeCharts(); })
            .catch(error => console.error('Error:', error));
    } else { sizeOptions = []; updateAllSizeCharts(); }
}

function checkSizeVisibility() {
    const condition = document.getElementById('conditionSelect').value;
    const categorySelect = document.getElementById('categorySelect');
    const selectedOption = categorySelect.options[categorySelect.selectedIndex];
    const sizeType = selectedOption.getAttribute('data-size-type');
    if (condition === 'new' && sizeType && sizeType !== 'none') { loadSizes(); }
    else { sizeOptions = []; updateAllSizeCharts(); }
}

function addItem() {
    const existingItems = document.querySelectorAll('.item-section').length;
    if (existingItems >= 10) { showCustomAlert('You can only add up to 10 items per post.'); return; }
    const container = document.getElementById('itemsContainer');
    let newIndex = 0;
    while (document.getElementById('item' + newIndex)) { newIndex++; }

    const itemHTML =
        '<div class="glass-card item-section" id="item' + newIndex + '">' +
            '<div class="item-header">' +
                '<h3><i class="fa-solid fa-box"></i> Item</h3>' +
                (existingItems === 0 ? '' : '<button type="button" class="remove-item-btn" onclick="removeItem(' + newIndex + ')"><i class="fa-solid fa-trash"></i> Remove Item</button>') +
            '</div>' +
            '<div class="product-grid">' +
                '<div class="input-card"><label><i class="fa-solid fa-tag"></i> Item Name *</label><input type="text" name="item_name_' + newIndex + '" placeholder="e.g., Blue Cotton T-Shirt" required></div>' +
                '<div class="input-card"><label><i class="fa-solid fa-money-bill-wave"></i> Price (MMK) *</label><input type="number" name="item_price_' + newIndex + '" placeholder="Enter price" required min="1"></div>' +
            '</div>' +
            '<div class="product-grid">' +
                '<div class="input-card item-qty-card" id="itemQtyCard' + newIndex + '">' +
                    '<label><i class="fa-solid fa-boxes-stacked"></i> Quantity *</label>' +
                    '<input type="number" name="simple_quantity_' + newIndex + '" placeholder="Enter quantity" value="1" min="1" required>' +
                    '<small style="color:#64748b;font-size:12px;">This quantity will be used if no sizes are selected</small>' +
                '</div>' +
            '</div>' +
            '<div class="description-card"><label><i class="fa-solid fa-align-left"></i> Item Description</label><textarea name="item_description_' + newIndex + '" placeholder="Describe this item..."></textarea></div>' +
            '<label class="item-upload-area" for="fileInput' + newIndex + '"><div class="upload-icon"><i class="fa-solid fa-cloud-arrow-up"></i></div><h3>Upload Photos</h3><p>Click to browse</p><span>Choose Files</span></label>' +
            '<input type="file" id="fileInput' + newIndex + '" name="images_' + newIndex + '" multiple accept="image/*" style="display:none" onchange="handleFileSelect(this, ' + newIndex + ')">' +
            '<div class="preview-grid" id="previewGrid' + newIndex + '"></div>' +
            '<div id="sizeChart' + newIndex + '" class="size-chart" style="display:none"><label><i class="fa-solid fa-ruler"></i> Select Sizes</label><div class="size-buttons" id="sizeButtons' + newIndex + '"></div></div>' +
            '<div id="selectedSizes' + newIndex + '" class="selected-sizes" style="display:none"><input type="hidden" name="size_count_' + newIndex + '" value="0"></div>' +
            '<button type="button" class="add-sizes-btn" id="addMoreSizes' + newIndex + '" style="display:none" onclick="toggleSizeChart(' + newIndex + ')"><i class="fa-solid fa-plus"></i> Add Sizes</button>' +
        '</div>';

    container.insertAdjacentHTML('beforeend', itemHTML);
    itemFiles[newIndex] = [];
    updateAllSizeCharts();
    checkItemLimit();
}

function removeItem(index) {
    const allItems = document.querySelectorAll('.item-section');
    if (allItems.length <= 1) { showCustomAlert('You must have at least one item in your post.'); return; }
    const item = document.getElementById('item' + index);
    if (item) { item.remove(); delete itemFiles[index]; delete selectedSizes[index]; }
    checkItemLimit();
}

function checkItemLimit() {
    const addBtn = document.querySelector('.add-item-btn');
    const existingItems = document.querySelectorAll('.item-section').length;
    if (addBtn) addBtn.style.display = existingItems >= 10 ? 'none' : 'inline-flex';
}

// ============================================
// IMAGE HANDLING - GUARANTEED ORDER
// ============================================
function handleFileSelect(input, itemIdx) {
    const newFiles = Array.from(input.files);
    if (!itemFiles[itemIdx]) itemFiles[itemIdx] = [];

    // Add files one at a time to maintain selection order
    for (var i = 0; i < newFiles.length; i++) {
        if (itemFiles[itemIdx].length >= 5) {
            showCustomAlert('You can upload a maximum of 5 images per item.');
            break;
        }
        if (newFiles[i].type.startsWith('image/')) {
            itemFiles[itemIdx].push(newFiles[i]);
        }
    }

    updatePreview(itemIdx);
    // Clear the file input to allow re-selecting the same files
    input.value = '';
}

function updatePreview(itemIdx) {
    const previewGrid = document.getElementById('previewGrid' + itemIdx);
    if (!previewGrid) return;

    // Clear the preview grid first
    previewGrid.innerHTML = '';

    if (!itemFiles[itemIdx] || itemFiles[itemIdx].length === 0) return;

    // Create all preview cards in order using a document fragment for better performance
    const fragment = document.createDocumentFragment();

    // Process files in order - first file is always the cover
    itemFiles[itemIdx].forEach(function(file, i) {
        const reader = new FileReader();

        // Create card element immediately to maintain order
        const card = document.createElement('div');
        card.className = 'preview-card';
        card.dataset.index = i; // Store the index for reference

        // Set initial placeholder
        card.innerHTML = '<div class="image-frame"><div class="loading-placeholder">Loading...</div></div>';

        // Add card to fragment in correct order
        fragment.appendChild(card);

        // Load the image
        reader.onload = (function(currentCard, currentIndex) {
            return function(e) {
                currentCard.innerHTML = '<div class="image-frame">' +
                    '<img src="' + e.target.result + '" alt="Preview">' +
                    (currentIndex === 0 ? '<div class="cover-tag"><i class="fa-solid fa-star"></i> Cover</div>' : '') +
                    '<button type="button" class="remove-image-btn" onclick="removeImage(' + itemIdx + ', ' + currentIndex + ')"><i class="fa-solid fa-xmark"></i></button>' +
                    '</div>';
            };
        })(card, i);

        reader.readAsDataURL(file);
    });

    // Append all cards at once in the correct order
    previewGrid.appendChild(fragment);
}

function removeImage(itemIdx, fileIndex) {
    if (!itemFiles[itemIdx]) return;

    // Remove the file at the specified index
    itemFiles[itemIdx].splice(fileIndex, 1);

    // Re-render the preview to maintain order
    updatePreview(itemIdx);
}

// ============================================
// SIZE HANDLING
// ============================================
function updateAllSizeCharts() {
    const condition = document.getElementById('conditionSelect').value;
    document.querySelectorAll('.item-section').forEach(function(item) {
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
                var ss = document.getElementById('selectedSizes' + itemId);
                if (ss) ss.style.display = 'none';
                if (selectedSizes[itemId]) selectedSizes[itemId] = [];
            }
        }
    });
}

function populateSizeButtons(itemIdx) {
    const sb = document.getElementById('sizeButtons' + itemIdx);
    if (!sb) return;
    sb.innerHTML = '';
    sizeOptions.forEach(function(size) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'size-btn';
        btn.textContent = size;
        if (selectedSizes[itemIdx] && selectedSizes[itemIdx].find(function(s) { return s.size === size; })) {
            btn.classList.add('active');
        }
        btn.onclick = function() { toggleSize(itemIdx, size, btn); };
        sb.appendChild(btn);
    });
}

function saveAllQuantities(itemIdx) {
    const rows = document.querySelectorAll('#selectedSizes' + itemIdx + ' .size-row');
    rows.forEach(function(row, idx) {
        const q = row.querySelector('.quantity-input');
        const p = row.querySelector('.price-input');
        if (selectedSizes[itemIdx] && selectedSizes[itemIdx][idx]) {
            if (q) selectedSizes[itemIdx][idx].quantity = parseInt(q.value) || 0;
            if (p) selectedSizes[itemIdx][idx].price = parseInt(p.value) || 0;
        }
    });
}

function toggleSize(itemIdx, size, button) {
    if (!selectedSizes[itemIdx]) selectedSizes[itemIdx] = [];
    saveAllQuantities(itemIdx);
    const idx = selectedSizes[itemIdx].findIndex(function(s) { return s.size === size; });
    if (idx === -1) {
        selectedSizes[itemIdx].push({size: size, quantity: 0, price: 0});
        button.classList.add('active');
    } else {
        selectedSizes[itemIdx].splice(idx, 1);
        button.classList.remove('active');
    }
    updateSelectedSizesDisplay(itemIdx);
}

function updateSelectedSizesDisplay(itemIdx) {
    const div = document.getElementById('selectedSizes' + itemIdx);
    if (!div) return;
    const qtyCard = document.getElementById('itemQtyCard' + itemIdx);

    // find main price input and its card inside the item card
    const priceInput = document.querySelector('#item' + itemIdx + ' input[name="item_price_' + itemIdx + '"]');
    const priceCard = priceInput ? priceInput.closest('.input-card') : null;

    // helper to enable/disable inputs and manage required attribute
    function setInputState(input, enabled) {
        if (!input) return;
        input.disabled = !enabled;
        if (!enabled) {
            input.removeAttribute('required');
            input.setAttribute('aria-hidden', 'true');
        } else {
            input.setAttribute('required', ''); // restore required when re-enabled
            input.removeAttribute('aria-hidden');
        }
    }

    // No sizes selected -> hide sizes block, show main qty & price
    if (!selectedSizes[itemIdx] || selectedSizes[itemIdx].length === 0) {
        div.innerHTML = '<input type="hidden" name="size_count_' + itemIdx + '" value="0">';
        div.style.display = 'none';
        if (qtyCard) {
            qtyCard.style.display = 'block';
            setInputState(qtyCard.querySelector('input'), true);
        }
        if (priceCard) {
            priceCard.style.display = 'block';
            setInputState(priceInput, true);
        }
        return;
    }

    // Sizes selected -> hide main qty & price, show sizes block
    if (qtyCard) {
        qtyCard.style.display = 'none';
        setInputState(qtyCard.querySelector('input'), false);
    }
    if (priceCard) {
        priceCard.style.display = 'none';
        setInputState(priceInput, false);
    }

    div.style.display = 'block';
    var html = '<h4><i class="fa-solid fa-circle-check"></i> Selected Sizes</h4><input type="hidden" name="size_count_' + itemIdx + '" value="' + selectedSizes[itemIdx].length + '">';
    selectedSizes[itemIdx].forEach(function(so, j) {
        html += '<div class="size-row">' +
            '<span class="size-label">' + so.size + '</span>' +
            '<input type="number" class="quantity-input" name="quantity_' + itemIdx + '_' + j + '" placeholder="Qty" value="' + (so.quantity || 0) + '" min="0" required oninput="saveQuantity(' + itemIdx + ',' + j + ',this.value)">' +
            '<input type="number" class="price-input" name="size_price_' + itemIdx + '_' + j + '" placeholder="Price" value="' + (so.price || '') + '" min="0" required oninput="saveSizePrice(' + itemIdx + ',' + j + ',this.value)">' +
            '<input type="hidden" name="size_' + itemIdx + '_' + j + '" value="' + so.size + '">' +
            '<button type="button" class="remove-size-btn" onclick="removeSize(' + itemIdx + ',' + j + ',\'' + so.size + '\')"><i class="fa-solid fa-times"></i></button>' +
            '</div>';
    });
    div.innerHTML = html;
}

function saveQuantity(a,b,v){if(selectedSizes[a]&&selectedSizes[a][b])selectedSizes[a][b].quantity=parseInt(v)||0;}
function saveSizePrice(a,b,v){if(selectedSizes[a]&&selectedSizes[a][b])selectedSizes[a][b].price=parseInt(v)||0;}

function removeSize(itemIdx, sizeIndex, size) {
    saveAllQuantities(itemIdx);
    selectedSizes[itemIdx].splice(sizeIndex, 1);
    const sb = document.getElementById('sizeButtons' + itemIdx);
    if (sb) {
        var btns = sb.getElementsByClassName('size-btn');
        for (var i = 0; i < btns.length; i++) {
            if (btns[i].textContent === size) {
                btns[i].classList.remove('active');
                break;
            }
        }
    }
    updateSelectedSizesDisplay(itemIdx);
}

function toggleSizeChart(itemIdx) {
    const chart = document.getElementById('sizeChart' + itemIdx);
    if (chart) chart.style.display = chart.style.display === 'none' ? 'block' : 'none';
}

// ============================================
// ALERT
// ============================================


// ============================================
// FORM SUBMISSION WITH AJAX (OPTION B)
// ============================================
document.getElementById('createPostForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent default form submission

    const form = e.target;
    const items = document.querySelectorAll('.item-section');

    // Check if sizes should be required
    const condition = document.getElementById('conditionSelect').value;
    const categorySelect = document.getElementById('categorySelect');
    const selectedOption = categorySelect.options[categorySelect.selectedIndex];
    const sizeType = selectedOption ? selectedOption.getAttribute('data-size-type') : null;
    const categorySupportsSizes = sizeType && sizeType !== 'none';
    const isNewItem = condition === 'new';
    const shouldHaveSizes = categorySupportsSizes && isNewItem;

    // Validate items exist
    if (items.length === 0) {
        showCustomAlert('Please add at least one item.');
        return false;
    }

    // Validate all fields
    var allValid = true;
    items.forEach(function(item, index) {
        var id = item.id.replace('item', '');
        var n = item.querySelector('input[name^="item_name_"]');
        var d = item.querySelector('textarea[name^="item_description_"]');

        // Item name validation
        if (allValid && n && !n.value.trim()) {
            showCustomAlert('Enter a name for Item ' + (index + 1) + '.');
            n.focus();
            allValid = false;
        }

        // Description validation
        if (allValid && d && !d.value.trim()) {
            showCustomAlert('Enter a description for Item ' + (index + 1) + '.');
            d.focus();
            allValid = false;
        }

        // SIZE VALIDATION - For Brand New items in size-supporting categories
        if (shouldHaveSizes) {
            // Check if any sizes are selected
            if (allValid && (!selectedSizes[id] || selectedSizes[id].length === 0)) {
                showCustomAlert('Select at least one size for Item ' + (index + 1));
                allValid = false;

                // Focus/highlight size chart
                var sizeChart = document.getElementById('sizeChart' + id);
                if (sizeChart) {
                    sizeChart.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }

            // Check each selected size has quantity and price
            if (allValid && selectedSizes[id] && selectedSizes[id].length > 0) {
                selectedSizes[id].forEach(function(s, sIdx) {
                    if (allValid && (!s.quantity || s.quantity <= 0)) {
                        showCustomAlert('Enter a valid quantity for size "' + s.size + '" in Item ' + (index + 1) + '. Quantity must be greater than 0.');
                        allValid = false;
                    }
                    if (allValid && (!s.price || s.price <= 0)) {
                        showCustomAlert('Enter a valid price for size "' + s.size + '" in Item ' + (index + 1) + '. Price must be greater than 0.');
                        allValid = false;
                    }
                });
            }
        } else {
            // PRICE & QUANTITY VALIDATION - For items without sizes
            var p = item.querySelector('input[name^="item_price_"]');
            var q = item.querySelector('input[name^="simple_quantity_"]');

            if (allValid && p && (!p.value || parseInt(p.value) <= 0)) {
                showCustomAlert('Enter a valid price for Item ' + (index + 1) + '. Price must be greater than 0.');
                p.focus();
                allValid = false;
            }

            if (allValid && q && (!q.value || parseInt(q.value) <= 0)) {
                showCustomAlert('Enter a valid quantity for Item ' + (index + 1) + '. Quantity must be greater than 0.');
                q.focus();
                allValid = false;
            }
        }

        // Image validation
        if (allValid && (!itemFiles[id] || itemFiles[id].length === 0)) {
            showCustomAlert('Upload at least one image for Item ' + (index + 1) + '.');
            allValid = false;
        }
    });

    if (!allValid) return false;

    // Build FormData from the form (this captures all non-file form fields)
    const formData = new FormData(form);
console.log("POST DATA:");

for (const [key, value] of formData.entries()) {
    console.log(key, value);
}
    // Append files from itemFiles to FormData
    // The files are stored in itemFiles with keys matching item indices
    Object.keys(itemFiles).forEach(function(itemIdx) {
        if (!itemFiles[itemIdx] || itemFiles[itemIdx].length === 0) return;

        // Append each file for this item
        // Using 'images_X' as the field name (without []) - adjust if your backend expects array syntax
        itemFiles[itemIdx].forEach(function(file, fileIndex) {
            // Append with the same name as your file input: images_0, images_1, etc.
            // If your backend expects array syntax like images_0[], change accordingly
            formData.append('images_' + itemIdx, file);
        });
    });

    // Show loading state (optional)
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Uploading...';
    }

    // Submit via fetch
    fetch(form.action, {
        method: form.method || 'POST',
        body: formData,
        credentials: 'same-origin',
        headers: {
            'X-Requested-With': 'XMLHttpRequest' // Let Django know this is an AJAX request
        }
    })
    .then(function(response) {
        if (!response.ok) {
            throw new Error('Enter a description for post ');
        }
        // Check if response is JSON or HTML
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return response.json();
        }
        return response.text();
    })
    .then(function(data) {
        // Handle successful submission
        if (typeof data === 'object' && data.redirect_url) {
            // If server returns a redirect URL
            window.location.href = data.redirect_url;
        } else if (typeof data === 'object' && data.success) {
            // If server returns success message
            window.location.href = '/home/'; // Default redirect, adjust as needed
        } else {
            // If server returns HTML (like a redirect), just navigate
            window.location.href = '/home/'; // Default redirect, adjust as needed
        }
    })
    .catch(function(error) {
        // Handle errors
        console.error('Upload error:', error);
        showCustomAlert('Upload failed: ' + error.message);

        // Re-enable submit button
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Publish Product';
        }
    });

    return false;
});



// ============================================
// INIT
// ============================================
document.addEventListener('mousemove', function(e) {
    var g = document.getElementById('mouseGlow');
    if (g) { g.style.left = e.clientX + 'px'; g.style.top = e.clientY + 'px'; }
});
addItem();







// function showAlert(message, type = "error") {
//
//     const container = document.getElementById("alertContainer");
//
//     if (!container) {
//         return;
//     }
//
//     container.innerHTML = "";
//
//     let messages = [];
//
//     if (Array.isArray(message)) {
//         messages = message;
//     } else {
//         messages = [message];
//     }
//
//     const alert = document.createElement("div");
//
//     alert.className =
//         type === "success"
//             ? "custom-alert success-alert"
//             : "custom-alert error-alert";
//
//     const icon =
//         type === "success"
//             ? "fa-circle-check"
//             : "fa-circle-exclamation";
//
//     const title =
//         type === "success"
//             ? "Success"
//             : "Please check your information";
//
//     alert.innerHTML = `
//         <div class="alert-icon">
//             <i class="fa-solid ${icon}"></i>
//         </div>
//
//         <div class="alert-content">
//             <strong>${title}</strong>
//
//             <div class="alert-messages">
//                 ${messages.map(msg => `<div>${msg}</div>`).join("")}
//             </div>
//         </div>
//
//         <button type="button"
//                 class="alert-close"
//                 onclick="closeAlert(this)">
//             <i class="fa-solid fa-xmark"></i>
//         </button>
//     `;
//
//     container.appendChild(alert);
// }


// ============================================
// CENTER ERROR ALERT
// ============================================

function showCustomAlert(message) {

    // Remove existing alert
    const existingAlert = document.querySelector('.center-error-alert');

    if (existingAlert) {
        existingAlert.remove();
    }

    // Get overlay
    const overlay = document.getElementById('alertOverlay');

    // Show white transparent background
    if (overlay) {
        overlay.classList.add('active');
    }

    // Create alert
    const alert = document.createElement('div');

    alert.className = 'center-error-alert';

    alert.innerHTML = `
        <button type="button"
                class="alert-close-btn"
                onclick="closeAlert(this)"
                aria-label="Close alert">
            <i class="fa-solid fa-xmark"></i>
        </button>

        <div class="alert-icon">
            <i class="fa-solid fa-circle-exclamation"></i>
        </div>

        <h3>Please check your information</h3>

        <p>${message}</p>
    `;

    document.body.appendChild(alert);

    // Animate alert
    requestAnimationFrame(function () {
        alert.classList.add('show');
    });
}

// ============================================
// CLOSE CENTER ALERT
// ============================================

function closeAlert(button) {

    const alert = button.closest('.center-error-alert');
    const overlay = document.getElementById('alertOverlay');

    if (alert) {
        alert.classList.remove('show');

        setTimeout(function () {
            alert.remove();
        }, 200);
    }

    // Hide overlay
    if (overlay) {
        overlay.classList.remove('active');
    }
}