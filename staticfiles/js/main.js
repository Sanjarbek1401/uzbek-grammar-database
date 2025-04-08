// Custom JavaScript for Uzbek Grammar Website

document.addEventListener('DOMContentLoaded', function() {
    // Activate tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add active class to current navigation link
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentLocation === linkPath) {
            link.classList.add('active');
        }
    });

    // Add highlight to search terms in results
    const highlightSearchTerms = () => {
        const urlParams = new URLSearchParams(window.location.search);
        const searchQuery = urlParams.get('q');

        if (searchQuery && searchQuery.length > 0) {
            const searchResults = document.querySelectorAll('.table tbody td:not(:last-child)');

            searchResults.forEach(cell => {
                const text = cell.innerHTML;
                const regex = new RegExp('(' + searchQuery + ')', 'gi');
                cell.innerHTML = text.replace(regex, '<mark>$1</mark>');
            });
        }
    };

    // Call highlight function if we're on the search results page
    if (currentLocation.includes('/search/')) {
        highlightSearchTerms();
    }
});