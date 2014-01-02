$(function(){
	$('.change-projection-text input').keydown(function(event){
		if (event.which == 13){
			event.preventDefault();
			$(this).parent().hide();
			if ($.isNumeric($(this).val())){
				$('td#proj_'+this.id.substring(11)).html('$'+$(this).val());
			}
			$('td#proj_'+this.id.substring(11)).show();
		}
	});
	$('.change-projection-text').hide();
	$('.change-projection-link').click(function(){
		var this_id = this.id.substring(5);
		$('td#proj_'+this_id).hide();
		$('td#proj_text_'+this_id+' input').val($('td#proj_'+this_id).html().substring(1));
		$('td#proj_text_'+this_id).show();
		return false;
	});
});