//------------------------------------------------------------------------------  

function notify(data){
 
  $.pnotify({
					pnotify_title: data.title,
					pnotify_type: data.type,
					pnotify_text: data.message
				});
}

//------------------------------------------------------------------------------
  
function updateProgress(target, data)
{
  if(data.type == 'info')
  {
    $( "div.progressbar", $(target).closest('tr')).progressbar(
      "option", "value", parseInt(data.message));
    $( "span.progress", $(target).closest('tr')).text(data.message);
    if (parseInt(data.message) == "100")
    {
      $('button.pause',$(target).closest('tr')).button( "option", "disabled", true );
      pause($('button.pause',$(target).closest('tr')));
    }
  }    
  else
  {
    notify(data);
  }    
}

//------------------------------------------------------------------------------
  
function custom_error(ajaxMethodName)
{
    $.pnotify({
					pnotify_title: "Server error",
					pnotify_type: "error",
					pnotify_text: "There was internal server error while invocing " + 
					                                        ajaxMethodName + " method."
				});
}

//------------------------------------------------------------------------------
  
function getProgress(target)
{
  Dajaxice.gui.getTaskProgress
  (
      function(data)
      {
        updateProgress(target, data); 
      },      
      
      {'name': $('td:eq(0)',$(target).closest('tr')).text()},
      {'error_callback': function(){custom_error("getTaskProgress");}}
   );
}
  
//------------------------------------------------------------------------------      
    
function pause(target)
{
  $(target).button("option", {
    icons: { primary: "ui-icon-play" }
  }).unbind('click').toggleClass( "play pause" ).button(
                                              'option', 'label', 'Start task');
  
  clearInterval($(target).data("timer"));
  
  $( target ).click(function()
  {
    var that = this;
    Dajaxice.gui.startTask
    (
      function(data)
      {
        play(that); 
        notify(data);
      }, 
      {'name':$('td:eq(0)',$(this).closest('tr')).text()},
      {'error_callback': function(){custom_error("startTask");}}
    );
  });    
}

//------------------------------------------------------------------------------
  
function play(target)
{
  $(target).button("option", {
    icons: { primary: "ui-icon-pause" }
  }).unbind('click').toggleClass( "play pause" ).button(
                                            'option', 'label', 'Pause task');
  
  $(target).data("timer", setInterval(
                function(){getProgress(target)}, 4000));
  
  $( target ).click(function()
  {
    var that = this;
    Dajaxice.gui.pauseTask
    (
      function(data)
      {
        pause(that); 
        notify(data);
      }, 
      {'name':$('td:eq(0)',$(this).closest('tr')).text()},
      {'error_callback': function(){custom_error("pauseTask");}}
    );
  });    
}

//------------------------------------------------------------------------------
  
function stop(target)
{
  $('button:eq(0)',$(target).closest('tr')).button( "option", "disabled", false );
  pause($('button:eq(0)',$(target).closest('tr')));
  updateProgress(target, {type: "info", message:0});
}

//------------------------------------------------------------------------------
  
function trash(target)
{
  stop(target);
  $(target).closest('tr').remove();
}

//------------------------------------------------------------------------------
    
$(function() {

	$( "button.play" ).button({
          icons: {
              primary: "ui-icon-play"
          },
          text: false
      });
      
  $( "button.pause" ).button({
          icons: {
              primary: "ui-icon-pause"
          },
          text: false
  });     
  
	$( "button.stop" ).button({
          icons: {
              primary: "ui-icon-stop"
          },
          text: false
      });
      
	$( "button.trash" ).button({
          icons: {
              primary: "ui-icon-trash"
          },
          text: false
      });
      
  $( "button.settings" ).button({
          icons: {
              primary: "ui-icon-gear"
          },
          text: false
      });
      
  $( "button.results" ).button({
          icons: {
              primary: "ui-icon-disk"
          },
          text: false
      });

$("div.settings").dialog({ autoOpen: false,  modal: true, minWidth: 500, buttons: {
				"Apply": function() {
					$( this ).dialog( "close" );
				},
				Cancel: function() {
					$( this ).dialog( "close" );
				},
			 "Advanced...": function() {
					$( this ).dialog( "close" );
				}
			}, open: function(event, ui) { $('#descriptions').spinner({ min: 0, max: 1000, step: 10 });
$('#alignments').spinner({ min: 0, max: 1000, step: 10 });
$('#hitlist_size').spinner({ min: 0, max: 100});
$("#matrix_name").selectmenu({style:"dropdown",width:120});
}});
$( "div#program" ).buttonset();
$( "div#flavour" ).buttonset();
$( "div#filter" ).buttonset();
$( "div#other_dbs > button" ).button();
$(".multiselect").multiselect({dividerLocation: 0.5});
$("#magablast").checkbox();


		$( "#slider-range" ).slider({
			step: 0.1,
			min: 0.0,
			max: 10.0,
			value: 10.0,
			slide: function( event, ui ) {
				$( "#expect" ).val( ui.value );
			}
		});
		$( "#expect" ).val( $( "#slider-range" ).slider( "value" ) );

$( "button.settings" ).click(function()
  {
    var that = this;
    var modalId = ($(that).text())? "#" + $(that).text() + "-settings" : "#settings";
    $(modalId).length? $.noop : modalId = "#settings"; 
		$( modalId ).dialog('open');		
  });
  
$( "button.results" ).click(function()
  {
    var that = this;
    var nam = $('td:eq(0)',$(this).closest('tr')).text();
    window.open('/results?name=' + nam,'_blank');
  });  
  
  $( "button.play" ).click(function()
  {
    var that = this;
    Dajaxice.gui.startTask
    (
      function(data)
      {
        play(that); 
        notify(data);
      }, 
      {'name':$('td:eq(0)',$(this).closest('tr')).text()},
      {'error_callback': function(){custom_error("startTask");}}
    );
  });
  
  $( "button.pause" ).click(function()
  {
    var that = this;
    Dajaxice.gui.pauseTask
    (
      function(data)
      {
        pause(that); 
        notify(data);
      }, 
      {'name':$('td:eq(0)',$(this).closest('tr')).text()},
      {'error_callback': function(){custom_error("pauseTask");}}
    );
  })
  
  $( "button.pause" ).each
  (
    function()
    {
      var that = this;
      $(that).data
      (
        "timer", 
        setInterval
        (
          function()
          {
            getProgress(that);
          }, 
          4000
        )
      );
    }
  );
  
  $( "button.stop" ).click(function()
  {
    var that = this;
    Dajaxice.gui.stopTask
    (
      function(data)
      {
        stop(that);
        notify(data);
      }, 
      {'name':$('td:eq(0)',$(this).closest('tr')).text()},
      {'error_callback': function(){custom_error("stopTask");}}
    );
  });
  
  $( "button.trash" ).click(function() 
  {
    var that = this;
    Dajaxice.gui.deleteTask
    (
      function(data)
      {
        trash(that);
        notify(data);
      }, 
      {'name':$('td:eq(0)',$(this).closest('tr')).text()},
      {'error_callback': function(){custom_error("deleteTask");}}
    );
  });
  
  $( "div.progressbar" ).each
  (

    function()
    {
      var that = this;
      $(that).progressbar({value: parseInt($("span.progress",$(that).closest('tr')).text())	});
    }
  );
                   
});
  
//------------------------------------------------------------------------------  
