const productGrid = document.getElementById("productGrid");
const searchInput = document.getElementById("searchInput");
const sortBtn = document.getElementById("sortBtn");

let products = [];
let sortedHigh = false;

// Fetch products
fetch("https://dummyjson.com/products")
  .then(res => res.json())
  .then(data => {
    products = data.products;
    renderProducts(products);
  });

// Render function
function renderProducts(items) {
  productGrid.innerHTML = "";

  items.forEach(product => {
    const card = document.createElement("div");
    card.className = "card";

    card.innerHTML = `
      <span class="badge">NEW</span>
      <img src="${product.thumbnail}" alt="${product.title}">
      <h3>${product.title}</h3>
      <p class="price">$${product.price}</p>
    `;

    productGrid.appendChild(card);
  });
}

// Search
searchInput.addEventListener("input", () => {
  const value = searchInput.value.toLowerCase();
  const filtered = products.filter(p =>
    p.title.toLowerCase().includes(value)
  );
  renderProducts(filtered);
});

// Sort
sortBtn.addEventListener("click", () => {
  sortedHigh = !sortedHigh;

  const sorted = [...products].sort((a, b) =>
    sortedHigh ? b.price - a.price : a.price - b.price
  );

  sortBtn.innerText = sortedHigh
    ? "Sort: Low → High"
    : "Sort: High → Low";

  renderProducts(sorted);
});
