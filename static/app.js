const container = document.querySelector(".container");
const form  = document.querySelector("#form");
const generateBtn  = document.querySelector("#generate-btn");
const generatingBtn  = document.querySelector("#generating-btn");
const errorText = document.querySelector(".error-text");

const successToast = document.getElementById('successToast')
const errorToast = document.getElementById('errorToast')
const successToastBootstrap = bootstrap.Toast.getOrCreateInstance(successToast)
const errorToastBootstrap = bootstrap.Toast.getOrCreateInstance(errorToast)

function isMobile() {
  if (!window) {
    return;
  }
  return window.innerWidth <= 768;
}

function fetchPalette(query) {
  generateBtn.classList.toggle("hidden");
  generatingBtn.classList.toggle("hidden");
  fetch("/palette", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: new URLSearchParams({
      query
    })
  })
  .then((response => response.json()))
  .then(data => {
    const colors = data.result;

    createColorBlocks(colors, container);
  })
  .catch(() => {
    errorToastBootstrap.show();
    errorText.innerText = "Something went wrong, try generate again";
    generateBtn.classList.toggle("hidden");
    generatingBtn.classList.toggle("hidden");
  });
}

function createColorBlocks(colors, container) {
  container.innerHTML = "";
  for (const color of colors) {
    const div = document.createElement("div");

    div.classList.add("color");
    div.style.backgroundColor = color.code;

    if (isMobile()) {
      div.style.height = `calc(100%/${colors.length})`;
    } else {
      div.style.width = `calc(100%/${colors.length})`;
    }

    div.addEventListener("click", function() {
      navigator.clipboard.writeText(color.code);
    })

    const spanColor = document.createElement("span");
    spanColor.innerText = color.code;
    div.appendChild(spanColor);

    const spanName = document.createElement("span");
    spanName.innerText = color.name;
    div.appendChild(spanName);

    container.appendChild(div);
  }
  successToastBootstrap.show();
  generateBtn.classList.toggle("hidden");
  generatingBtn.classList.toggle("hidden");
}

if (window) {
  // Initially hide the generating button
  generatingBtn.classList.add("hidden");

  // initiate fetch random palette
  fetchPalette("random colorful colors");
}

form.addEventListener("submit", function(e) {
  e.preventDefault();
  errorText.innerText = ""
  const query = form.elements.query.value;

  fetchPalette(query);
});