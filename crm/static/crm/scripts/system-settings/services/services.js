//add SERVICE form by click on button
$('#add-service').click(function() {
	let form_idx = $('#id_form-TOTAL_FORMS').val();
	$('#service_form').append($('#empty_form-service').html().replace(/__prefix__/g, form_idx));
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})


//delete SERVICE form
function delete_service(index) {
	$('.delete-list-service').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
	$('#' + index + '-form').css('display', 'none');
}


//add UNIT form by click on button
$('#add-unit').click(function() {
	let form_idx = $('#id_unit_formset-TOTAL_FORMS').val();
	$('#unit_form').append($('#empty_form-unit').html().replace(/__prefix__/g, form_idx));
	$('#id_unit_formset-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})


//delete UNIT form
function delete_unit(index) {

	$('.delete-list-unit').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
	$('#' + index + '-form').css('display', 'none');
}

