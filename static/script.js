$( document ).ready(function() {

	// Hide the hidden image thats there for 
	$("#hiddenImage").hide();

	// Display and remove header on scroll
    var position = $(window).scrollTop(); 
	$(window).scroll(function() {
	    var scroll = $(window).scrollTop();
	    if(scroll > position) {
	        $("#navbar").fadeOut(200);
	    } else {
	        $("#navbar").fadeIn(200);
	    }
	    position = scroll;
	});

});