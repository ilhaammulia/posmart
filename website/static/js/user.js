function updateUser(e) {
  const userId = e.getAttribute("data-id");
  $.ajax({
    url: `http://localhost:5000/json/users?user_id=${userId}`,
    method: "GET",
  }).then((resp) => {
    $("#user-id").attr("value", userId);
    $("#update-name").attr("value", resp.name);
    $("#user-name").attr("value", resp.username);
    $(`#update-role option[value=${resp.role}]`).attr("selected", "selected");
  });
}

function deleteUser(e) {
  const userId = e.getAttribute("data-id");
  $("#user-id-delete").attr("value", userId);
}
