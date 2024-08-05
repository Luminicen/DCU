document.addEventListener("DOMContentLoaded", function() {
    const scrollContainer = document.getElementById("scroll-content-container");
    const pages = document.querySelectorAll(".page");
    const indicators = document.querySelectorAll(".dot");
    const prevBtn = document.getElementById("prevBtn");
    const prevLbl = document.getElementById("prevLbl");
    const nextBtn = document.getElementById("nextBtn");
    const nextLbl = document.getElementById("nextLbl");
    let currentIndex = 0;

    function updateIndicators(index) {
        indicators.forEach((dot, i) => {
            dot.classList.toggle("active", i === index);
        });
    }

    function scrollToPage(index) {
        const offset = index * window.innerWidth;
        scrollContainer.scrollTo({
            left: offset,
            behavior: "smooth"  
        });
        updateIndicators(index);
        updateButtons(index);
    }

    function updateButtons(index) {
        prevBtn.classList.toggle("hidden", index === 0);
        prevLbl.classList.toggle("hidden", index === 0);
        nextBtn.classList.toggle("hidden", index === pages.length - 1);
        nextLbl.classList.toggle("hidden", index === pages.length - 1);
    }

    prevBtn.addEventListener("click", function() {
        if (currentIndex > 0) {
            currentIndex--;
            scrollToPage(currentIndex);
        }
    });

    nextBtn.addEventListener("click", function() {
        if (currentIndex < pages.length - 1) {
            currentIndex++;
            scrollToPage(currentIndex);
        }
    });

    indicators.forEach((dot, index) => {
        dot.addEventListener("click", function() {
            currentIndex = index;
            scrollToPage(currentIndex);
        });
    });

    const uploadSection = document.querySelector(".upload-file");
    const uploadSectionIndex = Array.from(pages).indexOf(uploadSection);

    if (uploadSectionIndex !== -1) {
        currentIndex = uploadSectionIndex;
        scrollToPage(currentIndex);
    }

    updateIndicators(currentIndex);
    updateButtons(currentIndex);
});