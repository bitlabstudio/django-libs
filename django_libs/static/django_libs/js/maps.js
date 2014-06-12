/* 
 * Utility functions for use with Google maps
 *
 */
/* global google */

function centerOnPosition(map, lat, lon) {
    // centers the map on a certain position
    map.setCenter(new google.maps.LatLng(lat, lon));
}

function centerOnMarkerPosition(map, lat, lon, marker) {
    // centers the map on a certain position
    centerOnPosition(map, lat, lon);

    // close all open info windows
    for (var i=0; i<window.GoogleMapInfoWindows.length; i++) {
        window.GoogleMapInfoWindows[i].close();
    }

    // trigger a click to open info window
    google.maps.event.trigger(marker, 'click');
}

function createInfoWindow(data, map, marker) {
    // fetches the content for the info window via ajax and adds the
    // listener to the marker, that opens the window.
    var infowindow = new google.maps.InfoWindow({
        content: data
    });
    // add the click listener to the marker to open the info window
    google.maps.event.addListener(marker, 'click', function(){
        infowindow.open(map, marker);
    });
    window.GoogleMapInfoWindows.push(infowindow);
}

function createInfoWindowAJAX(url, map, marker) {
    // fetches the content for the info window via ajax and then creates
    // the info window

    $.ajax({
        url: url,
        success: function(data) {
            createInfoWindow(data, map, marker);
        }
    });
}

function createMarker(lat, lon, map, title) {
    // creates a new marker on the map
    if (title===undefined) {title='';}
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(lat, lon),
        map: map,
        title: title,
    });
    return marker;
}
