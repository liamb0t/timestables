// script.js

document.addEventListener("DOMContentLoaded", function() {
    const navbarLinks = document.querySelectorAll('.search-nav a');
    const submit = document.querySelector('.search-bar form');
    // Check if referrer is from the same origin
    let referrer = document.referrer;
    
    if (!referrer.includes(window.location.origin+'/search')) {
        localStorage.removeItem('activePage'); 
    }

    // Check local storage for active link
    let activePage = localStorage.getItem('activePage');
    if (activePage) {
        navbarLinks.forEach(link => {
            if (link.getAttribute('href') === activePage) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    } else {
        // Set the first link as active by default
        navbarLinks[0].classList.add('active');
    }

    navbarLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            localStorage.setItem('activePage', this.getAttribute('href'));
        });
    });
    submit.addEventListener('submit', function() {
        const urlParams = new URLSearchParams(window.location.search);
        const type = urlParams.get('type')
        if (type) {
            const queryInput = document.getElementById('main-search');
            localStorage.setItem('activePage',`/search?q=${queryInput.value}&type=${type}`);
        }
    })
});
