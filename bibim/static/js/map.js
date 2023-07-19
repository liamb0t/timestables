let map;
let marker;
let myLat = parseFloat(document.querySelector('#map').dataset.lat);
let myLng = parseFloat(document.querySelector('#map').dataset.lng);
let geocoder;
let latLng;

async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    const myLatLng = { lat: myLat, lng: myLng }
    map = new Map(document.getElementById("map"), {
      center: myLatLng,
      zoom: 18,
    });
  
    marker = new google.maps.Marker({
      position: myLatLng,
      map: map,
      title: 'BIBIM SURF', // Set the title as the location name
      label: {
        text: 'BIBIM SURF',
        color: 'black',
        fontWeight: 'bold',
        fontSize: '14px',
        fontFamily: 'Arial, sans-serif',
        backgroundColor: 'white',
        padding: '5px',
        textShadow: '2px 2px 4px rgba(0, 0, 0, 0.5)',
        textAlign: 'center'
      }
    });

    geocoder = new google.maps.Geocoder();
    latLng = new google.maps.LatLng(myLat, myLng);
    geocode()
  }
  
document.addEventListener('DOMContentLoaded', function() {
  initMap()
})

function geocode() {
  geocoder.geocode({ 'latLng': latLng }, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      if (results[0]) {
        // Retrieve the formatted address and other components
        var formattedAddress = results[0].formatted_address;
        var addressComponents = results[0].address_components;
        // You can extract specific details like city, country, street name, etc. from addressComponents array
        console.log('Formatted Address: ' + formattedAddress);
        console.log('Address Components: ', addressComponents);
      } else {
        console.log('No results found');
      }
    } else {
      console.log('Geocoder failed due to: ' + status);
    }
  });
}





