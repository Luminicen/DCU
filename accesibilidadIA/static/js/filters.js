
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("add-filter-btn").addEventListener("click", function () {
        const filterName = document.getElementById("custom-filter").value.trim();
        if (filterName) {
            const container = document.getElementById("usability-errors");

            if (Array.from(container.querySelectorAll("input")).some(input => input.value === filterName)) {
                alert("Este filtro ya ha sido agregado.");
                return;
            }

            const div = document.createElement("div");
            div.classList.add("checkbox-group");

            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.id = `custom-${filterName}`;
            checkbox.name = "usability-errors";
            checkbox.value = filterName;

            const label = document.createElement("label");
            label.htmlFor = checkbox.id;
            label.textContent = filterName;

            div.appendChild(checkbox);
            div.appendChild(label);

            container.appendChild(div);

            document.getElementById("custom-filter").value = "";
        } else {
            alert("Por favor, ingrese un nombre para el filtro.");
        }
    });
});
