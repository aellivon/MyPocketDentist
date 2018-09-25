app.controller('HomeController', [
        "$scope","$ionicModal","$state" , "$stateParams","$http",
        "AllDiseaseParameter","HypothesisParameter","ExaminingAnswers",
        "$ionicPopup",
    	function($scope,$ionicModal, $state, $stateParams,$http,
                AllDiseaseParameter,HypothesisParameter,ExaminingAnswers,
                $ionicPopup)
    {

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
        
        // The StartExamine function transfers you the examine page
 		$scope.StartExamine = function(){
            if(ExaminingAnswers.getExaminingProperty() == "start"){
                $state.go('examining', {});
            }else{
                $ionicPopup.show({
                    title: 'Would you like to resume the previous examination?',
                        buttons: [
                          {
                                text: 'Yes',
                                type: 'button-positive',
                                // Button Function
                                    onTap: function(e) {
                                        $state.go('examining', {});
                                        HypothesisParameter.setExaminingProperty("0");
                                    }
                            },
                            {
                                text: 'No',
                                type: 'button-positive',
                                // Button Function
                                    onTap: function(e) {
                                        ExaminingAnswers.setExaminingProperty("start");
                                        HypothesisParameter.setExaminingProperty("0");
                                        $state.go('examining', {});
                                    }
                            }
                        ]
                    });
            }
            
        }

        function jumpContainer(id){
            angular.element(document.querySelector(id))[0].style.position = "relative";

            function cPosition(pos){
                angular.element(document.querySelector(id))[0].style.bottom = pos + "px";
            }
            function popPosition(p){
                var g = p.shift();
                cPosition(g);
                if(p.length > 0){
                    setTimeout(function(){
                        popPosition(p);
                    }, 50);
                }
            }
            var pattern = new Array(0,0,0,0,0,1,2,3,3,2,1,0,1,2,3,3,2,1,0);
            pattern = pattern.concat(pattern.concat(pattern));
            popPosition(pattern);
        }

        // This function transfers you to All DiseaseList with the paremeter "All"
        $scope.GoToDisease = function(){
            AllDiseaseParameter.setParameter('All');
            $state.go('AllDiseaseList', {});
        }

        // This function transfers  you to All  Disease List with the paremeter SearchText
        //      from the modal text.
        $scope.SearchDisease = function(SearchText){
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
            $scope.SearchModal.hide();
            
            $state.go('AllDiseaseList', {});
        }
        jumpContainer(".ion-information-circled");
}]);