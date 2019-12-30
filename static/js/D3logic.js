// Perform an API call to the Divvy Station Information endpoint
d3.json("https://gbfs.divvybikes.com/gbfs/en/station_information.json", function(infoRes) {

    var stationInfo = infoRes.data.stations;
});
console.log(stationInfo)

var fs = require("fs");

fs.writeFile("station.json", JSON.stringify(stationInfo, null, 4), (err) => {
    if (err) {
        console.error(err);
        return;
    };
    console.log("File has been created");
});