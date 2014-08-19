function LocationPlotter(opts) {
	this.location_points = []
	this.file = ''
	this.type = ''
	$.extend(this, opts);
	
	this.populate()
}

LocationPlotter.prototype._readTextFile = function(fn) {
    var rawFile = new XMLHttpRequest();
	var self = this;
    rawFile.open("GET", this.file, false);
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
	this._readTextFile(function(text) {
		lines = text.split('\n')
		for (i in lines) {
			line_sections = lines[i].split(',')
			if (this.type === 'restaurants') {
				if (line_sections[1]) {
					var place_location = new google.maps.LatLng(parseFloat(line_sections[1]), parseFloat(line_sections[2]))
					this.location_points.push({
						point: place_location, 
						name: line_sections[0].trim()
					});
				}
			} else if (this.type === 'building_location') {
				if (line_sections[2]) {
					var place_location = new google.maps.LatLng(parseFloat(line_sections[2]), parseFloat(line_sections[3]))
					this.location_points.push({
						point: place_location, 
						name: line_sections[0].trim() + line_sections[1].trim()
					});
				}
			} else if (this.type === 'building_cover') {
				if (line_sections[4] && line_sections[4].trim()) {
					points = line_sections[4].split('|')
					var cover_holder = []
					//var place_location = new google.maps.LatLng(parseFloat(line_sections[2]), parseFloat(line_sections[3]))
					for (i in points) {
						console.log('mauahahah', points[i])
						var lat = points[i].split('&')[0]
						var lng = points[i].split('&')[1]
						cover_holder.push(new google.maps.LatLng(lat, lng));
					}
					this.location_points.push(cover_holder)
				}
			} else if (this.type === 'parking') {
			
			} else if (this.type === 'recreational') {
			
			}
		}
	
	}); //readtextfile
}

LocationPlotter.prototype.getPoints = function() {
	return this.location_points;
}

LocationPlotter.prototype.remove = function() {
	
}

LocationPlotter.prototype.add = function() {
	if (this.type === 'building_cover') {
		addCover(this.location_points);
	} else {
		for (i in this.location_points) {
			addMarker(this.location_points[i].point, this.location_points[i].name);
		}
	}
	
}


