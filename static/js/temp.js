function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: {lat: 23.037506263879862, lng: 72.52325094533654},
        zoom: 7,
    });

    new handler(map);
}

class handler {
    map;
    origin_place_id; 
    destination_place_id;
    directionsService;
    directionsRenderer;
    constructor(map) {
        this.map = map;
        this.origin_place_id = "" ;
        this.destination_place_id = "" ;
        this.directionsService = new google.maps.DirectionsService();
        this.directionsRenderer = new google.maps.DirectionsRenderer();
        this.directionsRenderer.setMap(map);

        const origin_input = document.getElementById("origin");
        const destination_input = document.getElementById("destination");

        const origin_autocomplete = new google.maps.places.Autocomplete(origin_input, 
            {
                type: ['establishment'],
                componentRestrictions: {'country': ['IN']},
                fields: ["place_id", "geometry", "name"]
            }
        );
        const destination_autocomplete = new google.maps.places.Autocomplete(destination_input, 
            {
                type: ['establishment'],
                componentRestrictions: {'country': ['IN']},
                fields: ["place_id", "geometry", "name"]
            }
        );

        // this.setupClickListener("confirm-direction");

        this.setupPlaceChangedListener(origin_autocomplete, "ORIG");
        this.setupPlaceChangedListener(destination_autocomplete, "DEST");

    }

    // setupClickListene(id) {
    //     window.alert("Click Listener")
    //     const c = document.getElementById(id);

    //     c.addEventListener("click", () => {
    //         this.route();
    //     })
    // }

    setupPlaceChangedListener(autocomplete, mode) {
        autocomplete.bindTo("bounds", this.map);
        autocomplete.addListener("place_changed", () => {
            const place = autocomplete.getPlace();

            if (!place.geometry) {
                window.alert("Please select an option from the dropdown list");
                return;
            }

            if (mode === "ORIG") {
                window.alert("it's origin");
                this.origin_place_id = place.name;
                window.alert(this.origin_place_id);
            } else {
                window.alert("it's destination");
                this.destination_place_id = place.name;
            }
        });
        this.route();
    }

    route() {
        if (!this.origin_place_id || !this.destination_place_id) {
            return;
        }

        this.directionsService.route(
            {
                origin: this.origin_place_id,
                destination: this.destination_place_id,
                travelMode: google.maps.TravelMode["DRIVING"]
            },
            (response, status) => {
                if (status === "OK") {
                    this.directionsRenderer.setDirections(response);
                } else {
                    window.alert("Failed to display directions: " + status);
                }
            }
        );
    }
}

google.maps.event.addDomListener(window, 'load', initMap);