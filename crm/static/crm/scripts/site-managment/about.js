$('#add').click(function() {
	let form_idx = $('#id_formset-TOTAL_FORMS').val();
	$('#formset').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_formset-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})


function delete_doc(index) {
	$('#id_' + index + '-document').val('')
	$('.delete-list').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
	$('#' + index + '-form').css('display', 'none');
}