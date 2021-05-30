function setCustomValidation(obj, appendix) {
    if (obj.value == '' && obj.localName == "select") {
        obj.setCustomValidity('Izvēlieties ' + appendix + '.');
    }
    else if (obj.value == '' && obj.localName == "input") {
        obj.setCustomValidity('Ievadiet ' + appendix + '.');
    }
    else {
        obj.setCustomValidity('');

        return false;
    }

    return true;
}

function fillDeploymentNames(venue_id, system_type) {
    $.ajax({
        url:"analysis_type", //the page containing python script
        type: "POST",
        dataType: 'html',
        data: {venue: venue_id, system: system_type},
        success: function (result) {
            //
        },
    }).fail(function (reply) {
        $('#rerenderDeploymentNames').html(reply.responseText);
    }).done(function (reply) {
        $('#rerenderDeploymentNames').html(reply);
    });
}

function checkOffset(){
  var typeSelection = document.getElementById("type");
  var selectedType = typeSelection.value;

  var venueSelection = document.getElementById("deploymentVenue");
  var selectedVenue = venueSelection.value;

  if (selectedType != "" && selectedVenue != ""){
      fillDeploymentNames(selectedVenue, selectedType);
  }

  if (selectedType == "Decawave") {
      $(".offsetBlock").each(function(index, element){
            $(".offsetBlock > input, select").prop('required', true);
            $(".offsetBlock > input").prop('oninvalid', "setCustomValiditation(this, 'nobīdi')");
            $(".offsetBlock > select").prop('oninvalid', "setCustomValiditation(this, 'zonu vai zonas')");
            $(element).css("display" , "block");
      });
  } else {
      $(".offsetBlock").each(function(index, element){
            $(".offsetBlock > input, select").prop('required', false);
            $(".offsetBlock > input, select").prop('oninvalid', null);
            $(element).css("display" , "none");
      });
  }
}

function selectAllZones () {
    $('#zoneId option').prop('selected', true);
    $('select.chosen-select').trigger('chosen:updated');
}

function deselectAllZones () {
    $('#zoneId option').prop('selected', false);
    $('select.chosen-select').trigger('chosen:updated');
}

$(".chosen-select").chosen({
      no_results_text: "Nav pievienotas zonas!",
      placeholder_text_single: ".",
  });

$(function() {
    $("input.datepicker").datepicker();

    $("input.timepicker").timepicker({
        showMeridian: false,
        timeFormat: 'HH:mm:ss',
        interval: 5,
    });
} );

$.datepicker.setDefaults( $.datepicker.regional[ "lv" ] );
$.datepicker.formatDate( "dd.mm.yyyy", new Date( 2007, 1 - 1, 26 ) );