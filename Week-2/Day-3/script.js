const items = document.querySelectorAll(".item");

items.forEach(item => {
  const button = item.querySelector(".title");
  const icon = item.querySelector(".icon");

  button.addEventListener("click", () => {
    const isOpen = item.classList.contains("active");

    // Close all items first
    items.forEach(i => {
      i.classList.remove("active");
      i.querySelector(".icon").textContent = "+";
    });

    // If it was closed before, open it
    if (!isOpen) {
      item.classList.add("active");
      icon.textContent = "−";
    }
  });
});
