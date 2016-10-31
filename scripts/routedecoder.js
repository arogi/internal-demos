// decode an encoded shape (and return an array of coordinates)
function legDecoder(numberOfLegs, passedLegArray){
    decodedLegArray = {};
    aLegCounter = 0;
    while (aLegCounter < numberOfLegs) {

      str = passedLegArray[aLegCounter];
      // precision per the Mapzen Valhalla documentation (6); differs from Google polyline encoding (5)
      precision = 6;

      var index = 0,
      lat = 0,
      lng = 0,
      coordinates = [],
      shift = 0,
      result = 0,
      byte = null,
      latitude_change,
      longitude_change,
      factor = Math.pow(10, precision || 6);

      // Coordinates have variable length when encoded, so just keep
      // track of whether we've hit the end of the string. In each
      // loop iteration, a single coordinate is decoded.
      while (index < str.length) {

        // Reset shift, result, and byte
        byte = null;
        shift = 0;
        result = 0;

        do {
          byte = str.charCodeAt(index++) - 63;
          result |= (byte & 0x1f) << shift;
          shift += 5;
        } while (byte >= 0x20);

        latitude_change = ((result & 1) ? ~(result >> 1) : (result >> 1));
        shift = result = 0;

        do {
          byte = str.charCodeAt(index++) - 63;
          result |= (byte & 0x1f) << shift;
          shift += 5;
        } while (byte >= 0x20);

        longitude_change = ((result & 1) ? ~(result >> 1) : (result >> 1));

        lat += latitude_change;
        lng += longitude_change;

        coordinates.push([lng / factor, lat / factor]);
      }

      decodedLegArray[aLegCounter] = coordinates;
      aLegCounter = aLegCounter + 1;
    }
    return decodedLegArray;
};

// create a polyline GeoJSON from an array of coordinate pairs
function geojsonMaker(numSolutionLegs, decodedLegCoordinates2){
  var ourGeojson = {
    "name":"NewFeatureType",
    "type":"FeatureCollection",
    "features":[]
  };
  var iCounter = 0;
  while (iCounter < numSolutionLegs) {
    var eachFeature = {
      "type":"Feature",
      "geometry":{
        "type":"LineString",
        "coordinates": decodedLegCoordinates2[iCounter]
      },
      "properties":null
    };
    ourGeojson.features[iCounter] = eachFeature;
    iCounter = iCounter + 1;
  };
  return ourGeojson;
};


// function to find number of markers
function objectLength(obj) {
  var result = 0;
  for(var prop in obj) {
    if (obj.hasOwnProperty(prop)) {
      result++;
    }
  }
  return result;
};
