let dark = localStorage.getItem("darkMode");
var element = document.getElementById("light");

if (dark == "true") {
  element.setAttribute("href", "/css/main.dark.css");
}
else {
  element.setAttribute("href", "/css/main.css");
}
// I have tried sevral times to make it work with the event listeners but it just wont
// so I am taking the L on this and using the buttons onclick attribute
function toggle_style() {
  if (element.getAttribute("href") == "/css/main.css") {
    element.setAttribute("href", "/css/main.dark.css");
    localStorage.setItem("darkMode", "true");
  }
  else {
    element.setAttribute("href", "/css/main.css");
    localStorage.setItem("darkMode", "false");

  }
  element.classList.toggle("dark-mode");
}


function submitSale() {
  const msg = document.getElementById("message-field").value;
  const saleBanner = document.getElementById("sale-banner")
  const m = { message: msg };
  fetch("/api/sale", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(m)
  }).then(response => response.json())
    .then(data => {
      saleBanner.innerText = data.message;
      saleBanner.style.display = 'block';
    })
  //TODO: FIX! doesnt work :(
}
function endSale() {
  const saleBanner = document.getElementById('sale-banner');
  fetch('/api/sale', {
    method: 'DELETE',
  })
    .then(() => {
      // Hide the sale banner
      saleBanner.style.display = 'none';
    })

}