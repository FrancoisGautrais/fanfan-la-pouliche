/* ========================================================================= */
/*	Preloader
/* ========================================================================= */

jQuery(window).load(function(){

	$("#preloader").fadeOut("slow");

});



$(document).ready(function(){

	/* ========================================================================= */
	/*	Menu item highlighting
	/* ========================================================================= */

	jQuery('#nav').singlePageNav({
		offset: jQuery('#nav').outerHeight(),
		filter: ':not(.external)',
		speed: 1200,
		currentClass: 'current',
		easing: 'easeInOutExpo',
		updateHash: true,
		beforeStart: function() {
			console.log('begin scrolling');
		},
		onComplete: function() {
			console.log('done scrolling');
		}
	});
	
    $(window).scroll(function () {
        if ($(window).scrollTop() > 400) {
            $("#navigation").css("background-color","#000");
        } else {
            $("#navigation").css("background-color","rgba(16, 22, 54, 0.2)");
        }
    });
	
	/* ========================================================================= */
	/*	Fix Slider Height
	/* ========================================================================= */	

	var slideHeight = $(window).height();
	
	$('.elt-slider, .carousel.slide, .carousel-inner, .carousel-inner .item').css('height',slideHeight);

	$(window).resize(function(){'use strict',
		$('.elt-slider, .carousel.slide, .carousel-inner, .carousel-inner .item').css('height',slideHeight);
	});
	var children = $("#nav > li > a");
	children.each((i, e) => $(e).removeClass("current"))
	children.first().addClass("current")
	
	
	/* ========================================================================= */
	/*	Portfolio Filtering
	/* ========================================================================= */	
	
	
    // portfolio filtering

    $(".project-wrapper").mixItUp();
	
	
	$(".fancybox").fancybox({
		padding: 0,

		openEffect : 'elastic',
		openSpeed  : 650,

		closeEffect : 'elastic',
		closeSpeed  : 550,

		closeClick : true,
	});
	
	/* ========================================================================= */
	/*	Parallax
	/* ========================================================================= */	
	
	$('#facts').parallax("50%", 0.3);
	
	/* ========================================================================= */
	/*	Timer count
	/* ========================================================================= */

	"use strict";
    $(".number-counters").appear(function () {
        $(".number-counters [data-to]").each(function () {
            var e = $(this).attr("data-to");
            $(this).delay(6e3).countTo({
                from: 50,
                to: e,
                speed: 3e3,
                refreshInterval: 50
            })
        })
    });
	
	/* ========================================================================= */
	/*	Back to Top
	/* ========================================================================= */
	
	
    $(window).scroll(function () {
        if ($(window).scrollTop() > 400) {
            $("#back-top").fadeIn(200)
        } else {
            $("#back-top").fadeOut(200)
        }
    });
    $("#back-top").click(function () {
        $("html, body").stop().animate({
            scrollTop: 0
        }, 1500, "easeInOutExpo")
    });

    viewer.init();


	
});
const regex = /^\w+@\w+(\.\w+)+$/gm;

function mail_ok(){
    $("#mail-error").hide()
    $("#mail-ok").show();
}

function send_mail(){
    var data = {
        name : $("#contact-name").val(),
        email : $("#contact-email").val(),
        message : $("#contact-message").val(),
    }
    var errors = []
    if(data.name.length<2){
        errors.push("Le nom est incorrecte")
    }
    if(regex.exec(data.email)==null){
        errors.push("L'adresse email est incorrecte ")
    }
    if(data.message.length<1){
        errors.push("Le message est incorrect")
    }
    if(errors.length){
        var text='<ul>';
        for(var i =0; i< errors.length; i++) text+='<li>'+errors[i]+'</li>'
        text+='</ul>'
        var elem = $("#mail-error")
        elem.empty()
        elem.append($(text))
        elem.show()
        $("#mail-ok").hide()
        return
    }
    else{
        console.log(data)
        $.ajax({
          type: "POST",
          url: "/contact",
          data: JSON.stringify(data),
          success: mail_ok,
          headers: {
            "Content-Type" : "application/json"
          },
          dataType: "json"
        });
    }
}

function show_image(id){
    var elem = $('<a class="image fancy-image" href="/image/'+id+'/l">LA</a>')
    $("body").append(elem)
    $(".fancy-image").fancybox({
		'transitionIn'	:	'elastic',
		'transitionOut'	:	'elastic',
		'speedIn'		:	600,
		'speedOut'		:	200,
		'overlayShow'	:	true
	});
}

