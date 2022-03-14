function initialize(){

    //The center location of our map.
    var centerOfMap = new google.maps.LatLng(23.037506263879862, 72.52325094533654);

    var options = {
        center: centerOfMap,
        zoom: 10,
        mapTypeControl: true,
        mapTypeControlOptions: {
        style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
        position: google.maps.ControlPosition.TOP_CENTER,
        }
    };

    //Create the map object.
    const map = new google.maps.Map(document.getElementById('map'), options);

    const trafficlayer = new google.maps.TrafficLayer();

    trafficlayer.setMap(map);

    // Get element from which input should be taken
    var input = document.getElementById('origin');
    var input2 = document.getElementById('destination');

    // Initialize an object for the Google Maps Autocomplete API service (Since we have both origin and destination,
    // we will create two objects, one for each)
    autocomplete = new google.maps.places.Autocomplete(input,
    {
        type: ['establishment'],
        componentRestrictions: {'country': ['IN']},
        fields: ['place_id','geometry','name']
    });
    autocomplete2 = new google.maps.places.Autocomplete(input2,
    {
        type: ['establishment'],
        componentRestrictions: {'country': ['IN']},
        fields: ['place_id','geometry','name']
    });

    // This will call "onPlaceChanged" function when an option from the dropdown suggestions is selected.
    // 'place_changed' is a value in google maps JavaScript API
    autocomplete.addListener('place_changed', onOriginChanged);
    autocomplete2.addListener('place_changed',onDestinationChanged);
}

// This line is responsible for loading this file and map on page.
google.maps.event.addDomListener(window, 'load', initialize);

function onOriginChanged(){
    
    // Using the object created in previous method, we will call "getPlace()" function (provided by google), to get 
    // place details like geometry and place_id (Geometry means latitude and longitude).
    var origin_place = autocomplete.getPlace();

    // We will check if the user has selected an input from the dropdown or has typed something himself without selecting anything from the dropdown.
    // This can be checked if the location has a geometry.
    if (!origin_place.geometry){
        document.getElementById('origin').placeholder = 'Enter a Place';
    }   else {
        // Setting Origin values to the hidden fields in the form.
        origin_lat = origin_place.geometry.location.lat()
        origin_lng = origin_place.geometry.location.lng()

        document.getElementById('origin_lat').value = origin_lat
        document.getElementById('origin_lng').value = origin_lng
    }

    // Creating a new map to display a marker on the map for the selected location
    const map = new google.maps.Map(document.getElementById('map'), {
        center: origin_place.geometry.location,
        zoom: 14,
        mapTypeControl: true,
        mapTypeControlOptions: {
        style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
        position: google.maps.ControlPosition.TOP_CENTER,
        }
    })

    const trafficlayer = new google.maps.TrafficLayer();

    trafficlayer.setMap(map);

    //Marker Object is created here
    marker = new google.maps.Marker({
        position: origin_place.geometry.location, map, title: 'Origin'
    })

    //If user changes location by clicking on map, below code is used to store it's geometry
    google.maps.event.addListener(map, 'click', function(event) {
        var clickedlocation = event.latLng;
        temp = marker.setPosition(clickedlocation)

        var latlng = {
            lat: clickedlocation.lat(),
            lng: clickedlocation.lng()
        }
        var geocoder = new google.maps.Geocoder();

        geocoder.geocode({location: latlng}, (results, status) =>{
            if (status == google.maps.GeocoderStatus.OK) {
                latitude = clickedlocation.lat();
                longitude = clickedlocation.lng();
                document.getElementById('origin_lat').value = latitude;
                document.getElementById('origin_lng').value = longitude;
                document.getElementById('origin').value = results[0].formatted_address;
            } else {
                window.alert(status);
            }
        });
      });
}

// Everything used in the "onOriginChanged()" is implemented in same way for the "onDestinationChanged()" method.
function onDestinationChanged(){
    var destination_place = autocomplete2.getPlace();

    if (!destination_place.geometry){
        document.getElementById('destination').placeholder = 'Enter a Place';
    }   else {

        destination_lat = destination_place.geometry.location.lat()
        destination_lng = destination_place.geometry.location.lng()

        document.getElementById('destination_lat').value = destination_lat
        document.getElementById('destination_lng').value = destination_lng
    }

    const map = new google.maps.Map(document.getElementById('map'), {
        center: destination_place.geometry.location,
        zoom: 14,
        mapTypeControl: true,
        mapTypeControlOptions: {
        style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
        position: google.maps.ControlPosition.TOP_CENTER,
        }
    })

    const trafficlayer = new google.maps.TrafficLayer();

    trafficlayer.setMap(map);

    marker = new google.maps.Marker({
        position: destination_place.geometry.location, map, title: 'Destination'
    })

    google.maps.event.addListener(map, 'click', function(event) {
        var clickedlocation = event.latLng;
        temp = marker.setPosition(clickedlocation)

        var latlng = {
            lat: clickedlocation.lat(),
            lng: clickedlocation.lng()
        }
        var geocoder = new google.maps.Geocoder();

        geocoder.geocode({location: latlng}, (results, status) =>{
            if (status == google.maps.GeocoderStatus.OK) {
                latitude = clickedlocation.lat();
                longitude = clickedlocation.lng();
                document.getElementById('destination_lat').value = latitude;
                document.getElementById('destination_lng').value = longitude;
                document.getElementById('destination').value = results[0].formatted_address;
            } else {
                window.alert(status);
            }
        });
    });
}

