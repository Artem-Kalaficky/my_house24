// formset
$('#add-service').click(function() {
	let form_idx = $('#id_formset-TOTAL_FORMS').val();
	$('#formset-table tbody').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_formset-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})


function delete_service(index) {
	$('.delete-list').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
	$('#' + index + '-form').remove();
    get_full_cost()
}

// work with services in formset
function get_full_cost() {
    let sum= 0;
    $("input.full-cost").each(function(){
      sum += +($(this).val());
    });
    $('#current_amount').html(sum.toFixed(2), Math.round(sum*10)/10)
    $('#amount').attr('value', sum)
}


function get_cost(index) {
    if (index.indexOf('expense') > 0) {
        let cost_for_unit = index.replace(/expense/g, 'cost_for_unit')
        let full_cost = index.replace(/expense/g, 'full_cost')
        let cost = $('#' + index).val() * $('#' + cost_for_unit).val()
        $('#' + full_cost).attr('value', cost.toFixed(2), Math.round(cost*10)/10)
    } else {
        let expense = index.replace(/cost_for_unit/g, 'expense')
        let full_cost = index.replace(/cost_for_unit/g, 'full_cost')
        let cost = $('#' + index).val() * $('#' + expense).val()
        $('#' + full_cost).attr('value', cost.toFixed(2), Math.round(cost*10)/10)
    }
    get_full_cost()
}




// date widgets
$('input[name="date"]').daterangepicker({
    singleDatePicker: true,
    default: 'date',
    opens: 'center',
    autoUpdateInput: false,
    onClose: function() {
      $( this ).valid();
    },
    locale: {
        format: 'DD.MM.YYYY',
        "applyLabel": "Ок",
        "cancelLabel": "Отмена",
        "fromLabel": "От",
        "toLabel": "До",
        "customRangeLabel": "Произвольный",
        "daysOfWeek": [
            "Вс",
            "Пн",
            "Вт",
            "Ср",
            "Чт",
            "Пт",
            "Сб"
        ],
        "monthNames": [
            "Январь",
            "Февраль",
            "Март",
            "Апрель",
            "Май",
            "Июнь",
            "Июль",
            "Август",
            "Сентябрь",
            "Октябрь",
            "Ноябрь",
            "Декабрь"
        ],
        firstDay: 1
    }
});
$('input[name="date"]').on('apply.daterangepicker', function(ev, picker) {
    $(this).val(picker.startDate.format('DD.MM.YYYY'));
});
$('input[name="date"]').on('cancel.daterangepicker', function(ev, picker) {
    $(this).val('');
});


$('input[name="date_with"]').daterangepicker({
    singleDatePicker: true,
    default: 'date',
    opens: 'center',
    autoUpdateInput: false,
    onClose: function() {
      $( this ).valid();
    },
    locale: {
        format: 'DD.MM.YYYY',
        "applyLabel": "Ок",
        "cancelLabel": "Отмена",
        "fromLabel": "От",
        "toLabel": "До",
        "customRangeLabel": "Произвольный",
        "daysOfWeek": [
            "Вс",
            "Пн",
            "Вт",
            "Ср",
            "Чт",
            "Пт",
            "Сб"
        ],
        "monthNames": [
            "Январь",
            "Февраль",
            "Март",
            "Апрель",
            "Май",
            "Июнь",
            "Июль",
            "Август",
            "Сентябрь",
            "Октябрь",
            "Ноябрь",
            "Декабрь"
        ],
        firstDay: 1
    }
});
$('input[name="date_with"]').on('apply.daterangepicker', function(ev, picker) {
    $(this).val(picker.startDate.format('DD.MM.YYYY'));
});
$('input[name="date_with"]').on('cancel.daterangepicker', function(ev, picker) {
    $(this).val('');
});


$('input[name="date_before"]').daterangepicker({
    singleDatePicker: true,
    default: 'date',
    opens: 'center',
    autoUpdateInput: false,
    onClose: function() {
      $( this ).valid();
    },
    locale: {
        format: 'DD.MM.YYYY',
        "applyLabel": "Ок",
        "cancelLabel": "Отмена",
        "fromLabel": "От",
        "toLabel": "До",
        "customRangeLabel": "Произвольный",
        "daysOfWeek": [
            "Вс",
            "Пн",
            "Вт",
            "Ср",
            "Чт",
            "Пт",
            "Сб"
        ],
        "monthNames": [
            "Январь",
            "Февраль",
            "Март",
            "Апрель",
            "Май",
            "Июнь",
            "Июль",
            "Август",
            "Сентябрь",
            "Октябрь",
            "Ноябрь",
            "Декабрь"
        ],
        firstDay: 1
    }
});
$('input[name="date_before"]').on('apply.daterangepicker', function(ev, picker) {
    $(this).val(picker.startDate.format('DD.MM.YYYY'));
});
$('input[name="date_before"]').on('cancel.daterangepicker', function(ev, picker) {
    $(this).val('');
});