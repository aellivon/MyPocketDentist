app.controller('AllDiseaseController', [
        "$scope","$ionicModal","$state" , "$stateParams","$http",
        "AllDiseaseParameter","ServerLinkProperty","$ionicPopup","$timeout",
    function($scope,$ionicModal, $state, $stateParams,$http,
            AllDiseaseParameter,ServerLinkProperty,$ionicPopup,$timeout)
    {
        // Global Variables
        $scope.load = true;
        var TimeOutPromise = null;
        var Timeout = false;

        // This Function gets the details of all diseases from the an end link
        GetAllDisease =function (){
            $http.get(ServerLinkProperty.get() + "/Disease/ListOfAllDiseases/?format=json", {})
            .then(function (response) {
                $scope.AllDisease = response.data;
                $scope.load = false;
                $timeout.cancel(TimeOutPromise);

                return response
        }, function (ErrorResponse) {
            console.log(ErrorResponse);

            // If the timer did not timeout, tries to fetch the data again. 
            if(Timeout == false){
                GetEndLinkData();
            }
            });
        };

        GetSearchDisease = function (){
            $http.get(ServerLinkProperty.get() + "/Disease/SearchDiseaseProfile/" + AllDiseaseParameter.getParameter() +"/?format=json", {})
            .then(function (response) {

                $timeout.cancel(TimeOutPromise);
                $scope.AllDisease = response.data; 
                $scope.load = false;
                if(Object.keys(response.data).length == 0){
                    $scope.showPopup();
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

        $scope.showPopup = function() {
            $ionicPopup.show({
                title: 'Application did not detect any results.',
                         buttons: [
                         {
                           text: 'Ok',
                            type: 'button-positive',
                            // Button Function
                            onTap: function(e) {
                        }
                    }
                ]
            });
        };

        
        // decides if it will get all the disease or a searched one


        // go to disease details with the specified id
        $scope.GoToDisease = function(DiseaseID){
            $timeout.cancel(TimeOutPromise);
            $state.go('DiseaseDetails', {ID:DiseaseID});
        }

        $scope.goHome = function(DiseaseID){
            $timeout.cancel(TimeOutPromise);
            $state.go('home', {});
        }

    

    
        // ties up the search modal to this controller
        $ionicModal.fromTemplateUrl('SearchModal.html', {
                scope: $scope,
                animation: 'slide-in-up'
            }).then(function (modal) {
                $scope.SearhModal = modal;    
        });

        // Opens up the Search Modal
        $scope.openSearchModal = function () {
          $scope.SearhModal.show();
        };


        // Hides the Search Modal
        $scope.closeSearchModal = function () {
          $scope.SearhModal.hide();
        };


        // Reloads the page with a search tezt
         $scope.SearchDisease = function(SearchText){
            $scope.SearhModal.hide();
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
            $state.reload();
        }


        // Go back one page
        $scope.goBack = function(){
           if(AllDiseaseParameter.getParameter()=="All"){
              $timeout.cancel(TimeOutPromise);
              $state.go('home',{});
           }else{
              $timeout.cancel(TimeOutPromise);
              window.history.go(-1);
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
            if(AllDiseaseParameter.getParameter()=="All"){
                GetAllDisease();
            }else{
                GetSearchDisease();
            }
        };

        function initialize(){
            StartTimeout();
            GetEndLinkData();
        };


        initialize();

}]);