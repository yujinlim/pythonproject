app.factory('petRandomVideoService', function($http, $rootScope, randomUrl, nextUrl, detailUrl){
        var localEvents = {
            NEW_VIDEO_LOADED: "petRandomVideo:new_video",
            NEXT_VIDEO_LOADED: "petRandomVideo:next_new_video",
            GET_DETAILS: "petRandomVideo:get_details"
        };
        return {
            events: localEvents,
            load: function(){
                var url = randomUrl;
                $http.get(url).success(function(data){
                    $rootScope.$broadcast( localEvents.NEW_VIDEO_LOADED,  data.data);
                });
            },
            getNext: function(){
                var url = nextUrl;
                $http.get(url).success(function(data){
                    $rootScope.$broadcast( localEvents.NEW_VIDEO_LOADED,  data.data);
                });
            },
            getDetail: function(){
                var url = detailUrl;
                $http.get(url).success(function(data){
                    $rootScope.$broadcast( localEvents.GET_DETAILS,  data.data);
                });
            }
        }
        
});

app.controller('petRandomVideoController', function($scope, petRandomVideoService){
        petRandomVideoService.load();
        $scope.$on(petRandomVideoService.events.NEW_VIDEO_LOADED, function(e, video){
                petRandomVideoService.getDetail();
                if (video.video.video_link.match('watch') != "" && video.video.video_link.match('watch') != null)
                {
                    video.video.video_link = "http://www.youtube.com/embed/" + video.video.video_link.split('v=').reverse()[0];
                }
                $scope.videos = video.video;
        });
        
        $scope.nextVideo = function(){
            petRandomVideoService.getNext();
            petRandomVideoService.getDetail();
        };
        
        
        $scope.$on(petRandomVideoService.events.GET_DETAILS, function(e, data){
            $scope.panes = [
                { title: "Details", content:data.pet }
            ];
        });
});
