let allUpdateButtons = document.querySelectorAll(".update-cart");

allUpdateButtons.forEach((element) => {
  element.addEventListener("click", () => {
    let productId = element.dataset.product;
    let action = element.dataset.action;

    console.log("USER : ", user);
    if (user == "AnonymousUser") {
      addCookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
    console.log("Product ID : ", productId, "Action : ", action);
  });
});

const addCookieItem = (productId, action) => {
  console.log("User is not authenticated");

  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId]["quantity"]++;
    }
  }
  if (action == "remove") {
    cart[productId]["quantity"]--;
    if (cart[productId]["quantity"] <= 0) {
      console.log("Item should be delete");
      delete cart[productId];
    }
  }
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
};

const updateUserOrder = (productId, action) => {
  console.log("Update user order work");
  let url = "/update_item/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      location.reload();
    });
};
