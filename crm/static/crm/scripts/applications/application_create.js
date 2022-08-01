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