app.controller('ExaminingController', ["$scope","$ionicModal","$state" , 
        "$stateParams","$http","AllDiseaseParameter","ExaminingAnswers"
        ,"HypothesisParameter","ServerLinkProperty","$ionicPopup","$timeout",
    function($scope,$ionicModal, $state, $stateParams,
            $http,AllDiseaseParameter,ExaminingAnswers,
            HypothesisParameter,ServerLinkProperty,$ionicPopup,$timeout)
    {

        //Global Variable
        $scope.load = true;
        $scope.progress = 0;
        back = false;
        var TimeOutPromise = null;
        var Timeout = false;

        // This Function gets the question, if no more question can be fetch from the data
        //      it will go to the Result List Page
        var GetQuestion = function (parameter){
            $http.get(ServerLinkProperty.get() + "/Rules/Examine/" + parameter +"/" + HypothesisParameter.getExaminingProperty() + "/?format=json", {})
            .then(function (response) {
                $scope.load = false;
                $timeout.cancel(TimeOutPromise);
                $scope.data = response.data;
                if ($scope.data.progress != "no change"){
                    if(back == false){
                        if($scope.data.progress > $scope.progress){
                            $scope.progress = $scope.data.progress;
                        }
                    }else{
                        $scope.progress = $scope.data.progress
                    }

                    
                }
                
                if ($scope.data.result == "yes"){
                    $timeout.cancel(TimeOutPromise);
                    $state.go('ResultList',{});
                }else{
                    after_server_link = response.data.question[0].image;
                    HypothesisParameter.setExaminingProperty($scope.data.hypothesis);
                    // join the image path
                    if (response.data.question[0].image == "/media/media/None/no-img.jpg" || response.data.question[0].image == null){
                        $scope.show_image = false;
                        after_server_link = response.data.question[0].image;
                        $scope.image = ServerLinkProperty.get() + after_server_link;
                    }else{
                        $scope.show_image = true;
                        after_server_link = response.data.question[0].image;
                        $scope.image = ServerLinkProperty.get() + after_server_link;
                    }
                
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

        function shakeContainer(id){
            angular.element(document.querySelector(id))[0].style.position = "relative";
            function cPosition(pos){
                angular.element(document.querySelector(id))[0].style.left = pos + "px";
            }
            function popPosition(p){
                var g = p.shift();
                cPosition(g);
                if(p.length > 0){
                    setTimeout(function(){
                        popPosition(p);
                    }, 20);
                }
            }
            var pattern = new Array(2, 5, 1, 0, -2, -5, -1, 0);
            pattern = pattern.concat(pattern.concat(pattern));
            popPosition(pattern);
        }

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


        $ionicModal.fromTemplateUrl('ImageModal.html', {
                scope: $scope,
                animation: 'slide-in-up'
            }).then(function (modal) {
                $scope.ImageModal = modal;    
        });

        // This function opens up the search modal
        $scope.openImageModal = function () {
          $scope.ImageModal.show();
        };

        // This function hides the search modal
        $scope.closeImageModal = function () {
          $scope.ImageModal.hide();
        };
        
        // This function goes back 1 page
        $scope.goBack = function(){
            $timeout.cancel(TimeOutPromise);
           window.history.go(-1);
        }

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

        // This function transfers you to the search disease page with the parameter
        //          SearchText
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

        $scope.goHome = function(DiseaseID){
            $timeout.cancel(TimeOutPromise);
            $state.go('home', {});
        }



        // This function goes back to home if no answers are detected
        //      else, it  will try to remove the latest answer from the collection
        //      of answers and refresh the examining page
        $scope.goBack = function(){

            back = true;

            HypothesisParameter.setExaminingProperty("0");
            if(ExaminingAnswers.getExaminingProperty() == "start"){
                $timeout.cancel(TimeOutPromise);
                $state.go('home', {});
            }else{
                Reduce_One = ExaminingAnswers.getExaminingProperty();
                new_stack = "";
                Arr_Reduce_One = Reduce_One.split(',');
                popped = Arr_Reduce_One.pop();
                
                a = 0;
                while(a < Arr_Reduce_One.length){
                    new_stack += Arr_Reduce_One[a];
                    if(a != Arr_Reduce_One.length -1){
                        new_stack += ",";
                    }
                    a+=1;
                }


                if(new_stack == ""){
                    $timeout.cancel(TimeOutPromise);
                    ExaminingAnswers.setExaminingProperty("start");
                    initialize();
                }else{
                    $timeout.cancel(TimeOutPromise);
                    ExaminingAnswers.setExaminingProperty(new_stack);
                    initialize();
                }
            }
            
        }


        //  This function collects the id of the answered question and
        //      the answer cf separated by '='. If the answer is a 'yes' 
        //      then the certainty factor would be 1 if it's a 'no' 
        //      then it would be '-1'. E.g. "id>answer","1=1,"
        $scope.Yes_Next =function(ans){

            if(ans!=null){

                $timeout.cancel(TimeOutPromise);
                if(ExaminingAnswers.getExaminingProperty() == "start"){
                    ExaminingAnswers.setExaminingProperty("");
                }
                stack_param = "";
                if(ExaminingAnswers.getExaminingProperty() != ""){
                    stack_param = ExaminingAnswers.getExaminingProperty() + ","
                }
                stack_param = stack_param  + ans + "=1";
                ExaminingAnswers.setExaminingProperty(stack_param);

                shakeContainer(".ProgressBar");
                initialize();
            }
        }

        //  This function collects the id of the answered question and
        //      the answer cf separated by '='. If the answer is a 'yes' 
        //      then the certainty factor would be 1 if it's a 'no' 
        //      then it would be '-1'. E.g. "id>answer","1=1,2=-1"

        $scope.No_Next =function(ans){

            if(ans!=null){
                $timeout.cancel(TimeOutPromise);
                if(ExaminingAnswers.getExaminingProperty() == "start"){
                    ExaminingAnswers.setExaminingProperty("");
                }

                stack_param = "";
                if(ExaminingAnswers.getExaminingProperty() != ""){
                    stack_param = ExaminingAnswers.getExaminingProperty() + ","
                }
                stack_param = stack_param  + ans + "=-1";


                ExaminingAnswers.setExaminingProperty(stack_param);
                shakeContainer(".ProgressBar");
                initialize();

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
        
        GetEndLinkData = function GetEndLinkData(){
            // The function to get the EndLinkData

            $scope.data = null;
            $scope.load = true;
            parameter = ExaminingAnswers.getExaminingProperty();
            GetQuestion(parameter);
        };
        
        function initialize(){
            // initialization of the page
            StartTimeout();
            GetEndLinkData();
        };

        initialize();


}]);