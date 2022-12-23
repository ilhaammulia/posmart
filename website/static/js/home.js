$(function () {
  getCatalog("drinks");
});

let currentCategory = "";
let cart = {};

function processCart(e) {
  const productId = e.parentElement.getAttribute("data-id");
  const productName = e.parentElement.getAttribute("data-name");
  let productStocks = parseInt(e.parentElement.getAttribute("data-stocks"));
  let producOriginStocks = parseInt(
    e.parentElement.getAttribute("data-origin-stocks")
  );
  const productPrice = parseInt(e.parentElement.getAttribute("data-price"));
  const action = e.getAttribute("data-action");

  let product = cart[productId];
  if (product) {
    newQty = eval(`${product.qty} ${action} 1`);
    if (newQty >= 0 && newQty <= producOriginStocks) {
      cart[productId].qty = newQty;
      cart[productId].price = eval(
        `${product.price} ${action} ${productPrice}`
      );
    }
  } else {
    newQty = eval(`0 ${action} 1`);
    if (newQty > 0 && newQty <= producOriginStocks) {
      cart[productId] = {
        name: productName,
        qty: 1,
        price: productPrice,
      };
    }
  }
  let currentStocks = eval(`${productStocks} ${action == "-" ? "+" : "-"} 1`);
  if (currentStocks >= 0 && currentStocks <= producOriginStocks) {
    controlCart(
      productId,
      productName,
      cart[productId].price,
      cart[productId].qty,
      currentStocks
    );
  }
}

function controlCart(itemId, itemName, itemPrice, itemStocks, currentStocks) {
  let itemContainer = $("#items");
  let itemListContainer = $(`#product-cart-${itemId}`);

  if (itemListContainer.length) {
    if (itemStocks > 0) {
      $(`#product-${itemId}-name`).html(itemName);
      $(`#product-${itemId}-qty`).html(itemStocks);
      $(`#product-${itemId}-price`).html(itemPrice);
    } else {
      itemListContainer.remove();
    }
  } else {
    let card = "";
    card += `<div id="product-cart-${itemId}">`;
    card += `<div class="card w-96 bg-base-100 shadow-xl">`;
    card += `<div class="card-body">`;
    card += `<div class="flex justify-between">`;
    card += `<h2 id="product-${itemId}-name" class="card-title">${itemName}</h2>`;
    card += `<h3 id="product-${itemId}-qty" class="card-title">${itemStocks}</h3>`;
    card += `<h2 id="product-${itemId}-price" class="card-title order-last">${itemPrice}</h2></div></div></div><br /></div>`;
    itemContainer.append(card);
  }

  $(`#product-stocks-${itemId}`).html(currentStocks);
  $(`#product-qty-${itemId}`).html(itemStocks);
  $(`#product-item-${itemId}`).attr("data-stocks", currentStocks);

  controlPayment();
}

function controlPayment() {
  let subtotal = 0;
  for (item in cart) {
    let prod = cart[item];
    subtotal += prod.price;
  }
  const tax = (subtotal * 3) / 100;
  const totalPay = subtotal + tax;

  const subtotalForm = $("#subtotal");
  const taxForm = $("#tax-total");
  const payForm = $("#pay-total");

  subtotalForm.html(`Rp. ${subtotal}`);
  subtotalForm.attr("data-subtotal", subtotal);

  taxForm.html(`Rp. ${tax}`);
  taxForm.attr("data-tax", tax);

  payForm.html(`Rp. ${totalPay}`);
  payForm.attr("data-total-pay", totalPay);
}

