function initialize2() {

    //The center location of our map.
    var centerOfMap = new google.maps.LatLng(23.037506263879862, 72.52325094533654);

    //Map options.
    var options = {
      center: centerOfMap, //Set center.
      zoom: 7 //The zoom value.
    };

    //Create the map object.
    map = new google.maps.Map(document.getElementById('map2'), options);
}
google.maps.event.addDomListener(window, 'load', initialize2);
//     // Get element from which input should be taken
//     var input = document.getElementById('origin');
//     var input_2 = document.getElementById('destination');

//     // Initialize an object for the Google Maps Autocomplete API service (Since we have both origin and destination,
//     // we will create two objects, one for each)
//     autocomplete = new google.maps.places.Autocomplete(input, 
//     {
//         // This are the place parameters that google will use to return results.
//         // This can help to reduce API usage costs by reducing the number of results.
//       types: ['establishment'],
//       componentRestrictions: {'country':['IN']},
//       fields: ['place_id','geometry','name']
//     }); 
//     autocomplete_2 = new google.maps.places.Autocomplete(input_2, 
//     {
//       types: ['establishment'],
//       componentRestrictions: {'country':['IN']},
//       fields: ['place_id','geometry','name']
//     });

//     // This will call "onPlaceChanged" function when an option from the dropdown suggestions is selected.
//     // 'place_changed' is a value in google maps JavaScript API
//     autocomplete.addListener('place_changed', onOriginChanged);
//     autocomplete_2.addListener('place_changed', onDestinationChanged);
//   }

//   // This line is responsible for displaying dropdown suggestions to the input fields.
//   google.maps.event.addDomListener(window, 'load', initialize);

//   function onOriginChanged() {
//       // Using the object created in previous method, we will call "getPlace()" function (provided by google), to get 
//       // place details like geometry and place_id (Geometry means latitude and longitude).
//     var origin_place = autocomplete.getPlace();

//     //We are using JSON 'stringify' function to convert the returned object into string for passing as text using the html form.
//     origin_place_string = JSON.stringify(origin_place.geometry)
//     origin_place_id = JSON.stringify(origin_place.place_id)
//   //   origin_place_name = JSON.stringify(origin_place.name)

//     // We will check if the user has selected an input from the dropdown or has typed something himself without selecting anything from the dropdown.
//     // This can be checked if the location has a geometry.
//     if (!origin_place.geometry) {
//       document.getElementById('origin').placeholder = 'Enter a Place';

//     } else {

//       // Setting Origin values to the hidden fields in the form.
//       document.getElementById('origin_coordinates').value = origin_place_string;
//       document.getElementById('origin_place_id').value = origin_place_id
//       document.getElementById("origin_name").value = origin_place.name

//       // Submitting form that has id="send_geometry" using the JavaScript "submit()" method.
//       // document.getElementById('send_location_info').submit();

//       map = new google.maps.Map(document.getElementById('map2'), {
//               center: origin_place.geometry.location,
//               zoom: 14
//           })
//           marker = new google.maps.Marker({
//               position: origin_place.geometry.location, map, title:"Origin"
//           })
//           google.maps.event.addListener(map, 'click', function(event){
       
//           var clickedLocation = event.latLng; 
//           marker.setPosition(clickedLocation)
//           // document.getElementById('origin').value = clickedLocation
//           var latlng = {
//             lat: clickedLocation.lat(),
//             lng: clickedLocation.lng(),
//           }
//          var geocoder = new google.maps.Geocoder(); 
//          geocoder
//          .geocode({location: latlng})
//          .then((response) =>{
//            if(response.results[0]){
//              document.getElementById("origin").value = response.results[0].formatted_address
//            }
//            else{
//              window.alert("No results found");
//            }
//          })
//          .catch((e) => window.alert("Unable to find address due to: " + e));
        
        
//       })
      
//     }
//   }

//   function onDestinationChanged() {
//     var destination_place = autocomplete_2.getPlace();

//     destination_place_string = JSON.stringify(destination_place.geometry)
//     destination_place_id = JSON.stringify(destination_place.place_id)
//     // destination_place_name = JSON.stringify(destination_place.name)

//     if (!destination_place.geometry) {
//       document.getElementById('destination').placeholder = 'Enter a Place';
//   } else {
//       document.getElementById('destination_coordinates').value = destination_place_string;
//       document.getElementById('destination_place_id').value = destination_place_id
//       document.getElementById('destination_name').value = destination_place.name

//       map = new google.maps.Map(document.getElementById('map2'), {
//             center: destination_place.geometry.location,
//             zoom: 14
//           })
//           marker = new google.maps.Marker({
//               position: destination_place.geometry.location, map, title:"Destination"
//           })

//           google.maps.event.addListener(map, 'click', function(event){
       
//             var clickedLocation = event.latLng; 
//             marker.setPosition(clickedLocation)
//             // console.log(clickedLocation)
//             // document.getElementById('destination').value = clickedLocation
//             var latlng = {
//               lat: clickedLocation.lat(),
//               lng: clickedLocation.lng(),
//             }
//            var geocoder = new google.maps.Geocoder(); 
//            geocoder
//            .geocode({location: latlng})
//            .then((response) =>{
//              if(response.results[0]){
//                document.getElementById("destination").value = response.results[0].formatted_address
//              }
//              else{
//                window.alert("No results found");
//              }
//            })
//            .catch((e) => window.alert("Unable to find address due to: " + e));
           
//         })
//   }
// }