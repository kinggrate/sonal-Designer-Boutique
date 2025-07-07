// Global variables
let customers = [];
let editingCustomerId = null;

// DOM elements
const customerModal = document.getElementById('customerModal');
const customerForm = document.getElementById('customerForm');
const customersList = document.getElementById('customersList');
const searchInput = document.getElementById('searchInput');
const addNewBtn = document.getElementById('addNewBtn');
const closeBtn = document.querySelector('.close');
const cancelBtn = document.getElementById('cancelBtn');
const submitBtn = document.getElementById('submitBtn');
const modalTitle = document.getElementById('modalTitle');
const customersCount = document.getElementById('customersCount');
const loadingSpinner = document.getElementById('loadingSpinner');
const toast = document.getElementById('toast');
const garmentTypeSelect = document.getElementById('garmentType');

// Garment field containers
const blouseFields = document.getElementById('blouseFields');
const pantFields = document.getElementById('pantFields');
const dressFields = document.getElementById('dressFields');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadCustomers();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    addNewBtn.addEventListener('click', openAddModal);
    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);
    customerForm.addEventListener('submit', handleFormSubmit);
    searchInput.addEventListener('input', handleSearch);
    garmentTypeSelect.addEventListener('change', handleGarmentTypeChange);
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === customerModal) {
            closeModal();
        }
    });
    
    // Handle escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && customerModal.style.display === 'block') {
            closeModal();
        }
    });
}

// Handle garment type change
function handleGarmentTypeChange() {
    const selectedType = garmentTypeSelect.value;
    
    // Hide all field sections
    blouseFields.style.display = 'none';
    pantFields.style.display = 'none';
    dressFields.style.display = 'none';
    
    // Remove active class from all sections
    blouseFields.classList.remove('active');
    pantFields.classList.remove('active');
    dressFields.classList.remove('active');
    
    // Show selected section
    switch(selectedType) {
        case 'blouse':
            blouseFields.style.display = 'block';
            blouseFields.classList.add('active');
            break;
        case 'pant':
            pantFields.style.display = 'block';
            pantFields.classList.add('active');
            break;
        case 'dress':
            dressFields.style.display = 'block';
            dressFields.classList.add('active');
            break;
    }
    
    // Update required fields based on garment type
    updateRequiredFields(selectedType);
}

// Update required fields based on garment type
function updateRequiredFields(garmentType) {
    // Remove all required attributes from measurement fields
    const allMeasurementInputs = document.querySelectorAll('.garment-fields input');
    allMeasurementInputs.forEach(input => {
        input.removeAttribute('required');
    });
    
    // Add required attributes based on garment type
    switch(garmentType) {
        case 'blouse':
            const blouseInputs = blouseFields.querySelectorAll('input');
            blouseInputs.forEach(input => input.setAttribute('required', 'required'));
            break;
        case 'pant':
            const pantInputs = pantFields.querySelectorAll('input');
            pantInputs.forEach(input => input.setAttribute('required', 'required'));
            break;
        case 'dress':
            const dressInputs = dressFields.querySelectorAll('input');
            dressInputs.forEach(input => input.setAttribute('required', 'required'));
            break;
    }
}

// API functions
async function loadCustomers() {
    showLoading(true);
    try {
        const response = await fetch('/api/customers');
        if (response.ok) {
            customers = await response.json();
            renderCustomers(customers);
            updateCustomersCount(customers.length);
        } else {
            showToast('Failed to load customers', 'error');
        }
    } catch (error) {
        console.error('Error loading customers:', error);
        showToast('Error loading customers', 'error');
    } finally {
        showLoading(false);
    }
}

async function saveCustomer(customerData) {
    try {
        const url = editingCustomerId ? `/api/customers/${editingCustomerId}` : '/api/customers';
        const method = editingCustomerId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(customerData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast(editingCustomerId ? 'Customer updated successfully!' : 'Customer added successfully!', 'success');
            closeModal();
            loadCustomers();
        } else {
            showToast(result.error || 'Failed to save customer', 'error');
        }
    } catch (error) {
        console.error('Error saving customer:', error);
        showToast('Error saving customer', 'error');
    }
}

async function deleteCustomer(customerId) {
    if (!confirm('Are you sure you want to delete this customer? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/customers/${customerId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showToast('Customer deleted successfully!', 'success');
            loadCustomers();
        } else {
            showToast('Failed to delete customer', 'error');
        }
    } catch (error) {
        console.error('Error deleting customer:', error);
        showToast('Error deleting customer', 'error');
    }
}

