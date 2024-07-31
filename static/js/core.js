const date = new Date();
const body = document.getElementById("body-id");
const modalBox = document.querySelector(".modalbox");
document.querySelector(".year-span").textContent = date.getFullYear();

// modal
function closeModal() {
  modalBox.style.display = "none";
  body.style.overflow = "auto";
}

// remove alert btn
function removeAlert() {
  const btn = document.querySelector(".message-alert");
  btn.classList.add("d-none")
}

// toggle sidebar
function toggle_sidebar() {
  const body = document.getElementById('body-id')
  const sidebar = document.querySelector('.navbar_ul')
  if (sidebar) {
    sidebar.classList.toggle("show-sidebar")
    body.classList.toggle("body-overflow-hidden")
  }
}

// scrolltop
function showScroll() {
  const scrollTop = document.getElementById("scroll-top");
  if (this.scrollY >= 500) {
    scrollTop.classList.add("show-scroll");
  } else {
    scrollTop.classList.remove("show-scroll");
  }
}

function scrollToTop() {
  window.scroll({top:0,left:0,behavior:'smooth'});
}

window.addEventListener("scroll", showScroll);