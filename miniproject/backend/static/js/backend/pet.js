function VideosController($scope){
		$scope.videos = []; 
		$scope.addVideo = function(){
			$scope.videos.push({
				video_link:$scope.videoLink, 
				published:$scope.videoPublished,
                ordering:$scope.videoOrdering
				});
            console.log("done")};
        
        $scope.changeInsertPetView = function(which){
                if (which == "pet"){
                    $scope.insertPet = false;
                    console.log("pet did it");
                }
                else
                {
                    $scope.insertPet = true;
                    console.log("video did it");
                }
                console.log("did it");
        };
}

