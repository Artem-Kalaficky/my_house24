$('#add').click(function() {
	let form_idx = $('#id_formset-TOTAL_FORMS').val();
	$('#formset').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_formset-TOTAL_FORMS').val(parseInt(form_idx) + 1);
	$('#id_formset-' + form_idx + '-description').wysihtml5({
		locale: 'ru-RU',
            toolbar: {
                "font-styles": true, //Font styling, e.g. h1, h2, etc. Default true
                "emphasis": true, //Italics, bold, etc. Default true
                "lists": true, //(Un)ordered lists, e.g. Bullets, Numbers. Default true
                "html": false, //Button which allows you to edit the generated HTML. Default false
                "link": false, //Button to insert a link. Default true
                "image": false, //Button to insert an image. Default true,
                "color": false, //Button to change color of font
                "blockquote": false, //Blockquote
                "fa": true,
                "size": 'none' //default: none, other options are xs, sm, lg
            }
	})
})


function delete_service(index) {
	$('.delete-list').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
	$('#' + index + '-form').css('display', 'none');
}