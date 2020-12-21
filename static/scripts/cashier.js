const http = new EasyHTTP();
const url = server_url;

const searchButton = document.getElementById("search-product-btn");
const searchField = document.getElementById("product_name");
const productsGallery = document.getElementsByClassName("products-gallery")[0];
const cartItemsContainer = document.getElementsByClassName(
  "cart-items-container"
)[0];
const cartTotalContainer = document.getElementsByClassName(
  "cart-total-container"
)[0];
const cartCheckoutContainer = document.getElementsByClassName(
  "cart-checkout-container"
)[0];

searchField.addEventListener("keyup", (event) => {
  let { value } = searchField;

  const { key } = event;
  if (key === "Escape") {
    searchField.value = "";
    removeElements(productsGallery);
    http
      .get(`${url}/products?name=`)
      .then((data) => addProductToDOM(data))
      .catch((err) => console.error(err));
  }

  if (value.length < 1) {
    removeElements(productsGallery);
    http
      .get(`${url}/products?name=`)
      .then((data) => addProductToDOM(data))
      .catch((err) => console.error(err));
  }
});

const searchProduct = (event) => {
  event.preventDefault();

  let { value } = searchField;

  if (value.length >= 3) {
    removeElements(productsGallery);
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

const handleProductCartAddClick = (productID) => {
  // console.log(productID);
  http
    .post(`${url}/add-product-to-order/${productID}`, {})
    .then(http.get(`${url}/get-order-info`))
    .then((data) => {
      listProducts(data);
    })
    .catch((error) => console.error(error));
};

const handleProductCartSubClick = (productID) => {
  // console.log(productID);
  http
    .post(`${url}/sub-product-from-order/${productID}`, {})
    .then(http.get(`${url}/get-order-info`))
    .then((data) => {
      if (data.length != undefined) {
        listProducts(data);
      }
    })
    .catch((error) => console.error(error));
};

const handleCartCheckoutClick = () => {
  http
    .post(`${url}/order-checkout`, {})
    .then(http.get(`${url}/get-order-info`))
    .then((data) => {
      if (data.length != undefined) {
        listProducts(data);
      }
      removeElements(cartItemsContainer);
      removeElements(cartTotalContainer);
      removeElements(cartCheckoutContainer);
      alert("Orden Finalizada con éxito");
    })
    .catch((error) => console.error(error));
};

const handleEmptyCartButton = () => {
  http
    .post(`${url}/empty-cart`, {})
    .then((data) => {
      removeElements(cartItemsContainer);
      removeElements(cartTotalContainer);
      removeElements(cartCheckoutContainer);
    })
    .catch((error) => console.error(error));
};

window.addEventListener("load", () => {
  http
    .get(`${url}/get-order-info`)
    .then((data) => {
      if (data.length != undefined) {
        listProducts(data);
      }
    })
    .catch((err) => console.error(err));
});

window.addEventListener("DOMContentLoaded", () => {
  http
    .get(`${url}/products?name=`)
    .then((data) => {
      addProductToDOM(data);
    })
    .catch((err) => console.error(err));
});

const listProducts = (products) => {
  removeElements(cartItemsContainer);
  removeElements(cartTotalContainer);
  removeElements(cartCheckoutContainer);

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

    const cardItemAdd = document.createElement("button");
    cardItemAdd.classList.add("cart-button");
    cardItemAdd.innerText = "+";
    cardItemAdd.addEventListener("click", () => {
      handleProductCartAddClick(item[1]);
    });
    const cardItemSub = document.createElement("button");
    cardItemSub.classList.add("cart-button");
    cardItemSub.innerText = "-";
    cardItemSub.addEventListener("click", () => {
      handleProductCartSubClick(item[1]);
    });

    const cartItemQty = document.createElement("span");
    cartItemQty.innerText = `x${item[4]} `;
    const cartItemPrice = document.createElement("span");
    cartItemPrice.innerText = `$ ${item[3].toLocaleString("de-DE")}`;
    cartItemDetails.append(
      cardItemSub,
      cardItemAdd,
      cartItemQty,
      cartItemPrice
    );

    cartItem.append(cartItemResume, cartItemDetails);
    // console.log(item[2], item[3], item[4]);
    cartItemsContainer.appendChild(cartItem);
    total = item[6];
  });

  if (total != undefined) {
    const totalTitle = document.createElement("h3");
    totalTitle.innerText = "Total";
    const totalTag = document.createElement("h3");
    totalTag.innerText = `$ ${total.toLocaleString("de-DE")}`;
    cartTotalContainer.append(totalTitle, totalTag);

    const cartCheckoutButton = document.createElement("button");
    cartCheckoutButton.classList.add("cart-checkout-button");
    cartCheckoutButton.innerText = "Finalizar Venta";
    cartCheckoutButton.addEventListener("click", () => {
      handleCartCheckoutClick();
    });

    const emptyCartButton = document.createElement("button");
    emptyCartButton.classList.add("cart-checkout-button");
    emptyCartButton.innerText = "Vaciar Carrito";
    emptyCartButton.addEventListener("click", () => {
      handleEmptyCartButton();
    });

    cartCheckoutContainer.append(emptyCartButton, cartCheckoutButton);
  }
};

const removeElements = (component) => {
  while (component.hasChildNodes()) {
    component.removeChild(component.firstChild);
  }
};
