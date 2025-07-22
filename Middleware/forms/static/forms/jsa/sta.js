document.addEventListener('DOMContentLoaded', function() {
// Get the elements
    var spotterRequiredCheckbox =
        document.getElementById("id_spotter_required");
    var spotterNameLabel =
        document.getElementById("spotter_name_label");
    var spotterNameDiv = 
        document.getElementById("spotter_name_div");
    var spotterQualifiedLabel =
        document.getElementById("spotter_qualified_label");
    var spotterQualifiedDiv = 
        document.getElementById("spotter_qualified_div");

    // Function to show or hide the spotter name fields
    function toggleSpotterNameFields() {
        if (spotterRequiredCheckbox.checked) {
            spotterNameLabel.style.display = "";
            spotterNameDiv.style.display = "";
            spotterQualifiedLabel.style.display = "";
            spotterQualifiedDiv.style.display = "";
        } else {
            spotterNameLabel.style.display = "none";
            spotterNameDiv.style.display = "none";
            spotterQualifiedLabel.style.display = "none";
            spotterQualifiedDiv.style.display = "none";
        }
    }

    // Initially call the function to set correct visibility
    console.log("test1")
    toggleSpotterNameFields();

    // Add an event listener to the checkbox
    console.log("test2")
    spotterRequiredCheckbox.addEventListener('change', function() {
        if (spotterRequiredCheckbox.checked) {
            spotterNameLabel.style.display = "";
            spotterNameDiv.style.display = "";
            spotterQualifiedLabel.style.display = "";
            spotterQualifiedDiv.style.display = "";
        } else {
            spotterNameLabel.style.display = "none";
            spotterNameDiv.style.display = "none";
            spotterQualifiedLabel.style.display = "none";
            spotterQualifiedDiv.style.display = "none";
        }
    });
    console.log("test3")
});

/**
 * Event handler for changing the selected skill option.
 * Adds a new row to the form if the selected skill ends with '-all'.
 * Removes the 'all' row and adds a blank row for the next response.
 * Adds a new row if the selected skill is not empty.
 */
$("body").on('change', '[name$="tool"]', function () {
    var newRow = $('#tool-inspections .empty-form > tbody:nth-child(1) > tr:nth-child(1)').clone();
    var formCount = $('#id_safetytaskanalysistoolinspection_set-TOTAL_FORMS').val();
    newRow.html(newRow.html().replace(/__prefix__/g, formCount));
    $('#tool-inspections #formset-container').append(newRow);
    newRow.find('select').select2();

    // update count
    var formCountInput = document.querySelector('#id_safetytaskanalysistoolinspection_set-TOTAL_FORMS');
    formCountInput.value = $('#tool-inspections #formset-container tr').length;
});

$("body").on('change', '[name$="hazard"]', function () {
    var newRow = $('#hazard-mitigation .empty-form > tbody:nth-child(1) > tr:nth-child(1)').clone();
    var formCount = $('#id_safetytaskanalysishazardassessment_set-TOTAL_FORMS').val();
    newRow.html(newRow.html().replace(/__prefix__/g, formCount));
    $('#hazard-mitigation #formset-container').append(newRow);
    newRow.find('select').select2();

    // update count
    var formCountInput = document.querySelector('#id_safetytaskanalysishazardassessment_set-TOTAL_FORMS');
    formCountInput.value = $('#hazard-mitigation #formset-container tr').length;
});


$("body").on('change', '[name$="employee"]', function () {
    var newRow = $('#employee-acknowledgement .empty-form > tbody:nth-child(1) > tr:nth-child(1)').clone();
    var formCount = $('#id_staemployeeacknowledgement_set-TOTAL_FORMS').val();
    newRow.html(newRow.html().replace(/__prefix__/g, formCount));
    $('#employee-acknowledgement #formset-container').append(newRow);
    newRow.find('select').select2();
    newRow.find('.jsign-wrapper').empty();
    newRow.find('.jsign-wrapper').jSignature();

    // update count
    var formCountInput = document.querySelector('#id_staemployeeacknowledgement_set-TOTAL_FORMS');
    formCountInput.value = $('#employee-acknowledgement #formset-container tr').length;
});
