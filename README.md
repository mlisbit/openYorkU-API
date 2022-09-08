# Open YorkU API
### A Restful API for all things York University.

#### Why is this being built?

York University is the 3rd largest university in Canada, and with the recent addition of Lassonde school of Engineering - it's about time something like this existed. Though I doubt openYorkU will become officially adapted, I hope York will see the potential and allow for easier access to their information.

With open data, students may create brilliant apps around it, and profs will have a large data set to work with and discover things otherwise overlooked. Tying this type of service around clubs, news and events; information will travel faster throughout the campus. The world will become aware of all the great things York University offers.

#### Universities with API's of their own.

* [Waterloo University](https://github.com/uWaterloo/api-documentation)
* [Berkeley University](https://developer.berkeley.edu/)
* [University of Michigan](http://developer.it.umich.edu/)
* [Others.](http://blog.mashape.com/list-of-15-university-apis/)

#### Possible app ideas.

* improved map of campus 
    * plot all food buildings, recreational areas, parking lots, and libraries.
    * directions to everything.
    * find the nearest bathroom facilities, art exhibits, or other place of interest.
    * find currently open restaurants and buildings. 
    * *not enough people know about all the great food places at York, cool study spots, and recreational areas.*
  * ratings 
    * courses (easiness/usefullness)
    * buildings (cleanliness/architectual appeal)
    * restaurants (cleanliness/cost/quantity)
  * social timetable picker (like [uwflow](https://uwflow.com/))
    * pick timetables with your friends, so you're all in the same courses. 
  * event notifications
    * with support for clubs to post events, every event would be known about 
    * (no more missing a bakesale, or a poster sale in Vari Hall.)

#### Examples
Once you've set up the app, and populated the database with entries using resources within the dev_helpers folder, you'll be able to do the following:

  * **localhost:1337/courses** to get a list of all the courses york has to offer.
  * **localhost:1337/courses?limit=5&fields=title&q=science** get only the titles of 5 courses with 'science' in it.
  * **localhost:1337/courses/#course_code#** look a little closer at the course.
  * **localhost:1337/courses?credit_count=3,6&year_level=3&course_subject=EECS** get all the 3rd year computer science programs with a credit count of 3 or 6.
  * **localhost:1337/subjects** get a list of all the subjects, and their respective courses
  * **localhost:1337/places/restaurants** get a list of all the restaurants at York, their open/close times, gps co-ordinates, and types of food served.
  * **localhost:1337/places/restaurants?tags=coffee&now_open=1** get all the open coffee shops
  * **localhost:1337/places/buildings** get a list of all buildings, including all Points of Interests within them, gps co-ordinates, and building cover polygon for google maps. 

#### Contact
Maciej Lis <[mlisbit@gmail.com](mailto:mlisbit@gmail.com)>.

#### Other York University APIs

Some other York University APIs, made by other students, include:

* https://github.com/SSADC-at-york/Yoki
* https://yorkapi.isaackogan.com/ by @isaackogan
