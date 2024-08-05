document.addEventListener("DOMContentLoaded", function () {
    const themeForm = document.getElementById("theme-form");
    const themeLink = document.getElementById("theme-link");

    const savedTheme = localStorage.getItem("selectedTheme");
    if (savedTheme) {
        themeLink.href = savedTheme;

        const radioButtons = themeForm.elements["theme"];
        for (let i = 0; i < radioButtons.length; i++) {
            if (radioButtons[i].value === savedTheme) {
                radioButtons[i].checked = true;
                break;
            }
        }
    }

    themeForm.addEventListener("change", function (event) {
        if (event.target.name === "theme") {
            const selectedTheme = event.target.value;
            themeLink.href = selectedTheme;

            localStorage.setItem("selectedTheme", selectedTheme);
        }
    });
});
