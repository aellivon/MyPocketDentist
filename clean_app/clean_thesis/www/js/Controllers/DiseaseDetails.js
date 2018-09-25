app.controller('DiseaseDetails', ["$scope","$ionicModal","$state" ,
        "$stateParams","$http","AllDiseaseParameter","ServerLinkProperty",
        "$timeout","$ionicPopup",
    function($scope,$ionicModal, $state, 
            $stateParams,$http,AllDiseaseParameter,ServerLinkProperty
            ,$timeout,$ionicPopup)
    {
        // Global Variables
        $scope.load = true;
        var TimeOutPromise = null;
        var Timeout = false;
        $scope.image_to_show = "";
        
         // Gets the details from the end link
         GetDiseaseDetails =function (id){
                  $http.get(ServerLinkProperty.get() + "/Disease/DiseaseProfile/" +  id + "/", {})
                    .then(function (response) {

                        $scope.DiseaseName = response.data.disease[0].name; 
                        $scope.Advise = response.data.disease[0].advise;
                        $scope.Cause = response.data.disease[0].cause;
                        
                        $scope.Details = response.data.disease[0].details;
                        $scope.Evidence = response.data.evidence;
                        count = 0;
                        while($scope.Evidence.length > count){
                            if($scope.Evidence[count].image == "/media/media/None/no-img.jpg" || $scope.Evidence[count].image == null){
                                $scope.Evidence[count].image = "";
                            }
                            count+=1;
                        }
                        $scope.load = false;
                        $timeout.cancel(TimeOutPromise);
                        return response
                    }, function (ErrorResponse) {
                        console.log(ErrorResponse);
                        if (Timeout == false){
                            GetDiseaseDetails($stateParams.ID);
                        }
                    });
        };


        // Loads up the search modal so it can be use by this controller

        $ionicModal.fromTemplateUrl('SearchModal.html', {
                scope: $scope,
                animation: 'slide-in-up'
            }).then(function (modal) {
                $scope.SearchModal = modal;    
        });


        $ionicModal.fromTemplateUrl('ImageModal.html', {
                scope: $scope,
                animation: 'slide-in-up'
            }).then(function (modal) {
                $scope.ImageModal = modal;    
        });

        // This function opens up the search modal
        $scope.openImageModal = function (image) {
          $scope.image = ServerLinkProperty.get() + image;
          $scope.ImageModal.show();
        };

        // This function hides the search modal
        $scope.closeImageModal = function () {
          $scope.ImageModal.hide();
        };

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
        
        // This function transfers  you to All  Disease List with the paremeter SearchText
        //      from the modal text.

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

        // This function goes back 1 page
        $scope.goBack = function(){
            $timeout.cancel(TimeOutPromise);
            window.history.go(-1);
        }

        $scope.goHome = function(DiseaseID){
            $timeout.cancel(TimeOutPromise);
            $state.go('home', {});
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

        function initialize(){
            // Initialization of the Page
            StartTimeout();
            GetDiseaseDetails($stateParams.ID);
            
        };

        initialize();
}]);