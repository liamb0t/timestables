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


