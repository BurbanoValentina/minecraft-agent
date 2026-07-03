const form = document.getElementById("builder-form");
const output = document.getElementById("result-output");
const title = document.getElementById("result-title");
const meta = document.getElementById("result-meta");
const copyButton = document.getElementById("copy-button");
const submitButton = form.querySelector("button[type='submit']");

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
  submitButton.disabled = true;
  submitButton.textContent = "Generando...";

  try {
    const response = await fetch("/api/build", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || "No se pudo generar el plan.");
    }

    const plan = await response.json();
    renderPlan(plan);
  } catch (error) {
    output.textContent = `No se pudo generar el plano. ${error.message || "Intenta otra vez."}`;
    meta.innerHTML = "";
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Generar plano de bloques";
  }
});

copyButton.addEventListener("click", async () => {
  await navigator.clipboard.writeText(output.textContent);
  copyButton.textContent = "Copiado";
  window.setTimeout(() => {
    copyButton.textContent = "Copiar";
  }, 1300);
});