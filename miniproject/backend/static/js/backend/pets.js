var paginator;
$(window).ready(function(){
	paginator = new Zest.Paginator({},"#pet-entries-list");
    var bootstrap = new Zest.Bootstrap(),
        paginatorMessages = $('#pet-entries-messages');

	paginator.on("beforeLoad",function(){
        paginator.box.empty().addClass("ajax-loading");
    });
    paginator.on("dataLoaded",function(response, success){
       paginator.box.removeClass("ajax-loading");
       
       bootstrap.putMessagesIntoBox(response.messages, paginatorMessages);
    });
    paginator.loadData();
})
