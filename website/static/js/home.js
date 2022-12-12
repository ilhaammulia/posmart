function choosePaymentMethod(e) {
  if (e.classList.contains("payment-btn")) {
    e.classList.remove("payment-btn");
    e.classList.add("btn-outline");
  } else {
    e.classList.remove("btn-outline");
    e.classList.add("payment-btn");
  }
}
