const toggleBtn = document.querySelector('.toggle-btn');
const endDateContainer = document.querySelector('.end-date-container');

toggleBtn.addEventListener('click', function() {
    if (endDateContainer.style.display == 'none') {
        endDateContainer.style.display = 'flex';
        this.innerHTML = '- End date and time'
    }
    else  {
        endDateContainer.style.display = 'none';
        this.innerHTML = '+ End date and time'
    }
})

let map;

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 8,
  });
}

initMap();