
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("add-filter-btn").addEventListener("click", function () {
        const filterName = document.getElementById("custom-filter").value.trim();
        if (filterName) {
            const container = document.getElementById("usability-errors");

            // Verificar si ya existe un filtro con el mismo nombre
            if (Array.from(container.querySelectorAll("input")).some(input => input.value === filterName)) {
                alert("Este filtro ya ha sido agregado.");
                return;
            }

            const div = document.createElement("div");
            div.classList.add("checkbox-group");

            // Crear el checkbox
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.id = `custom-${filterName}`;
            checkbox.name = "usability-errors";
            checkbox.value = filterName;

            // Crear la etiqueta asociada
            const label = document.createElement("label");
            label.htmlFor = checkbox.id;
            label.textContent = filterName;

            // Agregar el checkbox y la etiqueta al contenedor
            div.appendChild(checkbox);
            div.appendChild(label);

            // Agregar el nuevo contenedor al contenedor de filtros
            container.appendChild(div);

            // Limpiar el campo de entrada
            document.getElementById("custom-filter").value = "";
        } else {
            alert("Por favor, ingrese un nombre para el filtro.");
        }
    });
});
