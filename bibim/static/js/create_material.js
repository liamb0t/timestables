document.addEventListener('DOMContentLoaded', function() {
    const gradeSelect = document.querySelector('#grade');
    const publisherSelect = document.querySelector('#publisher');
    const lessonSelect = document.querySelector('#lesson');
    const selectButtons = [gradeSelect, publisherSelect];

    const level = document.querySelector('#level').value;

    selectButtons.forEach(btn => {
        btn.addEventListener('change', function() {
            fetch(`/get_lessons/${level}/${gradeSelect.value}/${publisherSelect.value}`)  
            .then(response => response.json())
            .then(data => {
                lessonSelect.innerHTML = ''
                lessonSelect.style.display = 'flex'
                data['lesson_choices'].forEach(choice => {
                let option = document.createElement('option');
                let text = choice[1];
                if (text.length > 20) {
                    text = text.substring(0, 15) + '...'
                }
                option.value = choice[0];
                option.text = text
                lessonSelect.appendChild(option);
                });
            })
            .catch(error => console.error(error));
        });
    });
});

let fileInput = document.querySelector('#files');
let fileInputLabel = document.querySelector('.file-upload-label');

fileInput.addEventListener('change', function() {
    let files = fileInput.files;
    if (files.length === 1) {
        fileInputLabel.textContent = files[0].name;
    } else {
        fileInputLabel.textContent = `${files.length} files selected`;
    }
});

const params = new URLSearchParams(window.location.search);
const type = params.get('type');


// If 'type' parameter exists, set the dropdown value
if(type) {
  const dropdown = document.getElementById("grade");
  dropdown.value = type;
}


