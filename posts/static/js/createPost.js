/*==================================================
                ITEMS & SIZES (NEW)
==================================================*/

let itemIndex = 0;
let sizeOptions = [];

function loadSizes() {
    const categorySelect = document.getElementById('categorySelect');
    const categoryId = categorySelect.value;
    const selectedOption = categorySelect.options[categorySelect.selectedIndex];
    const sizeType = selectedOption.dataset.sizeType;

    if (categoryId && sizeType !== 'none') {
        fetch(`/posts/get-category-sizes/${categoryId}/`)
            .then(response => response.json())
            .then(data => {
                sizeOptions = data.sizes;
                updateAllSizeCharts();
            });
    } else {
        sizeOptions = [];
        updateAllSizeCharts();
    }
}

function checkSizeVisibility() {
    const condition = document.getElementById('conditionSelect').value;
    const categorySelect = document.getElementById('categorySelect');
    const selectedOption = categorySelect.options[categorySelect.selectedIndex];
    const sizeType = selectedOption.dataset.sizeType;

    if (condition === 'new' && sizeType !== 'none') {
        loadSizes();
    } else {
        sizeOptions = [];
        updateAllSizeCharts();
    }
}

function addItem() {
    const container = document.getElementById('itemsContainer');
    const currentIndex = itemIndex;

    const itemHTML = `
        <div class="glass-card item-section" id="item${currentIndex}">
            <div class="item-header">
                <h3><i class="fa-solid fa-box"></i> Item ${currentIndex + 1}</h3>
                <button type="button" class="remove-item-btn" onclick="removeItem(${currentIndex})">
                    <i class="fa-solid fa-trash"></i> Remove Item
                </button>
            </div>

            <input type="hidden" name="item_count" value="${currentIndex + 1}">

            <div class="product-grid">
                <div class="input-card">
                    <label><i class="fa-solid fa-tag"></i> Item Name *</label>
                    <input type="text" name="item_name_${currentIndex}" placeholder="e.g., Blue Cotton T-Shirt" required>
                </div>

                <div class="input-card">
                    <label><i class="fa-solid fa-money-bill-wave"></i> Price (MMK) *</label>
                    <input type="number" name="item_price_${currentIndex}" placeholder="Enter price" required min="1">
                </div>
            </div>

            <div class="description-card">
                <label><i class="fa-solid fa-align-left"></i> Item Description</label>
                <textarea name="item_description_${currentIndex}" placeholder="Describe this item..."></textarea>
                <small>Include brand, colour, size, material and any other details</small>
            </div>

            <div class="section-title">
                <i class="fa-regular fa-images"></i>
                <div>
                    <h2>Item Images</h2>
                    <p>Upload photos for this item</p>
                </div>
            </div>

            <label for="fileInput${currentIndex}" class="item-upload-area">
                <div class="upload-icon">
                    <i class="fa-solid fa-cloud-arrow-up"></i>
                </div>
                <h3>Upload Photos</h3>
                <p>Click to browse your computer</p>
                <span>Maximum 5 Images</span>
                <input type="file" id="fileInput${currentIndex}" name="images_${currentIndex}" multiple accept="image/*" style="display:none" onchange="handleFileSelect(this, ${currentIndex})">
            </label>

            <div class="preview-grid" id="previewGrid${currentIndex}"></div>

            <div id="sizeChart${currentIndex}" class="size-chart hidden">
                <label><i class="fa-solid fa-ruler"></i> Select Sizes</label>
                <div class="size-buttons" id="sizeButtons${currentIndex}"></div>
            </div>

            <div id="selectedSizes${currentIndex}" class="selected-sizes hidden">
                <input type="hidden" name="size_count_${currentIndex}" id="sizeCount${currentIndex}" value="0">
            </div>

            <button type="button" class="add-sizes-btn hidden" id="addMoreSizes${currentIndex}" onclick="toggleSizeChart(${currentIndex})">
                <i class="fa-solid fa-plus"></i> Add Sizes
            </button>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', itemHTML);
    itemIndex++;
    updateAllSizeCharts();
}

function removeItem(index) {
    const item = document.getElementById(`item${index}`);
    if (item) {
        item.remove();
    }
}

function handleFileSelect(input, itemIndex) {
    const files = input.files;
    const previewGrid = document.getElementById(`previewGrid${itemIndex}`);
    previewGrid.innerHTML = '';

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();

        reader.onload = function(e) {
            const previewHTML = `
                <div class="preview-card">
                    <div class="image-frame">
                        <img src="${e.target.result}" alt="Preview">
                        ${i === 0 ? '<div class="cover-tag"><i class="fa-solid fa-star"></i> Cover</div>' : ''}
                    </div>
                </div>
            `;
            previewGrid.insertAdjacentHTML('beforeend', previewHTML);
        };

        reader.readAsDataURL(file);
    }
}

function updateAllSizeCharts() {
    for (let i = 0; i < itemIndex; i++) {
        const sizeChart = document.getElementById(`sizeChart${i}`);
        const addMoreBtn = document.getElementById(`addMoreSizes${i}`);

        if (sizeChart && addMoreBtn) {
            if (sizeOptions.length > 0) {
                sizeChart.classList.remove('hidden');
                addMoreBtn.classList.remove('hidden');
                populateSizeButtons(i);
            } else {
                sizeChart.classList.add('hidden');
                addMoreBtn.classList.add('hidden');
            }
        }
    }
}

function populateSizeButtons(itemIndex) {
    const sizeButtons = document.getElementById(`sizeButtons${itemIndex}`);
    if (!sizeButtons) return;
    sizeButtons.innerHTML = '';

    sizeOptions.forEach(size => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'size-btn';
        button.textContent = size;
        button.onclick = function() {
            toggleSize(itemIndex, size, button);
        };
        sizeButtons.appendChild(button);
    });
}

let selectedSizes = {};

function toggleSize(itemIndex, size, button) {
    if (!selectedSizes[itemIndex]) {
        selectedSizes[itemIndex] = [];
    }

    const index = selectedSizes[itemIndex].findIndex(s => s.size === size);

    if (index === -1) {
        selectedSizes[itemIndex].push({size: size, quantity: 0});
        button.classList.add('active');
    } else {
        selectedSizes[itemIndex].splice(index, 1);
        button.classList.remove('active');
    }

    updateSelectedSizesDisplay(itemIndex);
}

function updateSelectedSizesDisplay(itemIndex) {
    const selectedSizesDiv = document.getElementById(`selectedSizes${itemIndex}`);
    if (!selectedSizesDiv) return;

    if (!selectedSizes[itemIndex] || selectedSizes[itemIndex].length === 0) {
        selectedSizesDiv.innerHTML = `<input type="hidden" name="size_count_${itemIndex}" id="sizeCount${itemIndex}" value="0">`;
        selectedSizesDiv.classList.add('hidden');
        return;
    }

    selectedSizesDiv.classList.remove('hidden');

    let html = `<h4><i class="fa-solid fa-circle-check"></i> Selected Sizes</h4>`;
    html += `<input type="hidden" name="size_count_${itemIndex}" id="sizeCount${itemIndex}" value="${selectedSizes[itemIndex].length}">`;

    selectedSizes[itemIndex].forEach((sizeObj, j) => {
        html += `
            <div class="size-row">
                <span class="size-label">${sizeObj.size}</span>
                <div class="quantity-wrapper">
                    <input type="number" class="quantity-input" name="quantity_${itemIndex}_${j}" placeholder="Qty" value="${sizeObj.quantity || ''}" min="0" required>
                </div>
                <input type="hidden" name="size_${itemIndex}_${j}" value="${sizeObj.size}">
                <button type="button" class="remove-size-btn" onclick="removeSize(${itemIndex}, ${j}, '${sizeObj.size}')">
                    <i class="fa-solid fa-times"></i>
                </button>
            </div>
        `;
    });

    selectedSizesDiv.innerHTML = html;
}

function removeSize(itemIndex, sizeIndex, size) {
    selectedSizes[itemIndex].splice(sizeIndex, 1);

    const sizeButtons = document.getElementById(`sizeButtons${itemIndex}`);
    if (sizeButtons) {
        const buttons = sizeButtons.getElementsByClassName('size-btn');
        for (let button of buttons) {
            if (button.textContent === size) {
                button.classList.remove('active');
                break;
            }
        }
    }

    updateSelectedSizesDisplay(itemIndex);
}

function toggleSizeChart(itemIndex) {
    const sizeChart = document.getElementById(`sizeChart${itemIndex}`);
    if (sizeChart) {
        sizeChart.classList.toggle('hidden');
    }
}

// Add first item automatically when page loads
document.addEventListener("DOMContentLoaded", () => {
    addItem();
});

console.log("Items & Sizes System Loaded Successfully.");