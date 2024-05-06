let allUpdateButtons = document.querySelectorAll(".update-cart");

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
      if (action == "add") {
        appendAlert("Votre article a été ajouté au panier", "success");
      } else {
        appendAlert("L'article a bien été supprimer", "danger");
      }
    });
};

const filterProduct = () => {
  allFilter = document.querySelector(".filter_product");
  let url = "/product/filter/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ filter: allFilter.value }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      location.reload();
    });
};
// Activate the modal

// const myModal = document.getElementById("cartModal");
// const myInput = document.getElementById("myInput");

// myModal.addEventListener("shown.bs.modal", () => {
//   myInput.focus();
// });
