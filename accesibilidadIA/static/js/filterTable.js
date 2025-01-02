
function filterTable() {
    const startDate = document.getElementById("start_date").value;
    const endDate = document.getElementById("end_date").value;

    // Convert dates to comparable formats
    const start = startDate ? new Date(startDate) : null;
    const end = endDate ? new Date(endDate) : null;

    const rows = document.querySelectorAll("#analysisTable tbody tr");

    rows.forEach(row => {
        const dateCell = row.querySelector("td[data-date]");
        const rowDate = new Date(dateCell.getAttribute("data-date"));

        if ((start && rowDate < start) || (end && rowDate > end)) {
            row.style.display = "none";
        } else {
            row.style.display = "";
        }
    });
}