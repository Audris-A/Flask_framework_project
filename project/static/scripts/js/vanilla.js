$(document).ready(function() {
    checkFields();
});

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

function checkFields(){
  try {
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
                $(element).css("display" , "block");
          });
      } else {
          $(".offsetBlock").each(function(index, element){
                $(".offsetBlock > input, select").prop('required', false);
                $(element).css("display" , "none");
          });
      }
  } catch (e){
      //
  }
}

// Multi-select
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

// Datepicker
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

// Bootstarp validation
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()