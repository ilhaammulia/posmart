function openImage(src) {
  const img = $("#product-image");
  img.attr("src", src);
}

function updateProduct(element) {
  const productId = element.getAttribute("data-id");
  $.ajax({
    url: `http://localhost:5000/json/products?product_id=${productId}`,
    method: "GET",
  }).then((resp) => {
    $("#product-id").attr("value", resp.product_id);
    $("#product-name").attr("value", resp.name);
    $(`#product-category option[value=${resp.category}]`).attr(
      "selected",
      "selected"
    );
    $("#product-price").attr("value", resp.price);
    $("#product-stocks").attr("value", resp.stocks);
  });
}

function deleteProduct(element) {
  const productId = element.getAttribute("data-id");
  $("#product-id-delete").attr("value", productId);
}
