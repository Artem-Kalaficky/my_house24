$('#add-service').click(function() {
	let form_idx = $('#id_formset-TOTAL_FORMS').val();
	$('#formset').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_formset-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})


function delete_service(index) {
	$('#id_' + index + '-cost_for_unit').val("")
	$('.delete-list').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
	$('#' + index + '-form').css('display', 'none');
}


// load data for unit after select service
function select_unit(index) {
	let unit = $('#' + index).parent().find('option:selected').data('unit')
	$('#' + index + '-u').parent().find('option[value=' + unit + ']').prop('selected', 'true')
	if (unit) {
		$('#' + index + '-u').parent().find('option[value=' + unit + ']').prop('selected', 'true')
	} else {
		$('#' + index + '-u').parent().find('option[value=none]').prop('selected', 'true')
	}
}