function fetchPalette(query) {
  fetch("/palette", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: new URLSearchParams({
      query: query
    })
  })
  .then((response => response.json()))
  .then(data => {
    const colors = data.result.colors;
    const names = data.result.names;
    const container = document.querySelector(".container");

    createColorBlocks(colors, names, container);
  })
  .catch(e => console.log(e));
}

function createColorBlocks(colors, names, container) {
  container.innerHTML = "";
    for (let i = 0; i < colors.length; i++) {
      const div = document.createElement("div");

      div.classList.add("color");
      div.style.backgroundColor = colors[i];
      div.style.width = `calc(100%/${colors.length})`;

      div.addEventListener("click", function() {
        navigator.clipboard.writeText(colors[i]);
      })

      const spanColor = document.createElement("span");
      spanColor.innerText = colors[i];
      div.appendChild(spanColor);

      const spanName = document.createElement("span");
      spanName.innerText = names[i];
      div.appendChild(spanName);

      container.appendChild(div);
    }
}

// initiate fetch random palette
fetchPalette("colorful colors palette");

const form  = document.querySelector("#form");
form.addEventListener("submit", function(e) {
  e.preventDefault();
  const query = form.elements.query.value;

  fetchPalette(query);
})