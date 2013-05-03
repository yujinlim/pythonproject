app.constant('apiUrl', 'dsadsa');

app.factory('petService', function($http, apiUrl, $rootScope, YouTubeChannel){
        var localEvents = {
            VIDEOS_LOADED: "petservice:videosloaded"
        };
        return {
            events: localEvents,
            load: function(){
                if (YouTubeChannel != "" && YouTubeChannel != null)
                {
                    var url = "http://gdata.youtube.com/feeds/api/users/" + YouTubeChannel + "/uploads?alt=json-in-script&callback=JSON_CALLBACK"
                    $http.jsonp(url).success(function(data){
                        var videos = data.feed.entry;
                        angular.forEach(videos, function(video){
                           video.isSelected = false; 
                        });
                        $rootScope.$broadcast( localEvents.VIDEOS_LOADED,  videos);
                    });
                }
            }
        }
        
});

app.controller('VideosController', function($scope, $rootScope, $dialog, petService, $injector){
        $scope.dateOptions = {format: 'yyyy-mm-dd'};
		$scope.videos = [];
        $scope.indexes = [];
        var oldVideos = $injector.get("PetVideos");
		$scope.addVideo = function(video){
            if (video != "" && video != null)
            {
                //var url = video.link[0].href;
                var title = video.title.$t
                var videoId = video.id.$t.split('/').reverse()[0];
                var url = "http://www.youtube.com/embed/" + videoId;
                video.isSelected = true;
                $scope.videos.push({
                    title: title,
                    video_link:url, 
                    published:true
				});
            }
            else
            {
                $scope.videos.push({
                    title: $scope.title,
                    video_link:$scope.videoLink, 
                    published:$scope.videoPublished
				});
            }
            console.log("done")
            };
        
        if (oldVideos != "" && oldVideos != null)
        {
            oldVideos = JSON.parse(oldVideos);
            angular.forEach(oldVideos, function(video_object){
                    $scope.videos.push({
                        title: video_object.title,
                        video_id: video_object.id,
                        video_link: video_object.video_link,
                        published: video_object.published
                    });
            });
        }
        
        $scope.removeVideo = function(video, index){
            $scope.videos.splice(index,1);
            angular.forEach($scope.youtubeVideos, function(youtubeVideo){
                if (youtubeVideo.link[0].href == video.video_link)
                {
                    youtubeVideo.isSelected = false;
                }
            })
        };
        
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
        
        petService.load();
        $scope.$on( petService.events.VIDEOS_LOADED, function(e, videos){
            $scope.youtubeVideos = videos;
        });
        
        
        
        $scope.watchVideo =  function(videoid){
            var template = '<iframe id="youtubeVideo" type="text/html" width="640" height="390" src="http://www.youtube.com/embed/'+ videoid + '?autoplay=1"frameborder="0"/>'
            $scope.opts.template = template;
            var d = $dialog.dialog($scope.opts);
            d.open();
        };
        
        $scope.close = function()
        {
            $scope.watchYouTubeVideoLink = "";
            $scope.shouldBeOpen = false;
        }
        
        $scope.opts = {
            backdropFade: true,
            dialogFade:true,
            backdrop: true,
            keyboard: true,
            backdropClick: true,
            dialogClass: 'modal modal-video'
        };
}); 


app.controller('youtubeVideoController', function($scope){
    $scope.watchYouTubeVideo = [];
        $scope.watchVideo =  function(url){
            $scope.watchYouTubeVideo.link = url;
            $scope.watchYouTubeVideo.show = true;
        };
});

app.directive('bDatepicker', function(){
    return {
      require: '?ngModel',
      restrict: 'A',
      link: function($scope, element, attrs, controller) {
        var updateModel;
        updateModel = function(ev) {
          element.datepicker('hide');
          element.blur();
          return $scope.$apply(function() {
            return controller.$setViewValue(ev.date);
          });
        };
        if (controller != null) {
          controller.$render = function() {
            element.datepicker().data().datepicker.date = controller.$viewValue;
            element.datepicker('setValue');
            element.datepicker('update');
            return controller.$viewValue;
          };
        }
        return attrs.$observe('bDatepicker', function(value) {
          var options;
          options = {};
          if (angular.isObject(value)) {
            options = value;
          }
          if (typeof(value) === "string" && value.length > 0) {
            options = angular.fromJson(value);
          }
          return element.datepicker(options).on('changeDate', updateModel);
        });
      }
    };
});


