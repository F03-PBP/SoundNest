
let isLoaded = false;

document.addEventListener("DOMContentLoaded", function () {
    // Check if user is admin (staff)
    const isAdmin = document.querySelector('[data-is-staff="true"]') !== null;

    fetch('/show_json/')
    .then(response => {
        console.log("Response status:", response.status);
        return response.json();
    })
    .then(data => {
        console.log("Received data:", data);
    })
    .catch(error => {
        console.error("Error fetching data:", error);
    });

    if (isLoaded) return;
    isLoaded = true;

    const bestDealsHeader = document.getElementById("bestDealsHeader");
    bestDealsHeader.classList.remove("opacity-0", "translate-x-[-50px]");
    bestDealsHeader.classList.add("opacity-100", "translate-x-0");

    const topPicksContainer = document.getElementById('topPicksContainer');
    const latestDealsContainer = document.getElementById('latestDealsContainer');
    const productList = document.getElementById("productList");

    if (isAdmin) {
        const openAddModalBtn = document.getElementById("addToDealsBtn");
        if (openAddModalBtn) {
            openAddModalBtn.addEventListener("click", () => toggleModal(addModal, true));
        }

        const closeAddModalBtn = document.getElementById("closeAddModalBtn");
        if (closeAddModalBtn) {
            closeAddModalBtn.addEventListener("click", () => toggleModal(addModal, false));
        }

        const closeEditModalBtn = document.getElementById("closeEditModalBtn");
        if (closeEditModalBtn) {
            closeEditModalBtn.addEventListener("click", () => toggleModal(editModal, false));
        }
    }

    async function fetchBestDeals() {
        try {
            const response = await fetch("/best-deals/json");
            const data = await response.json();

            // Clear existing content
            topPicksContainer.innerHTML = '';
            latestDealsContainer.innerHTML = '';
            productList.innerHTML = '';

            // Determine if user is authenticated
            const isAuthenticated = document.body.classList.contains('user-authenticated');
             // Remove any existing empty state messages
            document.querySelectorAll(".no-products-message").forEach(msg => msg.remove());

            if (data.available_products.length) {
                data.available_products.forEach(product => {
                    const productCard = `
                        <div class="product-card cursor-pointer p-4 bg-gray-100 rounded-lg shadow hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600" data-product-id="${product.id}">
                            <h4 class="text-lg font-bold text-gray-800 dark:text-white">${product.product_name}</h4>
                            <p class="text-sm text-gray-500 dark:text-gray-300">Original Price: ${product.price}</p>
                            <p class="text-sm text-gray-500 dark:text-gray-300">Rating: ${product.rating}</p>
                        </div>
                    `;
                    productList.innerHTML += productCard;
                });
            } else {
                productList.innerHTML = '<p>No products available.</p>';
            }
            // Display products based on authentication status
            const topPicksToShow = isAuthenticated ? data.top_picks : data.top_picks.slice(0, 5);
            const latestDealsToShow = isAuthenticated ? data.least_countdown : data.least_countdown.slice(0, 5);
            // Display top picks
            topPicksToShow.forEach(product_sale => {
                topPicksContainer.innerHTML += createProductCard(product_sale);
            });

            // Display latest deals
            latestDealsToShow.forEach(product_sale => {
                latestDealsContainer.innerHTML += createProductCard(product_sale);
            });

            // Add event listeners for edit and delete buttons
            setupEventListeners();
            setupFilterListeners();
            
            // Apply any existing filter
            if (discountFilter.value !== "all") {
                applyDiscountFilter();
            }
        } catch (error) {
            console.error("Error fetching best deals:", error);
        }
    }

    //filter berdasarkan diskon
    const discountFilter = document.getElementById("discountFilter");

   // Add filter event listeners after data is loaded
    function setupFilterListeners() {
        discountFilter.addEventListener("change", applyDiscountFilter);
        // Apply initial filter if not set to "all"
        if (discountFilter.value !== "all") {
            applyDiscountFilter();
        }
    }

    function applyDiscountFilter() {
        const selectedFilter = discountFilter.value;
        
        // Get both containers
        const topPicksContainer = document.getElementById('topPicksContainer');
        const latestDealsContainer = document.getElementById('latestDealsContainer');
        
        // Function to filter products in a container
        function filterContainer(container) {
            const productCards = container.querySelectorAll(".product-card");
            let visibleCount = 0;
            
            productCards.forEach(card => {
                const discountBadge = card.querySelector(".bg-red-500");
                if (!discountBadge) return;
                
                const discount = parseFloat(discountBadge.textContent.replace(/[^0-9.]/g, ''));
                if (isNaN(discount)) return;
                
                let shouldDisplay = true;
                
                switch (selectedFilter) {
                    case "lt25":
                        shouldDisplay = discount < 25;
                        break;
                    case "25-50":
                        shouldDisplay = discount >= 25 && discount <= 50;
                        break;
                    case "50-75":
                        shouldDisplay = discount > 50 && discount <= 75;
                        break;
                    case "gt75":
                        shouldDisplay = discount > 75;
                        break;
                    case "all":
                    default:
                        shouldDisplay = true;
                        break;
                }
                
                card.classList.toggle('hidden', !shouldDisplay);
                if (shouldDisplay) visibleCount++;
            });
            
            // Update empty state message
            updateContainerEmptyState(container, container.id === 'topPicksContainer' ? 'top-picks' : 'latest-deals');
        }
        
        // Apply filter to both containers
        filterContainer(topPicksContainer);
        filterContainer(latestDealsContainer);
    }

    function updateContainerEmptyState(container, containerType) {
        const visibleProducts = container.querySelectorAll(".product-card:not(.hidden)");
        const existingMessage = container.querySelector(".no-products-message");
        
        if (visibleProducts.length === 0) {
            if (!existingMessage) {
                const message = document.createElement("p");
                message.className = "no-products-message text-gray-500 dark:text-gray-400 text-center py-4";
                message.textContent = `No ${containerType.replace("-", " ")} available in this discount range.`;
                container.appendChild(message);
            }
        } else if (existingMessage) {
            existingMessage.remove();
        }
    }

    function formatPrice(number) {
        // Convert to string and split by decimal point if exists
        const parts = number.toString().split('.');
        
        // Format the whole number part with dots
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        
        // Join back with decimal part if it exists
        return parts.join('.');
    }

     // Modified createProductCard function to include admin-specific buttons
     function createProductCard(product_sale) {
        const stars = Array(5).fill('').map((_, index) => 
            index < Math.floor(product_sale.rating) 
                ? '★' 
                : '☆'
        ).join('');
    
        // Admin actions HTML - only included if user is admin
        const adminActions = isAdmin ? `
            <div class="flex gap-2 mt-2">
                <button class="flex-1 bg-yellow-500 hover:bg-yellow-700 text-white font-medium py-2 px-4 rounded flex items-center justify-center gap-2 edit-deals" 
                    data-product-id="${product_sale.id}" 
                    data-discount="${product_sale.discount}" 
                    data-end="${product_sale.sale_end_time}">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                    Edit
                </button>
                <button class="flex-1 bg-red-500 hover:bg-red-700 text-white font-medium py-2 px-4 rounded flex items-center justify-center gap-2 delete-deals" 
                    data-product-id="${product_sale.id}">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    Delete
                </button>
            </div>` : '';
    
        return `
            <div class="relative bg-white shadow-md rounded-lg overflow-hidden product-card group">
                <div class="absolute top-2 left-2 bg-red-500 text-white text-sm px-2 py-1 rounded">
                    -${product_sale.discount}%
                </div>
                
                <div class="absolute top-2 right-2 flex flex-col gap-2">
                    <button class="bg-white p-2 rounded-full shadow-md hover:bg-gray-100 transition-colors">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                        </svg>
                    </button>
                    <button class="bg-white p-2 rounded-full shadow-md hover:bg-gray-100 transition-colors">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                    </button>
                </div>
    
                <div class="aspect-square bg-gray-100">
                    <img 
                        src="${imageUrl}"
                        alt="${product_sale.product_name}" 
                        class="w-full h-full object-cover"
                    />
                </div>
    
                <div class="p-4">
                    <h3 class="text-lg font-medium text-gray-900 mb-2">${product_sale.product_name}</h3>
                    
                    <div class="flex items-center gap-1 mb-2">
                        <span class="text-sm text-gray-900">${product_sale.rating.toFixed(1)}</span>
                        <span class="text-yellow-400">★</span>
                        <span class="text-sm text-gray-600">(${product_sale.reviews || 0})</span>
                    </div>
    
                    <div class="flex items-center gap-2 mb-3">
                        <span class="text-lg font-bold text-gray-900">Rp${formatPrice(product_sale.price)}</span>
                        <span class="text-sm text-gray-500 line-through">Rp${formatPrice(product_sale.original_price)}</span>
                    </div>
    
                    <p class="text-sm font-medium mb-3">
                        Sales ends in: 
                        <span class="time-remaining ${product_sale.time_remaining === 'Sale ended' ? 'text-red-500' : 'text-green-500'}">
                            ${product_sale.time_remaining}
                        </span>
                    </p>
    
                    ${adminActions}
                </div>
            </div>`;
    }

    

    function startTimeRefresh() {
        setInterval(async () => {
            await fetchBestDeals();  // Refresh the list every minute
            await deleteExpiredDeals(); // Automatically delete expired deals every minute
        }, 60000);
    }
    
    async function deleteExpiredDeals() {
        try {
            const response = await fetch("/best-deals/json");
            if (!response.ok) {
                throw new Error('Failed to fetch deals data');
            }
            
            const data = await response.json();
            
            const deletePromises = data.least_countdown
                .filter(product_sale => product_sale.time_remaining === "Sale ended")
                .map(async product_sale => {
                    try {
                        const deleteResponse = await fetch(
                            `/best-deals/delete-deals/${product_sale.product.id}/`, 
                            { method: 'DELETE' }
                        );
                        
                        if (!deleteResponse.ok) {
                            console.error(
                                `Failed to delete expired product with ID ${product_sale.product.id}`
                            );
                        }
                    } catch (error) {
                        console.error("Error deleting expired deal:", error);
                    }
                });
            
            await Promise.all(deletePromises);
        } catch (error) {
            console.error("Error in deleteExpiredDeals:", error);
        }
    }

    function setupEventListeners() {
        // Delete buttons
        document.querySelectorAll('.delete-deals').forEach(button => {
            button.addEventListener('click', handleDelete);
        });

        // Edit buttons
        document.querySelectorAll('.edit-deals').forEach(button => {
            button.addEventListener('click', handleEdit);
        });
    }

    async function handleDelete(e) {
        const productId = e.currentTarget.getAttribute('data-product-id');
        if (confirm('Are you sure you want to remove this product from deals?')) {
            try {
                const response = await fetch(`/best-deals/delete-deals/${productId}/`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    await fetchBestDeals(); // Refresh the data
                    // alert('Product removed successfully');
                } else {
                    alert('Failed to remove product');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while removing the product');
            }
        }
    }

    function handleEdit(e) {
        const button = e.currentTarget;
        const productId = button.getAttribute('data-product-id');
        const discount = button.getAttribute('data-discount');
        const endDate = new Date(button.getAttribute('data-end'));

        

        // Get individual parts of the local date and time
        const year = endDate.getFullYear();
        const month = String(endDate.getMonth() + 1).padStart(2, '0'); // Months are 0-based
        const day = String(endDate.getDate()).padStart(2, '0');
        const hours = String(endDate.getHours()).padStart(2, '0');
        const minutes = String(endDate.getMinutes()).padStart(2, '0');

        // Format to 'YYYY-MM-DDTHH:MM'
        const formattedDate = `${year}-${month}-${day}T${hours}:${minutes}`;
        

        // Set values in the edit modal
        document.getElementById("editDiscount").value = discount;
        document.getElementById("editEndDate").value = formattedDate;
        
        // Show the edit modal
        toggleModal(editModal, true);

        // Setup the form submission
        const editForm = document.getElementById("editDealsForm");
        editForm.onsubmit = async function(e) {
            e.preventDefault();
            
            const newDiscount = document.getElementById("editDiscount").value;
            const newEndDate = document.getElementById("editEndDate").value;

            try {
                const response = await fetch(`/best-deals/edit-deals/${productId}/`, {
                    method: 'PUT',
                    headers: { 
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        discount: newDiscount,
                        end_date: newEndDate
                    })
                });

                if (response.ok) {
                    toggleModal(editModal, false);
                    await fetchBestDeals();
                    // alert("Deal updated successfully!");
                } else {
                    alert("Failed to update the deal.");
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred while updating the deal.");
            }
        };
    }

    // Modals and Form Elements
    const addModal = document.getElementById("addToDealsModal");
    const editModal = document.getElementById("editDealsModal");
    const addProductForm = document.getElementById("addProductForm");
    const productIdField = document.getElementById("productId");

    // Toggle modal visibility
    const toggleModal = (modal, isVisible) => {
        modal.classList.toggle("hidden", !isVisible);
    };

      
    
        // Product selection
    productList.addEventListener("click", function(e) {
        const card = e.target.closest(".product-card");
        if (!card || !productList.contains(card)) return;
        
        const productId = card.getAttribute("data-product-id");
        const productIdField = document.getElementById("productId");
        
        if (productIdField && productId) {
            productIdField.value = productId;
            document.querySelectorAll(".product-card").forEach(c => 
                c.classList.remove("border-blue-500"));
            card.classList.add("border-blue-500");
        }
    });

    // Add to deals form submission
    addProductForm.addEventListener("submit", async function(e) {
        e.preventDefault();
        // Validate discount value
        discount = document.getElementById("discount").value;
        end_date = new Date(document.getElementById("end_date").value);
        const now = new Date();
        // alert(end_date)
        if (discount <= 0 || discount >= 100) {
            alert("Discount must be between 0 and 100.");
            return; // Exit the function to prevent form submission
        }

        if(end_date <= now){
            alert("End sale date must be in the future.")
            return;
        }
        if (productIdField.value == ""){
            alert("Please select a product before submitting.")
            return;
        }
        
        const formData = {
            product_id: productIdField.value,
            discount: document.getElementById("discount").value,
            end_date: document.getElementById("end_date").value,
        };

        try {
            const response = await fetch("/best-deals/add-to-deals/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                addProductForm.reset();
                toggleModal(addModal, false);
                await fetchBestDeals();
                // alert("Product added to deals successfully!");
            } else {
                const errorData = await response.json();
                alert(errorData.message || "Failed to add product to deals.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while adding the product.");
        }
    });

    // Initial fetch
    fetchBestDeals();

    // Start periodic refresh
    startTimeRefresh();

    // Apply filter after fetching products
    document.addEventListener("DOMContentLoaded", fetchBestDeals);
}, { once: true });
// Add this right after your DOMContentLoaded event
