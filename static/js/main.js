// ready function
$(document).ready(function () {
    // jQuery Materilize collapsible handlers
    $('.collapsible').collapsible();

    // handler for category
    $('select').material_select();

    // handle navigation hamburger
    $(".button-collapse").sideNav();

});

//initialize the picker for due date
$('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15, // Creates a dropdown of 15 years to control year,
    today: 'Today',
    clear: 'Clear',
    close: 'Ok',
    closeOnSelect: false // Close upon selecting a date,
});


