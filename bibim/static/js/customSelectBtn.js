const customSelectBtn = document.getElementById('custom-select');
const options = document.getElementById("selectOptions");
const filters = document.querySelector('.materials-filters')
customSelectBtn.addEventListener('click', toggleOptions)

const lessonFilter = document.querySelector('#lesson')
const textBookFilter = document.querySelector('#publisher')

const gradeFilter = document.querySelector('#grade')


document.addEventListener('DOMContentLoaded', function() {
  const publisher = textBookFilter.value;
  if (publisher != 'Textbook' && publisher != 'All' ) {
    lessonFilter.style.display = 'inline'
  }
})
  

function toggleOptions() {
  const rect = this.getBoundingClientRect();
  options.style.right = (document.documentElement.clientWidth - rect.right + 20) + 'px';
  
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


textBookFilter.onchange = function() {
  fetch(`/get_lessons/${filters.dataset.level}/${gradeFilter.value}/${textBookFilter.value}`)  
    .then(response => response.json())
    .then(data => {
      lessonFilter.innerHTML = ''
      data['lesson_choices'].forEach(choice => {
        let option = document.createElement('option');
        let text = choice[1];
        if (text.length > 20) {
          text = text.substring(0, 15) + '...'
        }
        option.value = choice[0];
        option.text = text
        lessonFilter.appendChild(option);
      });
    })
}