const customSelectBtn = document.getElementById('custom-select');
const options = document.getElementById("selectOptions");

customSelectBtn.addEventListener('click', toggleOptions)

const lessonFilter = document.querySelector('#lesson')
const textBookFilter = document.querySelector('#publisher')


document.addEventListener('DOMContentLoaded', function() {
  const publisher = textBookFilter.value;
  if (publisher != 'Textbook' && publisher != 'All' ) {
    lessonFilter.style.display = 'inline'
  }
})
  

function toggleOptions() {
  const rect = this.getBoundingClientRect();
  options.style.left = (document.documentElement.clientWidth - rect.left + 45) + 'px';
  
  if (options.style.display === "none" || options.style.display === "") {
    options.style.display = "block";
    document.addEventListener("click", handleOutsideClick);
  } else {
    options.style.display = "none";
    document.addEventListener("click", handleOutsideClick);
  }
}

function handleOutsideClick(event) {
    
    if (!options.contains(event.target) && !customSelectBtn.contains(event.target)) {
        options.style.display = "none";
        document.removeEventListener("click", handleOutsideClick);
    }
}

document.querySelectorAll('.filter-select').forEach(select => {
  select.onchange = function() {
    document.querySelector('#filter-submit').submit()
  }
});

document.querySelectorAll('.adv-filter').forEach(select => {
  select.onclick = function() {
    const currentURL = window.location.href;
    const baseUrl = currentURL.split('?')[0];
    let newURL;

    // Check if the URL already has query parameters
   
    newURL = baseUrl + `?f=${this.dataset.para}`
   
    history.pushState(null, '', newURL);
    document.querySelector('#filter-submit').submit()
  }
});