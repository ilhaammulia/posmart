function controlDrawer() {
  const drawer = document.getElementById("my-drawer");
  if (drawer.checked == true) {
    drawer.checked = false;
  } else {
    drawer.checked = true;
  }
}