function processCheckout() {
  let totalPay = parseInt($("#pay-total").attr("data-total-pay"));
  let totalMoney = parseInt($("#pay-total").attr("data-money"));
  let totalChange = totalMoney - totalPay;
  let paymentMethod = $("#payment-method").attr("data-method");

  $("#total-bill").val(totalPay);
  $("#table-total-bill").html(`Rp. ${totalPay}`);

  $("#total-paid-bill").val(totalMoney);
  $("#table-total-paid").html(`Rp. ${totalMoney}`);

  $("#total-change").val(totalChange);
  $("#table-total-change").html(`Rp. ${totalChange}`);

  $("#pay-with").val(paymentMethod);

  let date = new Date();
  $("#current-date").html(
    `${date.getDate()}-${date.getMonth()}-${date.getFullYear()}`
  );

  let hiddenInput = $("#hidden-input");
  let tableReceipt = $("#table-receipt tbody");
  tableReceipt.empty();
  let row = "";

  let no = 1;
  for (item in cart) {
    let prod = cart[item];

    hiddenInput.append(
      `<input type="hidden" name="productIds[]" value="${item}" />`
    );

    hiddenInput.append(
      `<input type="hidden" name="productQtys[]" value="${prod.qty}" />`
    );
    hiddenInput.append(
      `<input type="hidden" name="productPrices[]" value="${prod.price}" />`
    );

    row += "<tr>";
    row += `<td>${no}</td>`;
    row += `<td>${prod.name}</td>`;
    row += `<td>${prod.qty}</td>`;
    row += `<td>${prod.price}</td>`;
    row += "</tr>";
    no += 1;
  }

  tableReceipt.html(row);

  $("#invoice-modal").addClass("modal-open");
}

const searchProduct = document.getElementById("search-product");
searchProduct.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    getCatalog(currentCategory, searchProduct.value);
  }
});

function getCatalog(category, filterSearch = "") {
  const productList = $("#product-list");
  productList.empty();
  currentCategory = category;
  $.ajax({
    url: `http://localhost:5000/json/products?category=${category}`,
    method: "GET",
  }).then((resp) => {
    resp.map((item) => {
      if (String(item.name).toLowerCase().includes(filterSearch)) {
        let product = cart[item.product_id];
        let qty = product?.qty ?? 0;
        let stocks = item.stocks - qty;

        let card = "";
        card += `<div class="card card-compact w-60 product-bg indicator">`;
        card += `<span class="indicator-item indicator-center badge badge-primary font-bold">Rp.${item.price}</span>`;
        card += `<figure class="px-5 pt-5"><img src="/static/img/products/${item.img}" alt="${item.name}" class="rounded-xl" /></figure>`;
        card += '<div class="card-body">';
        card += `<h2 class="card-title text-theme">${item.name} <div id="product-stocks-${item.product_id}" class="badge badge-primary text-sm">${stocks}</div></h2>`;
        card += `<div id="product-item-${item.product_id}" class="card-actions justify-end" data-id="${item.product_id}" data-name="${item.name}" data-origin-stocks="${item.stocks}" data-stocks="${stocks}" data-price="${item.price}">`;
        card += `<button class="btn btn-primary btn-sm" data-action="-" onclick="processCart(this)">-</button>`;
        card += `<span id="product-qty-${item.product_id}" class="btn btn-sm btn-ghost">${qty}</span>`;
        card += `<button class="btn btn-primary btn-sm" data-action="+" onclick="processCart(this)">+</button></div></div></div>`;
        productList.append(card);
      }
    });
  });
}

function choosePaymentMethod(e, method) {
  let paymentMethod = $("#payment-method");
  if (e.classList.contains("payment-btn")) {
    e.classList.remove("payment-btn");
    e.classList.add("btn-outline");
  } else {
    e.classList.remove("btn-outline");
    e.classList.add("payment-btn");
    paymentMethod.attr("data-method", method);
  }
}

const checkMoney = document.getElementById("total-paid");
checkMoney.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    let payment = $("#pay-total");
    let totalPay = parseInt(payment.attr("data-total-pay"));
    let money = parseInt(checkMoney.value);
    if (money < totalPay) {
      checkMoney.classList.remove("input-success");
      checkMoney.classList.add("input-secondary");
      $("#pay-button").prop("disabled", true);
    } else {
      checkMoney.classList.remove("input-secondary");
      checkMoney.classList.add("input-success");
      payment.attr("data-paid", "true");
      $("#pay-button").prop("disabled", false);
      payment.attr("data-money", money);
    }
  }
});
