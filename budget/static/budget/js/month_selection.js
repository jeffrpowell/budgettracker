$(function(){
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
		
		var path = window.location.pathname;
		if (path.indexOf("date/") >= 0){
			path = path.substring(0, path.indexOf("date/"));
		}
		window.location = path+'date/'+month+'/'+year+'/';
	}
});
