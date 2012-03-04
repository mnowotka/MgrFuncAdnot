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
  pause($('button.pause',$(target).closest('tr')));
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
            console.log("ping");
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
      
  $( "div.progressbar" ).progressbar({
		value: $(this).text()
	});                    
});
  
//------------------------------------------------------------------------------  
