const form = document.getElementById("builder-form");
const output = document.getElementById("result-output");
const title = document.getElementById("result-title");
const meta = document.getElementById("result-meta");
const copyButton = document.getElementById("copy-button");

function renderPlan(plan) {
  title.textContent = plan.title;
  output.textContent = `${plan.summary}\n\nPlano ASCII:\n${plan.ascii_plan}`;
  meta.innerHTML = "";

  [
    `Tamaño ${plan.size}`,
    `${plan.floors} pisos`,
    `${plan.rooms.length} habitaciones`,
    `${plan.materials.length} materiales`,
  ].forEach((value) => {
    const chip = document.createElement("span");
    chip.textContent = value;
    meta.appendChild(chip);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  output.textContent = "Generando diseño...";

  const response = await fetch("/api/build", {
    method: "POST",
    body: formData,
  });

  const plan = await response.json();
  renderPlan(plan);
});

copyButton.addEventListener("click", async () => {
  await navigator.clipboard.writeText(output.textContent);
  copyButton.textContent = "Copiado";
  window.setTimeout(() => {
    copyButton.textContent = "Copiar";
  }, 1300);
});