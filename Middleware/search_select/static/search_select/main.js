const resultsContainer = document.getElementById('results');
const selectedItemsBody = document.getElementById('selected-items-body');
function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

function removeItems(items) {
    items.forEach(item => {
        const element = Array.from(results.children).filter(child => child.textContent === item);
        if (element) {
            element.forEach(element => {
                element.classList.add('slide-out');
                element.addEventListener('animationend', () => {
                    element.remove();
                })
            });
        }
    });
}

function addItems(items, selector, limit) {
    items.some((item, index) => {
        if (limit && index == limit) {
            const ellipsis = document.createElement('div');
            ellipsis.className = 'result-item';
            ellipsis.textContent = '...';
            resultsContainer.appendChild(ellipsis);
            return true;
        }

        const div = document.createElement('div');
        div.id = item.id;
        div.className = 'result-item';
        div.textContent = item.display;
        div.addEventListener('click', () => {
            addToSelectedItems(item, selector);
        });
        resultsContainer.appendChild(div);
    });
}

function displayResults(items, selector, limit) {
    // Get the current items in the results
    const currentItems = Array.from(resultsContainer.children).map(child => child.textContent);
    // Determine which items are new and which are removed
    const newItems = items.filter(item => !currentItems.includes(item));
    const removedItems = currentItems.filter(item => !items.includes(item));

    // Remove items with slideOut animation
    if (removedItems.length) {
        removeItems(removedItems);
    }

    // Add new items with slideIn animation
    if (newItems.length) {
        addItems(newItems, selector, limit);
    }
}

function addToSelectedItems(item, selector) {
    const totalForms = document.getElementById('id_scores-TOTAL_FORMS');
    const currentFormCount = parseInt(totalForms.value);
    const emptyForm = document.querySelector('#empty-form').cloneNode(true);
    emptyForm.style.display = 'block';
    const newFormHtml = emptyForm.innerHTML.replace(/__prefix__/g, currentFormCount);
    const newFormRow = document.createElement('tr');
    newFormRow.innerHTML = newFormHtml;
    newFormRow.querySelector('select').value = item.id;
    document.querySelector(selector).appendChild(newFormRow);
    totalForms.value = currentFormCount + 1;
}

function fetchItems(modelUrl, searchField, selector, limit=15) {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const params = new URLSearchParams();

    if (searchTerm) {
        resultsContainer.style.display = "flex";
        params.append(searchField, searchTerm);
        modelUrl += '?' + params.toString();
        fetch(modelUrl)
            .then(response => response.json())
            .then(items => {
                displayResults(items.map(item => ({ display: item[searchField], id: item.id })), selector, limit); // Change the limit here
            })
            .catch(error => {
                console.error('Error fetching items:', error);
            });
    } else {
        resultsContainer.style.display = "none";
    }
}

const debouncedFetchItems = debounce(fetchItems, 400);
