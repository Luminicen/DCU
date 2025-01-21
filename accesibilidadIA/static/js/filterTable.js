    function filterTable() {
        const startDate = document.getElementById("start_date").value;
        const endDate = document.getElementById("end_date").value;
    
        
        const start = startDate ? new Date(startDate) : null;
        const end = endDate ? new Date(endDate) : null;
    
        //tablita 
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
    
        //  tarjetas
        const cards = document.querySelectorAll(".analysis-cards .card");
        cards.forEach(card => {
            const cardDate = new Date(card.getAttribute("data-date"));
            if ((start && cardDate < start) || (end && cardDate > end)) {
                card.style.display = "none";
            } else {
                card.style.display = "";
            }
        });
    }
    