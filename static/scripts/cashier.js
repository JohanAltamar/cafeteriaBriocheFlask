const http = new EasyHTTP();
const url = "http://localhost:5000";

const searchButton = document.getElementById("search-product-btn");
const searchField = document.getElementById("product_name");
const productsGallery = document.getElementsByClassName("products-gallery")[0];
const cartItemsContainer = document.getElementsByClassName(
  "cart-items-container"
)[0];

searchField.addEventListener("keyup", (event) => {
  let { value } = searchField;

  const { key } = event;
  if (key === "Escape") {
    searchField.value = "";
    removeElements(productsGallery);
  }

  if (value.length < 3) {
    removeElements(productsGallery);
  }
});

const searchProduct = (event) => {
  event.preventDefault();

  let { value } = searchField;

  if (value.length >= 3) {
    http
      .get(`${url}/products?name=${value}`)
      .then((data) => addProductToDOM(data))
      .catch((err) => console.error(err));
  }
};

const addProductToDOM = (products) => {
  // console.log(products);
  products.forEach((product) => {
    const card = document.createElement("div");
    card.classList.add("product-card");

    const title = document.createElement("h2");
    title.classList.add("product-card-title");
    title.innerText = product[1];

    const image = document.createElement("img");
    image.classList.add("product-card-image");
    image.src = `/static/images/${product[3]}`;

    const price = document.createElement("h2");
    price.classList.add("product-card-price");
    price.innerText = `$ ${product[2].toLocaleString("de-DE")}`;

    card.append(title, image, price);
    card.id = product[0];
    card.addEventListener("click", (evt) =>
      handleProductCardClick(evt, product[0])
    );
    productsGallery.appendChild(card);
  });
};

const handleProductCardClick = (event, productID) => {
  // console.log(productID);
  http
    .post(`${url}/add-product-to-order/${productID}`, {})
    .then(http.get(`${url}/get-order-info`))
    .then((data) => {
      listProducts(data);
    })
    .catch((error) => console.error(error));
};

window.addEventListener("load", () => {
  http
    .get(`${url}/get-order-info`)
    .then((data) => listProducts(data))
    .catch((err) => console.error(err));
});

const listProducts = (products) => {
  const cartTotalContainer = document.getElementsByClassName(
    "cart-total-container"
  )[0];

  removeElements(cartItemsContainer);
  removeElements(cartTotalContainer);

  let total;
  products.forEach((item) => {
    const cartItem = document.createElement("div");
    cartItem.classList.add("cart-item");

    const cartItemResume = document.createElement("div");
    cartItemResume.classList.add("cart-item-resume");
    const cartItemName = document.createElement("h4");
    cartItemName.innerText = item[2];
    const cartItemTotal = document.createElement("h4");
    cartItemTotal.innerText = `$ ${(item[3] * item[4]).toLocaleString(
      "de-DE"
    )}`;
    cartItemResume.append(cartItemName, cartItemTotal);

    const cartItemDetails = document.createElement("div");
    cartItemDetails.classList.add("cart-item-details");
    const cartItemQty = document.createElement("span");
    cartItemQty.innerText = `x${item[4]} `;
    const cartItemPrice = document.createElement("span");
    cartItemPrice.innerText = `$ ${item[3].toLocaleString("de-DE")}`;
    cartItemDetails.append(cartItemQty, cartItemPrice);

    cartItem.append(cartItemResume, cartItemDetails);
    // console.log(item[2], item[3], item[4]);
    cartItemsContainer.appendChild(cartItem);
    total = item[6];
  });

  const totalTitle = document.createElement("h3");
  totalTitle.innerText = "Total";
  const totalTag = document.createElement("h3");
  totalTag.innerText = `$ ${total.toLocaleString("de-DE")}`;
  cartTotalContainer.append(totalTitle, totalTag);
};

const removeElements = (component) => {
  while (component.hasChildNodes()) {
    component.removeChild(component.firstChild);
  }
};