async function searchCustomers(query) {
    try {
        const response = await fetch(`/api/customers/search?q=${encodeURIComponent(query)}`);
        if (response.ok) {
            const searchResults = await response.json();
            renderCustomers(searchResults);
            updateCustomersCount(searchResults.length);
        }
    } catch (error) {
        console.error('Error searching customers:', error);
        showToast('Error searching customers', 'error');
    }
}

// UI functions
function openAddModal() {
    editingCustomerId = null;
    modalTitle.textContent = 'Add New Customer';
    submitBtn.textContent = 'Save Customer';
    customerForm.reset();
    
    // Set default garment type to blouse
    garmentTypeSelect.value = 'blouse';
    handleGarmentTypeChange();
    
    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('deliveryDate').min = today;
    
    customerModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function openEditModal(customer) {
    editingCustomerId = customer.id;
    modalTitle.textContent = 'Edit Customer';
    submitBtn.textContent = 'Update Customer';
    
    // Populate basic fields
    document.getElementById('customerName').value = customer.customer_name;
    document.getElementById('phoneNumber').value = customer.phone_number;
    document.getElementById('garmentType').value = customer.garment_type || 'blouse';
    document.getElementById('deliveryDate').value = customer.delivery_date;
    document.getElementById('additionalNotes').value = customer.additional_notes || '';
    
    // Handle garment type change to show correct fields
    handleGarmentTypeChange();
    
    // Populate garment-specific fields
    switch(customer.garment_type) {
        case 'blouse':
            document.getElementById('shoulder').value = customer.shoulder || '';
            document.getElementById('chest').value = customer.chest || '';
            document.getElementById('bust').value = customer.bust || '';
            document.getElementById('waist').value = customer.waist || '';
            document.getElementById('bustPoint').value = customer.bust_point || '';
            document.getElementById('bustToBust').value = customer.bust_to_bust || '';
            document.getElementById('sleeves').value = customer.sleeves || '';
            document.getElementById('penaltyCrease').value = customer.penalty_crease || '';
            document.getElementById('backNeck').value = customer.back_neck || '';
            document.getElementById('frontNeck').value = customer.front_neck || '';
            document.getElementById('length').value = customer.length || '';
            document.getElementById('lowerChest').value = customer.lower_chest || '';
            break;
        case 'pant':
            document.getElementById('pantWaist').value = customer.pant_waist || '';
            document.getElementById('heap').value = customer.heap || '';
            document.getElementById('pantLength').value = customer.pant_length || '';
            document.getElementById('thigh').value = customer.thigh || '';
            document.getElementById('knee').value = customer.knee || '';
            document.getElementById('bottom').value = customer.bottom || '';
            break;
        case 'dress':
            document.getElementById('dressShoulder').value = customer.dress_shoulder || '';
            document.getElementById('dressChest').value = customer.dress_chest || '';
            document.getElementById('dressWaist').value = customer.dress_waist || '';
            document.getElementById('dressHeap').value = customer.dress_heap || '';
            document.getElementById('dressLength').value = customer.dress_length || '';
            document.getElementById('armWholeRound').value = customer.arm_whole_round || '';
            document.getElementById('dressSleeves').value = customer.dress_sleeves || '';
            document.getElementById('penaltyCircle').value = customer.penalty_circle || '';
            document.getElementById('dressFrontNeck').value = customer.dress_front_neck || '';
            document.getElementById('dressBackNeck').value = customer.dress_back_neck || '';
            document.getElementById('mathaRound').value = customer.matha_round || '';
            break;
    }
    
    customerModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    customerModal.style.display = 'none';
    document.body.style.overflow = 'auto';
    customerForm.reset();
    editingCustomerId = null;
}

function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(customerForm);
    const customerData = {};
    
    for (let [key, value] of formData.entries()) {
        customerData[key] = value.toString().trim();
    }
    
    // Validate required fields
    const requiredFields = ['customer_name', 'phone_number', 'garment_type', 'delivery_date'];
    
    for (let field of requiredFields) {
        if (!customerData[field]) {
            showToast(`Please fill in the ${field.replace('_', ' ')} field`, 'error');
            return;
        }
    }
    
    saveCustomer(customerData);
}

function handleSearch() {
    const query = searchInput.value.trim();
    if (query) {
        searchCustomers(query);
    } else {
        renderCustomers(customers);
        updateCustomersCount(customers.length);
    }
}

