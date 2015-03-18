/* INIT SLIDING PANELS */

SMartSlidePanel = function(target){ 
  /* target = anchor or jquery object */
  target = $(target);
  target.addClass('current');
  target.siblings('.slidingpanels-item').removeClass("current");
  window.scrollTo(0,0);
}

/** AUTO BIND EVENTS **/

$(document).ready(function(){
  $("[data-slidingpanels-event='click']").bind("click", function(e){
    e.preventDefault();
    var target = $(this).attr('href');
    SMartSlidePanel(target);
  });
  
  $("[data-slidingpanels-event='submit']").bind("submit", function(e){
    e.preventDefault();
    var target = $(this).attr('action');
    SMartSlidePanel(target);
  });
});
