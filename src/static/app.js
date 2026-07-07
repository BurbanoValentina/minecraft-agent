const form = document.getElementById("builder-form");
const output = document.getElementById("result-output");
const title = document.getElementById("result-title");
const meta = document.getElementById("result-meta");
const copyButton = document.getElementById("copy-button");
const submitButton = form.querySelector("button[type='submit']");
const loading = document.getElementById("loading");
const requestInput = document.getElementById("user_request");
const tagButtons = document.querySelectorAll(".tag-btn");
const menuToggle = document.getElementById("menu-toggle");
const mainNav = document.getElementById("main-nav");

if (menuToggle && mainNav) {
  menuToggle.addEventListener("click", () => {
    const isOpen = mainNav.classList.toggle("is-open");
    menuToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });

  mainNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      mainNav.classList.remove("is-open");
      menuToggle.setAttribute("aria-expanded", "false");
    });
  });
}

tagButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const tag = button.dataset.tag;
    if (!tag) {
      return;
    }

    const text = requestInput.value.trim();
    requestInput.value = text ? `${text} [${tag}]` : `[${tag}]`;
    requestInput.focus();
  });
});

function renderPlan(plan) {
  title.textContent = plan.title || "Plano generado";
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

  if (!requestInput.value.trim()) {
    output.textContent = "Escribe una descripcion para poder generar un plano.";
    return;
  }

  output.textContent = "Generando diseño...";
  loading.style.display = "block";
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
    loading.style.display = "none";
  }
});

copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(output.textContent);
    copyButton.textContent = "Copiado";
    window.setTimeout(() => {
      copyButton.textContent = "Copiar";
    }, 1300);
  } catch {
    copyButton.textContent = "No se pudo copiar";
    window.setTimeout(() => {
      copyButton.textContent = "Copiar";
    }, 1300);
  }
});