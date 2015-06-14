$( document ).ready(function() {
    $(function() {
        $( "#slider" ).slider({
            value: null,
            min: 0,
            max: 500,
            step: 50,
            slide: function( event, ui ) {
                $( "#amount" ).val( "$" + ui.value );
            }
        });
        $( "#amount" ).val( "$" + $( "#slider" ).slider( "value" ) );
    });
});