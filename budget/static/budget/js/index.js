$(function(){
	//http://www.infiniterecursion.ca/blog/django/2011/1/30/django-and-jquery-ajax-patterns/
	//http://stackoverflow.com/questions/5100539/django-csrf-check-failing-with-an-ajax-post-request
	$.ajaxSetup({
		traditional: true,
		beforeSend: function(xhr, settings) {
			function getCookie(name) {
				var cookieValue = null;
				if (document.cookie && document.cookie != '') {
					var cookies = document.cookie.split(';');
					for (var i = 0; i < cookies.length; i++) {
						var cookie = jQuery.trim(cookies[i]);
						// Does this cookie string begin with the name we want?
						if (cookie.substring(0, name.length + 1) == (name + '=')) {
							cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
							break;
						}
					}
				}
				return cookieValue;
			}
			if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
				// Only send the token to relative URLs i.e. locally.
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		} 
	});
	
	//Handler for keypresses in edit textboxes
	$('.change-projection-text input').keydown(function(event){
		if (event.which == 13){ //Enter keycode
			event.preventDefault(); //Don't submit a form
			var this_id = this.id.substring(11); //extract account id
			$(this).parent().hide(); //Hide text input div
			if ($.isNumeric($(this).val())){ //If valid input
				$('td#proj_'+this_id).text('$'+$(this).val()).show(); //Update static label
				//Submit change to server
				var post_data = {account_id: this_id, amount: $(this).val()};
				$.post('projection/', post_data, function(data){
					if (data || data == 0){
						$('td#diff_'+this_id).text('$'+data); //Update Difference amount
					}
					else{/*something went pretty wrong*/}
				}, 'json');
			}
			else{
				$('td#proj_'+this_id).show(); //Show static label
			}
		}
	});
	
	//Highlight text in textbox when it receives focus
	$('.change-projection-text input').focus(function(){
		$(this).select(); 
	});
	
	//Actions to execute when page loads
	$('.change-projection-text').hide(); //hide textboxes
	$('td:contains("-")').each(function(){
		var text = $(this).text().replace(/\$/, '');
		if ($.isNumeric(text)){
			$(this).addClass('negative'); //color negative values
		}
	});
	
	//What happens when "Change Projection" link is clicked
	$('.change-projection-link').click(function(){
		var this_id = this.id.substring(5); //Extract account id
		$('td#proj_'+this_id).hide(); //Hide the static label
		$('td#proj_text_'+this_id+' input').val($('td#proj_'+this_id).html().substring(1)); //Put the static label value in textbox
		$('td#proj_text_'+this_id).show(); //show text box div
		$('td#proj_text_'+this_id+' input').focus(); //give focus to textbox, setting off our handler
		return false; //don't reload the page because we've clicked on a link
	});
	
	//MONTH - YEAR SELECTION LOGIC
	
	//Select month button
	$('#'+$('#start-month').val()).button('toggle');
	
	$('#month-buttons button').click(function(){
		$('#month-buttons button.active').not(this).button('toggle'); //radio-button toggling
		sendDateChangeAjax($(this).attr('id'), 0);
	});
	
	$('#year-increase').click(function(){
		sendDateChangeAjax($('#month-buttons button.active').attr('id'), 1);
	});
	
	$('#year-decrease').click(function(){
		sendDateChangeAjax($('#month-buttons button.active').attr('id'), -1);
	});
	
	/* yearChange should be integers -1, 0, or 1*/
	var sendDateChangeAjax = function(month, yearChange){
		var year = $('#year-select').text().replace(/"/, '').trim();
		year = parseInt(year) + yearChange;
		window.location = '/budget/date/'+month+'/'+year+'/';
	}
});
