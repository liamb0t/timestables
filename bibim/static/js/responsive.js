function addPropertyToClass() {
    const wrapper = document.querySelector('.wrapper');

   
    wrapper.style.marginLeft = 'calc(var(--sidebar-width) + 1.25rem)';
   
}

// Call the function when the page loads
window.addEventListener('load', addPropertyToClass);