function renderCustomers(customersToRender) {
    if (customersToRender.length === 0) {
        customersList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-users"></i>
                <h3>No customers found</h3>
                <p>Start by adding your first customer or try a different search term.</p>
            </div>
        `;
        return;
    }
    
    customersList.innerHTML = customersToRender.map(customer => {
        const measurements = getMeasurementsForGarmentType(customer);
        
        return `
            <div class="customer-card">
                <div class="customer-header">
                    <div class="customer-info">
                        <h3>${escapeHtml(customer.customer_name)}</h3>
                        <div class="phone">
                            <i class="fas fa-phone"></i>
                            ${escapeHtml(customer.phone_number)}
                        </div>
                        <div class="garment-type">${escapeHtml(customer.garment_type || 'blouse')}</div>
                    </div>
                    <div class="customer-actions">
                        <button class="btn btn-edit" onclick="openEditModal(${JSON.stringify(customer).replace(/"/g, '&quot;')})">
                            <i class="fas fa-edit"></i>
                            Edit
                        </button>
                        <button class="btn btn-delete" onclick="deleteCustomer(${customer.id})">
                            <i class="fas fa-trash"></i>
                            Delete
                        </button>
                    </div>
                </div>
                
                <div class="delivery-info">
                    <i class="fas fa-calendar-alt"></i>
                    <strong>Delivery Date: ${formatDate(customer.delivery_date)}</strong>
                </div>
                
                <div class="measurements-grid">
                    ${measurements}
                </div>
                
                ${customer.additional_notes ? `
                    <div class="additional-notes">
                        <h4><i class="fas fa-sticky-note"></i> Additional Notes</h4>
                        <p>${escapeHtml(customer.additional_notes)}</p>
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
}

function getMeasurementsForGarmentType(customer) {
    const garmentType = customer.garment_type || 'blouse';
    
    switch(garmentType) {
        case 'blouse':
            return `
                ${createMeasurementItem('Shoulder', customer.shoulder)}
                ${createMeasurementItem('Chest', customer.chest)}
                ${createMeasurementItem('Bust', customer.bust)}
                ${createMeasurementItem('Waist', customer.waist)}
                ${createMeasurementItem('Bust Point', customer.bust_point)}
                ${createMeasurementItem('Bust to Bust', customer.bust_to_bust)}
                ${createMeasurementItem('Sleeves', customer.sleeves)}
                ${createMeasurementItem('Penalty Crease', customer.penalty_crease)}
                ${createMeasurementItem('Back Neck', customer.back_neck)}
                ${createMeasurementItem('Front Neck', customer.front_neck)}
                ${createMeasurementItem('Length', customer.length)}
                ${createMeasurementItem('Lower Chest', customer.lower_chest)}
            `;
        case 'pant':
            return `
                ${createMeasurementItem('Waist', customer.pant_waist)}
                ${createMeasurementItem('Heap', customer.heap)}
                ${createMeasurementItem('Length', customer.pant_length)}
                ${createMeasurementItem('Thigh', customer.thigh)}
                ${createMeasurementItem('Knee', customer.knee)}
                ${createMeasurementItem('Bottom', customer.bottom)}
            `;
        case 'dress':
            return `
                ${createMeasurementItem('Shoulder', customer.dress_shoulder)}
                ${createMeasurementItem('Chest', customer.dress_chest)}
                ${createMeasurementItem('Waist', customer.dress_waist)}
                ${createMeasurementItem('Heap', customer.dress_heap)}
                ${createMeasurementItem('Length', customer.dress_length)}
                ${createMeasurementItem('Arm Whole Round', customer.arm_whole_round)}
                ${createMeasurementItem('Sleeves', customer.dress_sleeves)}
                ${createMeasurementItem('Penalty Circle', customer.penalty_circle)}
                ${createMeasurementItem('Front Neck', customer.dress_front_neck)}
                ${createMeasurementItem('Back Neck', customer.dress_back_neck)}
                ${createMeasurementItem('Matha Round', customer.matha_round)}
            `;
        default:
            return '';
    }
}

function createMeasurementItem(label, value) {
    if (!value) return '';
    return `
        <div class="measurement-item">
            <div class="measurement-label">${label}</div>
            <div class="measurement-value">${escapeHtml(value)}</div>
        </div>
    `;
}

function updateCustomersCount(count) {
    customersCount.textContent = count;
}

function showLoading(show) {
    loadingSpinner.style.display = show ? 'block' : 'none';
}

function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Utility functions
function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Make functions globally available for onclick handlers
window.openEditModal = openEditModal;
window.deleteCustomer = deleteCustomer;