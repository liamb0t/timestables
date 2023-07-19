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
let marker;
let geocoder;
let latLng;

function geocode(latLng) {
  geocoder.geocode({ 'latLng': latLng }, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      if (results[0]) {
        // Retrieve the formatted address and other components
        document.querySelector('#address').value = results[0].formatted_address;
        // You can extract specific details like city, country, street name, etc. from addressComponents array
      } else {
        console.log('No results found');
      }
    } else {
      console.log('Geocoder failed due to: ' + status);
    }
  });
}

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");
  const myLatLng = { lat: 37.532600, lng: 127.024612 }
  map = new Map(document.getElementById("map"), {
    center: myLatLng,
    zoom: 10,
  });

  marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    draggable: true
  });

  geocoder = new google.maps.Geocoder();
  
  map.addListener('click', function(event) {
    if (marker) {
      marker.setMap(null);
    }

    marker = new google.maps.Marker({
      position: event.latLng,
      map: map,
      draggable: true
    });

    geocode(event.latLng)

    document.querySelector('#lat').value = event.latLng.lat();
    document.querySelector('#lng').value = event.latLng.lng();
    
  })
}

initMap();

