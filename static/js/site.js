$(function(){
	// 委托
	var allows = false;
	$('.form_group').delegate('*','blur',function(){
		var txt = $(this).val()?$(this).val():$(this).html();
		if (txt.length==0||txt=='此项不能空!')
		{
			$(this).val('此项不能空!').css({color:'red'});
			allows = false;
		}
		else
		{
			$(this).css({color:'#000'})
			allows = true;
		}
	})
	$('.site_con form').submit(function(){
		return allows
	})
})