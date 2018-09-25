app.controller('ResultListController', [
        "$scope","$ionicModal","$state" , "$stateParams","$http",
        "AllDiseaseParameter","ExaminingAnswers","HypothesisParameter",
        "ServerLinkProperty","$ionicPopup","$timeout",
        function($scope,$ionicModal, $state, $stateParams,$http,
                AllDiseaseParameter,ExaminingAnswers, HypothesisParameter,
                ServerLinkProperty,$ionicPopup,$timeout)
    {

        // Global Variables
        $scope.load = true;
        var TimeOutPromise = null;
        var Timeout = false;


        // This function gets the end link from the Examine End Link
        var GetQuestion = function (parameter){
            $http.get(ServerLinkProperty.get() 
                    + "/Rules/Examine/" 
                    + parameter +"/" 
                    + HypothesisParameter.getExaminingProperty() 
                    + "/?format=json", {})
            .then(function (response) {
                $scope.AllDisease = response.data.result_item;
                $scope.orderByAttribute = 'cf';
                
                $scope.load = false;
                $timeout.cancel(TimeOutPromise);
                if(Object.keys(response.data.result_item).length == 0){
                    showPopup();
                }
                return response
        }, function (ErrorResponse) {
            console.log(ErrorResponse);

            // If the timer did not timeout, tries to fetch the data again. 
            if(Timeout == false){
                GetEndLinkData();
            }

           });
        };

        showPopup = function() {
            var alertPopup = $ionicPopup.alert({
              title: 'No Result',
              subTitle: "The application didn't detect any result!",
              cssClass: 'alertNoResult'
            });
        };


        
     

        // Loads up the search modal so it can be use by this controller
        $ionicModal.fromTemplateUrl('SearchModal.html', {
                scope: $scope,
                animation: 'slide-in-up'
            }).then(function (modal) {
                $scope.SearchModal = modal;    
        });

        // This function opens up the search modal
        $scope.openSearchModal = function () {
          $scope.SearchModal.show();
        };

        // This function hides the search modal
        $scope.closeSearchModal = function () {
          $scope.SearchModal.hide();
        };

        $ionicModal.fromTemplateUrl('AboutModal.html', {
                scope: $scope,
                animation: 'fade-in'
            }).then(function (modal) {
                $scope.AboutModal = modal;    
        });

            
        $scope.OpenAboutModal = function(){
          $scope.AboutModal.show();
        };

        $scope.closeAboutModal = function () {
          $scope.AboutModal.hide();
        };
        // This function passes you to the search page
        $scope.SearchDisease = function(SearchText){
            $scope.SearchModal.hide();
            if(SearchText!=null){
                RemoveSpace=SearchText.split(' ').join('');
                if(RemoveSpace != ""){
                    AllDiseaseParameter.setParameter(SearchText);
                }else{
                    AllDiseaseParameter.setParameter('All');
                }
            }else{
                AllDiseaseParameter.setParameter('All');
            }
            $timeout.cancel(TimeOutPromise);
            $state.go('AllDiseaseList', {});
        }

        // This function passes you to disease details
        $scope.GoToDisease = function(DiseaseID){
            $timeout.cancel(TimeOutPromise);
            $state.go('DiseaseDetails', {ID:DiseaseID});
        }

        $scope.goHome = function(DiseaseID){
            $timeout.cancel(TimeOutPromise);
            $state.go('home', {});
        }


        // This function purpose is the go back button
        // It passes you home if the examining property is set to start
        //     otherwise it will try to reduce one answer and ask you again
        $scope.goBack = function(){
            HypothesisParameter.setExaminingProperty("0");
            if(ExaminingAnswers.getExaminingProperty() == "start"){
                $timeout.cancel(TimeOutPromise);
                $state.go('home', {});
            }else{
                ToSplit = ExaminingAnswers.getExaminingProperty();
                new_stack = "";
                ArrayToReduceOne = ToSplit.split(',');
                popped = ArrayToReduceOne.pop();
                
                a = 0;
                while(a < ArrayToReduceOne.length){
                    new_stack += ArrayToReduceOne[a];
                    if(a != ArrayToReduceOne.length -1){
                        new_stack += ",";
                    }
                    a+=1;
                }


                if(new_stack == ""){
                    ExaminingAnswers.setExaminingProperty("start");
                    $timeout.cancel(TimeOutPromise);
                    $state.go('examining', {});
                }else{
                    ExaminingAnswers.setExaminingProperty(new_stack);
                    $timeout.cancel(TimeOutPromise);
                    $state.go('examining', {});
                }
            }
            
        }

        function StartTimeout(){
            TimeOutPromise = $timeout( function(){
                    $scope.load = false;

                    // Cancels the timeout so it won't run again after the timeout
                    TimeOutPromise = null;

                    // Set your timeout into true so the GetQuestion function won't
                    //      Loop forever.
                    Timeout = true;
                    $ionicPopup.show({
                                  title: 'Please check your internet connection.',
                                      buttons: [
                                      {
                                        text: 'Retry',
                                        type: 'button-positive',
                                        // Button Function
                                        onTap: function(e) {
                                        // Tries to get the end link again
                                        Timeout = false;
                                        $scope.load = true;
                                        initialize();
                                   }
                                  }
                            ]
                    });
            },5000);
        };

        function GetEndLinkData(){
            // Gets the end link data
            parameter = ExaminingAnswers.getExaminingProperty();
            GetQuestion(parameter);
        };

        function initialize(){
            StartTimeout();
            GetEndLinkData();
        };


        initialize();



}]);