$(function(){
	//-------------------------------------------------
	//		Actions to execute when page loads
	//-------------------------------------------------
	if ($("#trans_date").length > 0){
		//Adjust the date string from "Aug. 9, 1995" to "Aug 9, 1995"
		var str = $("#trans_date").val().replace(".", "");
		var date = new Date(str);
	}
	else{
		var date = new Date();
	}
	$('#id_date_month').val(date.getMonth()+1);
	$('#id_date_day').val(date.getDate());
	$('#id_date_year').val(date.getFullYear());
    $('#id_from_account').val(2);
});
