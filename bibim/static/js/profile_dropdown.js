// Get the dropdown and the profile picture
const dropdown = document.querySelector('.profile-dropdown');
const profilePic = document.querySelector('.profile-pic');

// Add a click event listener to the profile picture
// Add a click event listener to the profile picture
profilePic.addEventListener('click', function(event) {
    event.stopPropagation();
    
    // If the dropdown is already visible, hide it
    if (dropdown.style.display === 'block') {
        dropdown.style.display = 'none';
        return;
    }
    // Show the dropdown
    dropdown.style.display = 'block';
});


// Add a click event listener to the document
document.addEventListener('click', function() {
    // If the dropdown is visible, hide it
    if (dropdown.style.display === 'block') {
        dropdown.style.display = 'none';
    }
});
