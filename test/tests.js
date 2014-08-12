var assert = require('assert');
var http = require('http');
var course_model = require('../models/courses.js');
var request = require('request');

var port = 1337

describe('Connection and Setup', function(){
  describe('Server is up', function(){
    it('should get response', function(done){
      http.get({path: '/', port: port}, function(res) {
        assert(res, "Cannot establish connection to server.")
        done()
      })
    }) //it
  }) //describe 

  describe('Server is set up as a test server', function(){
    it('should have test env', function(done){
      request('http://localhost:1337/env', function (err, res, body) {
        assert.strictEqual(body, '"test"', "You should run the server with the following: 'NODE_ENV=test node app.js'")
        done()
      })
    }) //it
  }) //describe 
}) //main describe

describe('Status codes', function(){
  describe('GET /places/buildings', function(){
    it('would return a 200 reponse', function(done){
    	http.get({path: '/places/buildings', port: port}, function(res) {
        assert.equal(res.statusCode, 200, 'Expected 200, Actual ' + res.statusCode)
        done()
      })
    })
  }) //describe

  describe('GET /places/blahblah', function(){
    it('would return a 404 reponse', function(done){
      http.get({path: '/places/blahblah', port: port}, function(res) {
        assert.equal(res.statusCode, 404, 'Expected 404, Actual ' + res.statusCode)
        done()
      })
    })
  }) //describe

  describe('POST /courses', function(){
     var post_data = {
        'term_years_offered': [1415], 
        'description': '', 
        'title': 'Introduction To Financial Accounting I', 
        'course_subject': 'ACTG', 
        'year_level': 2, 
        'credit_count': 3, 
        'course_number': '2010', 
        'faculty': 'SB', 
        'course_code': 'ACTG2010'
    }

    var options = {
      url: 'http://localhost:1337/courses', 
      headers: {
        'content-type': 'application/json'
      },
      method: 'POST',
      json: post_data
    }

    it('would return success!', function(done){
      request(options, function (err, res, body) {
        //console.log('ERROR: ', err)
        //console.log('BODY: ', body)
        done()
      });
        //assert.equal(res.statusCode, 404, 'Expected 404, Actual ' + res.statusCode)
    }) //it
  }) //describe

}) //describe main