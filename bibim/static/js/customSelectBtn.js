const customSelectBtn = document.getElementById('custom-select');
const options = document.getElementById("selectOptions");
const filters = document.querySelector('.materials-filters')
customSelectBtn.addEventListener('click', toggleOptions)

const lessonFilter = document.querySelector('#lesson')
const textBookFilter = document.querySelector('#publisher')

const gradeFilter = document.querySelector('#grade')
const lesson = localStorage.getItem('lesson')

document.addEventListener('DOMContentLoaded', function() {
  const publisher = textBookFilter.value;
  if (publisher != 'Textbook' && publisher != 'All' ) {
    lessonFilter.style.display = 'inline'
  }
})

function toggleOptions() {
  const rect = this.getBoundingClientRect();
  options.style.left = rect.left + 'px';
  options.style.top = rect.bottom + 5 + 'px';
  
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
    if (select.id == 'lesson') {
      localStorage.setItem('lesson', select.value)
    }
    document.querySelector('#filter-submit').submit()
  }
});

window.onload = function() {
  fetch(`/get_lessons/${filters.dataset.level}/${gradeFilter.value}/${textBookFilter.value}`)  
    .then(response => response.json())
    .then(data => {
    if (data['lesson_choices']) {
      for (let i = lessonFilter.options.length - 1; i >= 2; i--) {
        lessonFilter.remove(i);
      }
      data['lesson_choices'].forEach(choice => {
        let option = document.createElement('option');
        let text = choice[1];
        if (text.length > 20) {
          text = text.substring(0, 15) + '...'
        }
        option.value = choice[0];
        option.text = text
        lessonFilter.appendChild(option);
        if (lesson == option.value) {
          lessonFilter.value = lesson
        }
      });
    }
  })
}

