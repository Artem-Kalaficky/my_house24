// load image to form
$('input[type=file]').change(function (event){
    $('img[id="' + this.id + '"]').attr('src', URL.createObjectURL(event.target.files[0]))
})
// validate
$('#id_image_1').change(function (event){
	let img = new Image();
	img.src = URL.createObjectURL(event.target.files[0]);
	img.onload = function () {
		if (img.width == 522 && img.height == 350) {
			$('#img1').css('color', 'green')
		} else {
			$('#img1').css('color', 'red')
		}
	}
})
$('#id_image_2, #id_image_3, #id_image_4, #id_image_5').change(function (event){
	let id = this.id
	let img = new Image();
	img.src = URL.createObjectURL(event.target.files[0]);
	img.onload = function () {
		if (img.width == 248 && img.height == 160) {
			$('#' + id).css('color', 'green')
		} else {
			$('#' + id).css('color', 'red')
		}
	}
})


//section formset
$('#add-section').click(function() {
	let form_idx = $('#id_section_formset-TOTAL_FORMS').val();
	$('#section_formset').append($('#empty_form-section').html().replace(/__prefix__/g, form_idx));
	$('#id_section_formset-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})

function delete_section(index) {
	$('.delete-list-section').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
	$('#' + index + '-form').css('display', 'none');
}


//floor formset
$('#add-floor').click(function() {
	let form_idx = $('#id_floor_formset-TOTAL_FORMS').val();
	$('#floor_formset').append($('#empty_form-floor').html().replace(/__prefix__/g, form_idx));
	$('#id_floor_formset-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})

function delete_floor(index) {
	$('.delete-list-floor').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
	$('#' + index + '-form').css('display', 'none');
}


//user formset
$('#add-user').click(function() {
	let form_idx = $('#id_form-TOTAL_FORMS').val();
	$('#user_formset').append($('#empty_form-user').html().replace(/__prefix__/g, form_idx));
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})

function delete_user(index) {
	$('.delete-list-user').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
	$('#' + index + '-form').css('display', 'none');
}




