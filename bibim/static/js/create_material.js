document.addEventListener('DOMContentLoaded', function() {
    const gradeSelect = document.querySelector('#grade');
    const publisherSelect = document.querySelector('#publisher');
    const lessonSelect = document.querySelector('#lesson');
    const selectButtons = [gradeSelect, publisherSelect];

    const level = document.querySelector('#level').value;

    selectButtons.forEach(btn => {
        btn.addEventListener('change', function() {
            const publisher = publisherSelect.value;
            const grade = gradeSelect.value;
            fetch(`/get_lessons/${level}/${grade}/${publisher}`)
                .then(response => response.json())
                .then(data => { 
                    lessonSelect.innerHTML = '';
                    data['lesson_choices'].forEach(option => {
                        const optionElem = document.createElement('option');
                        optionElem.value = option[0];
                        optionElem.text = option[1];
                        lessonSelect.appendChild(optionElem);
                    });
                })
            .catch(error => console.error(error));
        });
    });
});