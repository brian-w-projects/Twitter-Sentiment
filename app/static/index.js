(function($, window, document){

    $("#submit").click(function() {
            setTimeout(function(){disable();}, 0);
        }
    );

    function disable(){
        $("#submit").text("LOADING...").attr('disabled', true);
    }

}(window.jQuery, window, document));