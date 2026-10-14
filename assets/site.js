document.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-copy]");
  if (!button || button.dataset.copying === "true") return;
  const value = button.getAttribute("data-copy");
  const original = button.textContent;
  button.dataset.copying = "true";
  button.setAttribute("aria-live", "polite");
  let copied = false;

  try {
    await navigator.clipboard.writeText(value);
    copied = true;
  } catch (_error) {
    const input = document.createElement("textarea");
    input.value = value;
    input.setAttribute("readonly", "");
    input.style.position = "fixed";
    input.style.opacity = "0";
    document.body.appendChild(input);
    input.select();
    try {
      copied = document.execCommand("copy");
    } catch (_fallbackError) {
      copied = false;
    }
    input.remove();
    button.focus({ preventScroll: true });
  }

  button.textContent = copied ? "Copied" : "Copy failed";
  window.setTimeout(() => {
    button.textContent = original;
    delete button.dataset.copying;
  }, 1800);
});
