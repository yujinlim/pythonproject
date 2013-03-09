function VideosController($scope){
		$scope.videos = videos;
		$scope.addVideo = function(){
			$scope.videos.push({
				video_link:$scope.videoLink, 
				published:$scope.videoPublished, 
				ordering:$scope.videoOrdering
				});
			console.log("hahahdalh")}; 
}
