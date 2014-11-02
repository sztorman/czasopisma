jQuery(document).ready(function($) {
  
  function gridShow(){
  $("#main_conteiner").gridPreview({
      'columns':12,
      'columnClass': 'grid_1',
      'line': 20,
      'modul': 2,
      'topOffset': 0,
      'leftOffset': 0,
      'toggleGrid': 'g', 
      'toggleZindex': 'f',
      'showAtStart': false,
      'showOnTop': true
    });
  }
    gridShow();

  $(window).resize(function(){
    $("#gridPreviewHolder").remove();
    gridShow();
  });

  // Start your functions here

  $("#header_search input").focusin(function(){
    // $(".input_holder").animate({"width":"100%"}, function(){
      $("#header_submit").fadeIn();
    // });
  });
  $("#header_search input").focusout(function(){
    if($(this).val().length ==0){
      $("#header_submit").fadeOut();
      // $(".input_holder").animate({"width":"50%"});
    }
  });

    $(".download_icon a").click(function(e){
      e.preventDefault();
      if($("#downlaod_box").hasClass("opened")){
        $("#downlaod_box").slideUp();
        $("#downlaod_box").removeClass("opened");
        $(".download_icon").removeClass("active");
      }
      else{
        $("#downlaod_box").slideDown();
        $("#downlaod_box").addClass("opened");
        $(".download_icon").addClass("active");
      }
    })


    $(".share_icon").click(function(e){
      e.preventDefault();
      if($(".share_menu").hasClass("opened")){
        $(".share_menu").animate({"width": 0 });
        $(".share_menu").removeClass("opened");
      }
      else{
        $(".share_menu").width("auto");
        var menuShareWidth =  $(".share_menu").width();
        $(".share_menu").width(0);
        $(".share_menu").animate({"width": menuShareWidth });
        $(".share_menu").addClass("opened");
      }
    })

  
    $(".medium_thumbs_cont .thumb_wrap h2").dotdotdot({ellipsis : '…',});
    
    $(window).load(function(){
      if($(".thumb_wrap.active").length>0){
        var scrollToActive = $(".thumb_wrap.active").offset().top;
        var scrollToActive = scrollToActive - $("#top_panel").height() - 30;
        $("body, html").animate({scrollTop: scrollToActive})
      }
    });

    // list of names
    if($("#results_names ul li").length<12 && $("#results_names").length>0 ){
      $("#results_names ul").removeClass("columnised");
      $(".vertical_border_1, .vertical_border_2").remove();
    }

  // Drag zoomable img 

  var mouseDown = false;
  var startX;
  var startY;
  var endY;
  var endX;
  var actualPosX = 0;
  var actualPosY = 0;
  var newPosX;
  var newPosY;
  $("#zoom_mask img").mousedown(function(e){
    e.preventDefault();
    mouseDown = true;
    startX = e.pageX;
    startY = e.pageY;
    actualPosX = $("#zoom_mask img").offset().left;
    actualPosY = $("#zoom_mask img").offset().top;
  });

  $("#zoom_mask img").mousemove(function(e){
    if(mouseDown){
       e.preventDefault();
      moveX = e.pageX;
      moveY = e.pageY; 
      newPosX = startX - moveX; 
      newPosY = startY - moveY;
      $("#zoom_mask img").addClass("moved");
      $("#zoom_mask img").css({"left": actualPosX - newPosX });
      $("#zoom_mask img").css({"top": actualPosY - newPosY });
      // actualPosX = $("#zoom_img_conteiner").offset().left;
      // actualPosY = $("#zoom_img_conteiner").offset().top;
    }
  });

  $("#zoom_mask img").mouseup(function(e){
    e.preventDefault();
    mouseDown = false;
    endX = e.pageX;
    endY = e.pageY;
    actualPosX = $("#zoom_mask img").offset().left;
    actualPosY = $("#zoom_mask img").offset().top;

  });

   $("#zoom_mask img").mouseleave(function(e){
     e.preventDefault();
    mouseDown = false;
    actualPosX = $("#zoom_mask img").offset().left;
    actualPosY = $("#zoom_mask img").offset().top;

  });
  var panelHidden = false;

   $("#zoom_mask").click(function(){
    if(startX == endX && startY == endY){
      if(panelHidden){
        panelHidden = false;
        $("#top_panel").animate({"top": "0"});
        $("#zoom_box").animate({"bottom": "0"});
      }
      else{
        $("#top_panel").animate({"top": - $("#top_panel").height() });
        $("#zoom_box").animate({"bottom": -$("#zoom_box").height()-1 });
        panelHidden = true;
      }
    }
   });


   //initial zoom to middle
   var minSize = 200;
   var maxSize = parseFloat($("#zoom_mask").attr("attr-max"));
   var totalRange = maxSize - minSize;
   var initSize = minSize + (totalRange/2);
   var zoomState = 5;
   var zoomMax = 10;
   var zoomCenterX = $(window).width()/2;
   var zoomCenterY = $(window).height()/2;
   var yScaleIncr=0;
   var xScaleIncr=0;
   var scaleInit=0;


    function zoomControl(){
    	if ($(".slider_dot").length > 0) {
      var sliderDotPos = $(".slider_dot").offset().left;
      var lineX = $(".slider_real_base").offset().left;
      var sliderDotPos = sliderDotPos - lineX;
      var sliderDotPos = sliderDotPos/$(".slider_real_base").width();
      // console.log(sliderDotPos);
      zoomState = Math.round(sliderDotPos*10);
      var sizeDifference = totalRange * sliderDotPos;
      var currentSize = minSize + sizeDifference;
      var oldSize;
      if($(".vertical img").length>0){
        oldSize = $(".vertical img").height();
      };
      if($(".horisontal img").length>0){
        oldSize = $(".horisontal img").width();
      };
      var sizeRealDif = currentSize-oldSize;
      var scaleInit = sizeRealDif/oldSize;
      // console.log(scaleInit);
      $(".vertical img").height(currentSize);
      $(".horisontal img").width(currentSize);
      actualPosX = $("#zoom_mask img").offset().left;
      actualPosY = $("#zoom_mask img").offset().top;
      // console.log(actualPosX);
      // console.log(actualPosY);
      yScaleIncr = zoomCenterY - actualPosY;
      yScaleIncr = yScaleIncr * scaleInit;
      xScaleIncr = zoomCenterX - actualPosX;
      xScaleIncr = xScaleIncr * scaleInit;
      // ;
      $("#zoom_mask img").css({
        "top": actualPosY - yScaleIncr,
        "left": actualPosX - xScaleIncr,
      })
      console.log()
    } }
    zoomControl();
    $(window).load(function(){
      $("#zoom_mask img").addClass("moved");
      var windHeight = $(window).height();
      var windWidth = $(window).width();
      var imgHeight = $("#zoom_mask img").height();
      var imgWidth = $("#zoom_mask img").width();
      actualPosX = (windHeight/2) - (imgHeight/2);
      actualPosY = (windWidth/2) - (imgWidth/2);
      $("#zoom_mask img").css({"top": actualPosX});
      $("#zoom_mask img").css({"left": actualPosY});
      zoomControl();
    });
  

    // Slider clicking/dragging
    var sliderDown;
    function sliderMoving(e){
      var lineX = $(".slider_real_base").offset().left;
      var downX = e.pageX;
      var realDif = downX - lineX;
      var realDif = Math.round(realDif/$(".slider_real_base").width() * 100);
      if(realDif<0){
       var realDif = 0;
      }
      if(realDif>100){
       var realDif = 100;
      }
      $(".slider_dot").css({"left": realDif+"%"});
      zoomControl();
    }

    $(".zoom_line").mousedown(function(e){
      sliderDown = true;
      e.preventDefault();
      sliderMoving(e);
    });

    $(".zoom_line").mousemove(function(e){
      if(sliderDown){
        sliderDown = true;
        e.preventDefault();
        sliderMoving(e);
      }
    })

    $(".zoom_line").mouseup(function(e){
      sliderDown = false;
      e.preventDefault();
      // sliderMoving(e);
    });
    $(".zoom_line").mouseleave(function(e){
      sliderDown = false;
      e.preventDefault();
      // sliderMoving(e);
    });

    function zoomIn(){
      if(zoomState < zoomMax){
        zoomState++;
        zoomStep = 100/ zoomMax;
        actualState = zoomState * zoomStep;
        $(".slider_dot").css({"left": actualState+"%"});
        zoomControl();
      }
    }
    function zoomOut(){
      if(zoomState > 0){
        zoomState--;
        zoomStep = 100/ zoomMax;
        actualState = zoomState * zoomStep;
        $(".slider_dot").css({"left": actualState+"%"});
        zoomControl();
      }
    }

    // mouse zoom 
    $('#zoom_mask').bind('mousewheel', function(event, delta) {
      // console.log(delta)
      if(delta>0 ){
        zoomIn();
      } 
      if(delta<0){
        zoomOut();
      } 
    })


    $("#zoom_mask img").mousemove(function(e){
      zoomCenterX = e.pageX;
      zoomCenterY = e.pageY;
    });

    $("#zoom_mask img").mouseleave(function(e){
      zoomCenterX = $("#zoom_mask img").offset().left + ($("#zoom_mask img").width()/2);
      zoomCenterY = $("#zoom_mask img").offset().top + ($("#zoom_mask img").height()/2);
    });

    $(".zoomin").click(function(e){
      e.preventDefault();
      zoomIn();
    });
    $(".zoomout").click(function(e){
      e.preventDefault();
      zoomOut();
    })



  

});
