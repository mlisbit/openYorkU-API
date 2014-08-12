var assert = require("assert")
var course_model = require('../models/courses.js');

describe('Array', function(){
  describe('#indexOf()', function(){
    it('should return -1 when the value is not present', function(){
      assert.equal(-1, [1,2,3].indexOf(5), 'wtf');
      assert.equal(-1, [1,2,3].indexOf(0), "wtf");
    })
  })
})

describe('Async testing', function(){
  describe('adding a new user', function(){
    it('should return something...', function(){
    	var body = {'term_years_offered': [1415], 'description': '', 'title': 'Introduction To Financial Accounting I', 'course_subject': 'ACTG', 'year_level': 2, 'credit_count': 3, 'course_number': '2010', 'faculty': 'SB', 'course_code': 'ACTG201043'}
    	var instance = new Course(body);
    	//console.log(instance)
    	instance.save(function(err) {
			if (err) {
				console.log(err)
			}
			done()
		})
    })
  })
})

describe('Async testing', function(){
  describe('print courses', function(){
    it('should return something...', function(done){
    	console.log('starting search')
   		Course.find({},function (err, courses) {
        	console.log('hello?: ' + courses[0])
        	done()
    	});
    	
    	
    })
  })
})