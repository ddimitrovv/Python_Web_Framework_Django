document.addEventListener("DOMContentLoaded", function() {
    const mainNav = document.querySelector(".main-nav");
    const secondaryNav = document.querySelector(".secondary-nav");

    const menuButton = document.querySelector(".menu-button");
    menuButton.addEventListener("click", function() {
        secondaryNav.classList.toggle("show-dropdown"); // Toggle the class to show/hide the dropdown
    });

    // Update the visibility of the secondary navigation based on screen width
    function updateSecondaryNavVisibility() {
        if (window.innerWidth < 500) {
            secondaryNav.classList.remove("hidden");
            mainNav.classList.add('hidden')
        } else {
            secondaryNav.classList.add("hidden");
            mainNav.classList.remove('hidden')
        }
    }

    updateSecondaryNavVisibility(); // Initial check

    // Listen for window resize events
    window.addEventListener("resize", updateSecondaryNavVisibility);
});

function toggleDropdown() {
    const dropdownContent = document.getElementById("dropdownContent");
    dropdownContent.classList.toggle("show-dropdown");
}

// Close the dropdown menu if the user clicks outside of it
window.addEventListener("click", function(event) {
    const secondaryNav = document.querySelector('.secondary-nav');
    // Hide dropdown when clicked outside
    if (!event.target.matches('.menu-button') && !event.target.closest('.dropdown-content')) {
        secondaryNav.classList.remove('show-dropdown')
    }
});

