/*
 * GLOBAL SCRIPTS
 */

// Panel stack stuff (to be recoded)

function loadPanel(geturl, element, target){

  target.addClass("panelsheet-stacked");
  window.scroll(0,0);
  
  // Load the content from external file
  $.ajax({
     url: geturl,
     data: {},
     success: function (data) {
       $childPanel = $(data).find(element);
       target.children(".panelsheet-header").after($childPanel);
       target.children(".panelsheet-header").find("h1").bind("click", function(e){
         e.stopPropagation();
         unloadPanel(target);
       });
     },
     dataType: 'html'
  });
  
}

function unloadPanel(target){
  console.log(target);
  target.removeClass("panelsheet-stacked");
  target.children(".panelsheet-header").find("h1").unbind();
  target.children(".panelsheet").remove();
}


// PAGE INIT

$(document).ready(function() {
  
  /* INIT POLYPAGE */
  $('body').polypage();
  
  /* INIT TOOLTIPS */
  $("[rel=tooltip]").tooltip();
  
  /* INIT POPOVERS */
  $("[rel=popover]").popover({
    html: "true",
    animation: "true",
    trigger: "click",
    delay: { show: 0, hide: 300 }
  });
  
  /* INIT LOADING BUTTONS */
  $(".btn[data-loading-text]").click(function(e){
    $(this).button('loading');
  });
  
  /* SHOW ADVANCED OPTIONS */
  $(".adv-options-toggle").click( function() {
    $(".advanced-options").toggle(200);
  });
  
  /* LOADING EXEMPLES */
  $("#btn-loading-view").click(function() {
    $(".panelsheet").toggleClass("loading-view");
  });

  $("#btn-loading-content").click(function() {
    $(".panelsheet").toggleClass("loading-content");
  });

});

