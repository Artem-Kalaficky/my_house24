// check all messages in DataTable
$('.checkbox-toggle').click(function (){
    $('.check-fa').toggleClass('fa-square').toggleClass('fa-check-square')
    var cells = $("#table").DataTable().column(0).nodes() // Cells from 1st column

    for (var i = 0; i < cells.length; i += 1) {
        if ($('.check-fa').hasClass('fa-check-square')) {
            cells[i].querySelector("input[type='checkbox']").checked = true;
        } else {
            cells[i].querySelector("input[type='checkbox']").checked = false;
        }
    }
})
