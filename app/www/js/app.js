// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
var app = angular.module('MobileOralDiagnosis', ['ionic', 'ui.router'])





.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    if(window.cordova && window.cordova.plugins.Keyboard) {
      // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
      // for form inputs)
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);

      // Don't remove this line unless you know what you are doing. It stops the viewport
      // from snapping when text inputs are focused. Ionic handles this internally for
      // a much nicer keyboard experience.
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
})


app.service('AllDiseaseParameter', function () {   
  // This Service defines the disease to be displayed in the disease list
  //      template

   var parameter = 'All';

        return {
            getParameter: function () {
                return parameter;
            },
            setParameter: function(value) {
                parameter = value;
            }
        };
});

app.filter('orderObjectBy', function(){
  // This function orders by json data into descending order
  // attribute = the attribute that we will base on ordering
  // input = the whole 'data'

 return function(input, attribute) {
    // Checks if the 'input' is valid
    if (!angular.isObject(input)) return input;

    var array = [];
    // Since json cannot be sorted, we push the json data into array
    for(var objectKey in input) {
        array.push(input[objectKey]);
    }

    // Sorts the array
    array.sort(function(a, b){
        // Compares the two attribute value
         // "b-a" = Descending. a-b, will go for Ascending
        
        a = parseFloat(a[attribute]);
        b = parseFloat(b[attribute]);
       
        return b - a;
    });

    return array;
 }
});

app.service('ExaminingAnswers', function () {     
  // This Examining Service stores the question that is answered by the user
   var ExaminingProperty = 'start';
  

        return {
            getExaminingProperty: function () {
                return ExaminingProperty;
            },
            setExaminingProperty: function(value) {
                ExaminingProperty = value;
            }
        };

});

app.service('HypothesisParameter', function () {     
  // This Examining Service stores the hypothesis
   var HypothesisParameter = '0';
  

        return {
            getExaminingProperty: function () {
                return HypothesisParameter;
            },
            setExaminingProperty: function(value) {
                HypothesisParameter = value;
            }
        };

});

app.service('ServerLinkProperty', function () {     
  // This Examining Service stores the question that is answered by the user
  var ServerLinkProperty = 'http://127.0.0.1:8000';
  // var ServerLinkProperty = 'http://mobileoraldiagnosis.pythonanywhere.com';

        return {
            get: function () {
                return ServerLinkProperty;
            }
        };

});



app.config(function($stateProvider, $urlRouterProvider) {


  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js




$urlRouterProvider.otherwise('/home');
  $stateProvider

// HOME STATES AND NESTED VIEWS ========================================
        .state('home', {
            url: '/home',
            templateUrl: 'Templates/home.html',
            controller: 'HomeController'
        })

        .state('examining', {
            url: '/examining',
            templateUrl: 'Templates/examining.html',
            controller: 'ExaminingController'
        })

        .state('AllDiseaseList', {
            url: '/AllDiseaseList',
            templateUrl: 'Templates/AllDiseaseList.html',
            controller: 'AllDiseaseController'
        })



        .state('DiseaseDetails', {
            url: '/DiseaseDetails/:ID',
            templateUrl: 'Templates/DiseaseDetails.html',
            controller: 'DiseaseDetails'

        })

        .state('ResultList', {
            url: '/ResultList/',
            templateUrl: 'Templates/ResultList.html',
            controller: 'ResultListController'

        })

      })



/*
  This directive is used to disable the "drag to open" functionality of the Side-Menu
  when you are dragging a Slider component.
*/

.directive('disableSideMenuDrag', ['$ionicSideMenuDelegate', '$rootScope', function($ionicSideMenuDelegate, $rootScope) {
    return {
        restrict: "A",  
        controller: ['$scope', '$element', '$attrs', function ($scope, $element, $attrs) {

            function stopDrag(){
              $ionicSideMenuDelegate.canDragContent(false);
            }

            function allowDrag(){
              $ionicSideMenuDelegate.canDragContent(true);
            }

            $rootScope.$on('$ionicSlides.slideChangeEnd', allowDrag);
            $element.on('touchstart', stopDrag);
            $element.on('touchend', allowDrag);
            $element.on('mousedown', stopDrag);
            $element.on('mouseup', allowDrag);

        }]
    };
}])