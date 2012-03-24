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

function gatherBLASTSettings()
{
  var ret = {};
  var form = $("form.taskForm");
  ret["web"] = $("input:radio[name=web]:checked", form).val();
  ret["blast"] = $("input:radio[name=blast]:checked", form).val();
  ret["db"] = $("select#dbs", form).val();
  ret["ndesc"] = $("input#descriptions", form).val();
  ret["nalign"] = $("input#alignments", form).val();
  ret["nhits"] = $("input#hitlist_size", form).val();
  ret["cutoff"] = $("input#expect", form).val();
  ret["matrix"] = $("select#matrix_name", form).val();
  ret["filter"] = $("input:radio[name=filter]:checked", form).val();
  ret["megablast"] = $("input[name=megablast]", form).is(":checked");
  return ret;
}

//------------------------------------------------------------------------------

function decorateForm()
{
$('#descriptions').spinner({ min: 0, max: 1000, step: 10 });
$('#alignments').spinner({ min: 0, max: 1000, step: 10 });
$('#hitlist_size').spinner({ min: 0, max: 100});
$("#matrix_name").selectmenu({style:"dropdown",width:120});
$( "div#program" ).buttonset();
$( "div#flavour" ).buttonset();
$( "div#filter" ).buttonset();
$( "div#other_dbs > button" ).button();
$(".multiselect").multiselect({dividerLocation: 0.5});
$("#megablast").checkbox();


		$( "#slider-range" ).slider({
			step: 0.1,
			min: 0.0,
			max: 10.0,
			value: $("#expect").val(),
			slide: function( event, ui ) {
				$( "#expect" ).val( ui.value );
			}
		});
		$( "#expect" ).val( $( "#slider-range" ).slider( "value" ) );
}

//------------------------------------------------------------------------------

function setTaskInitialParams(data)
{
  if(data.type == 'info')
  {
    msg = data.message;
    var form = $("form.taskForm");
    $("input#" + msg["web"], form).attr('checked', true);
    $("input#" + msg["blast"], form).prop('checked', true);
    $("input#" + msg["filter"], form).prop('checked', true);
    $.each(msg["db"], function(index, value) {
      $("select option[value=" + value + "]", form).prop('selected', true); 
    });
    $("select#dbs", form).val(msg["db"]);
    $("input#descriptions", form).val(parseInt(msg["ndesc"]));
    $("input#alignments", form).val(parseInt(msg["nalign"]));
    $("input#hitlist_size", form).val(parseInt(msg["nhits"]));
    $("input#expect", form).val(parseFloat(msg["cutoff"]));
    $("select#matrix_name option[value=" + msg["matrix"] + "]", form).prop('selected', true);
    $("input[name=megablast]", form).prop('checked', msg["megablast"]);
  }    
  else
  {
    notify(data);
  }
  decorateForm(); 
}

//------------------------------------------------------------------------------

function getTaskParams(taskName)
{
    Dajaxice.gui.getTaskParams
    (
      function(data)
      {
        setTaskInitialParams(data);
      }, 
      {'name':taskName},
      {'error_callback': function(){custom_error("getTaskParams");}}
    );
}

//------------------------------------------------------------------------------

function submitBLASTSettingsForm(taskName)
{
      Dajaxice.gui.setTaskParams
      (
        function(data)
        {
          notify(data);
        }, 
        {'name':taskName, 'params' : gatherBLASTSettings()},
        {'error_callback': function(){custom_error("setTaskParams");}}
      );
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

$("div.settings").dialog({ autoOpen: false,  modal: true, minWidth: 500});

$( "button.settings" ).click(function()
  {
    var that = this;
    var modalId = ($(that).text())? "#" + $(that).text() + "-settings" : "#settings";
    $(modalId).length? $.noop : modalId = "#settings";
    if(modalId=="#Blst-settings")
    {
       $( modalId ).dialog("option", "buttons", {
				"Apply": function() {
					submitBLASTSettingsForm($(this).data("taskName")); $( this ).dialog( "close" );
				},
				Cancel: function() {
					$( this ).dialog( "close" );
				},
			 "Advanced...": function() {
					$( this ).dialog( "close" );
				}
			});
			
			$( modalId ).dialog("option", "open", function(event, ui) { 
getTaskParams($(this).data("taskName"));
});

    			$( modalId ).dialog("option", "close", function(event, ui) { 
$(".multiselect").multiselect("destroy");
});

    }
    
		$( modalId ).data("taskName", $('td:eq(0)',$(that).closest('tr')).text()).dialog('open');		
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

 $("form.taskForm").submit(
    function(event){
      event.preventDefault();
    }
 );   
  
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