// getDirections() method is called when user clicks on the "Confirm" button.
function getDirections() {

    // Checking if origin and destination fields are empty or not.
    if (document.getElementById("origin").value != "" && document.getElementById("destination").value != "") {

        // Initialized and created object of DirectionsService() and DirectionsRenderer() services of google maps Directions API.
        var directionsService = new google.maps.DirectionsService();
        var directionsRenderer = new google.maps.DirectionsRenderer();

        var trafficlayer = new google.maps.TrafficLayer();

        // Getting geometry values from the hidden fields to use in directions services.
        origin_lat = document.getElementById("origin_lat").value
        origin_lng = document.getElementById("origin_lng").value

        destination_lat = document.getElementById("destination_lat").value
        destination_lng = document.getElementById("destination_lng").value

        // Created LatLng object using coordinates that we got from the hidden fields
        var origin_object = new google.maps.LatLng(origin_lat, origin_lng);
        var destination_object = new google.maps.LatLng(destination_lat, destination_lng);

         // Creating map to display the directions to the user.
        const map = new google.maps.Map(document.getElementById("map"), {
            center: {lat: 23.037506263879862, lng: 72.52325094533654},
            zoom: 7,
            mapTypeControl: true,
            mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
            position: google.maps.ControlPosition.TOP_CENTER,
            }
        });

        directionsRenderer.setMap(map);

        // Passed "map" object to the directionsRenderer service so that it can know on which map it has to display the directions.
        

        // Setting values for origin, destination and mode of travel in the "request" variable.
        var request = {
            origin: origin_object,
            destination: destination_object,
            travelMode: google.maps.TravelMode["DRIVING"]
        }

        // Passing request variable into "route()" method of directionsService which is responsible for displaying the route between
        // origin and destination.
        directionsService.route(request, function(response,status) {
            // If a direction is available, the status would return 'OK' and that means we can use the response to display the directions.
            if (status == "OK") {

                directionsRenderer.setDirections(response);

                // Creating object of DistanceMatrix to find the distance and duration of travelling from origin to destination.
                var distanceService = new google.maps.DistanceMatrixService();

                // getDistanceMatrix is a method which is responsible for calculating the distance and duration.
                distanceService.getDistanceMatrix({
                    // in distance matrix, origin takes a list as a value.
                    //list can be of latitude or longitude, name of place or place id.
                    origins: [origin_object],
                    //same goes with destination.
                    destinations: [destination_object],
                    travelMode: google.maps.TravelMode["TRANSIT"],
                    unitSystem: google.maps.UnitSystem["METRIC"]
                }, (response,status) => {
                    if (status == "OK") {
                        var origins = response.originAddresses;
                        var destinations = response.destinationAddresses;

                        for (var i = 0; i < origins.length; i++) {
                        var results = response.rows[i].elements;
                        for (var j = 0; j < results.length; j++) {
                            var element = results[j];
                            var distance = element.distance.text;
                            var duration = element.duration.text;
                            }
                        }
                        
                        var box = document.createElement('div');
                        box.style.backgroundColor = '#ffffff';
                        box.style.opacity = '0.8';

                        // var temp = document.createElement('h6');
                        // temp.innerHTML = "Distance and Duration: " + distance + " and " + duration;
                        // box.appendChild(temp);
                        // map.controls[google.maps.ControlPosition.TOP_LEFT].push(box);
                        
                        var mydistance = document.createElement('h6');
                        mydistance.innerHTML = 'Distance: ' + distance;
                        var myduration = document.createElement('h6');
                        myduration.innerHTML = 'Duration: ' + duration;

                        box.appendChild(mydistance);
                        box.appendChild(myduration);
                        map.controls[google.maps.ControlPosition.TOP_LEFT].push(box);
                        // map.controls[google.maps.ControlPosition.TOP_LEFT].push(box);

                        // window.alert(distance);
                        // window,alert(duration);
                    } else {
                        window.alert(status)
                    }
                });
            }
            // If a direction is not available (an invalid origin or destination is selected or entered by the user)
            // an error would be displayed.
            else {
                window.alert("Unable to find direction due to" + status);
            }
        });
    }
    // This is the else part for the first "if" that checked if origin and destination fields are not empty.
    else {
        alert("Please enter a place")
    }
}