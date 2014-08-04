function LocationPlotter(opts) {
	this.location_points = []
	this.file = ''
	this.type = ''
	$.extend(this, opts);
	
	this.populate()
}

function readTextFile(self, file, fn) {
	
    var rawFile = new XMLHttpRequest();
	
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
				if (typeof(fn) === 'function') {
                	fn.call(self, rawFile.responseText)
				}
            }
        }
    }
    rawFile.send(null);
}

LocationPlotter.prototype.populate = function() {
	var self = this
	readTextFile(self, this.file, function(text) {
		lines = text.split('\n')
		for (i in lines) {
			line_sections = lines[i].split(',')
			if (this.type === 'restaurants') {
				if (line_sections[1]) {
					place_location = new google.maps.LatLng(parseFloat(line_sections[1]), parseFloat(line_sections[2]))
					this.location_points.push({
						point: place_location, 
						name: line_sections[0].trim()
					});
				}
			} else if (this.type === 'buildings') {
			
			} else if (this.type === 'parking') {
			
			} else if (this.type === 'recreational') {
			
			}
		}
	
	}); //readtextfile
}

LocationPlotter.prototype.remove = function() {
	
}

LocationPlotter.prototype.add = function() {
	for (i in this.location_points) {
		addMarker(this.location_points[i].point, this.location_points[i].name);
	}
}


