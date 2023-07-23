const buttons = document.querySelectorAll('.user-filters a');

buttons.forEach((link) => {
  link.classList.remove('active')
  link.addEventListener('click', (event) => {
    // Store the active link information in localStorage
    localStorage.setItem('activeLinkUserProfile', link.getAttribute('href'));
  });
});

// Check if there is an active link in localStorage
const activeBtn = localStorage.getItem('activeLinkUserProfile');
if (activeBtn) {
 
  const link = document.querySelector(`.user-filters a[href="${activeBtn}"]`);
  if (link) {
    link.classList.add('active');
  }
}