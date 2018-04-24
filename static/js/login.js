$(function(){
	var $uname = $('.name_input'),$upwd = $('.pass_input');
	var	unameVal = $uname.val(),upwdVal = $upwd.val();
	var crr_name = false, crr_pwd = false,jumpNow = false;

	$uname.blur(function(){
		check_name($(this));
	});
	$uname.focus(function(){
		$(this).next().hide();
	});	
	$upwd.blur(function(){
		check_pwd($(this));
	});
	$upwd.focus(function(){
		$(this).next().hide();
	});		
	function check_name(obj){
		var len = obj.val().length;
		obj.next().hide();
		if (len<5||len>10)
			{
				obj.next().html('请输入5-10位字符的用户名').show();
				crr_name = false
			}
		else				
			{
				crr_name  = true;
			}
	}
	function check_pwd(obj){
		var len = obj.val().length;
		obj.next().hide();
	 	if(len<8||len>20)
		{
			obj.next().html('请输入8-20位密码').show();
			crr_pwd = false
		}
		else
		{
			crr_pwd = true;
		}		
	}
	$('.input_submit').click(function(){
		check_name($uname);
		check_pwd($upwd);
		if (crr_name&&crr_pwd)
		{	
			$.ajaxSetup({
						data:{'csrfmiddlewaretoken':'{{csrf_token}}'}
					})
			$.ajax({
							url:'/user/login_handle/',
							type:'post', 
							// async:false,
							// data:{'username':$uname.val(),'pwd':$upwd.val(),'csrfmiddlewaretoken':$('[name="csrfmiddlewaretoken"]').val()},
							data:{'username':$uname.val(),'pwd':$upwd.val(),'csrfmiddlewaretoken':$('[name="csrfmiddlewaretoken"]').val()},
							dataType:'json',
							success:function(data)
							{
								var name = data['name'],pwd = data['pwd']
								if(name&&pwd){
									window.location.href = '/user/user_center_info'
								}
								if(name==0)
								{
									$upwd.val("");
									$uname.next().html('用户名不存在,请先注册再登陆!').show();
									crr_name = false;
									// 判断用户是否勾选记住用户
									if($.find('input:checked').length==0)
									{
										$uname.val("");
									}									
								}
								else
								{
									if(pwd==0)
										{
										$upwd.next().html('密码错误,请核对后重新输入!').show();
										crr_pwd = false;
										}
								}
								
							}
			})
		}
	});
});
		// $('#login_form').submit(function(){
		// 	check_name($uname);
		// 	check_pwd($upwd);
		// 	if (crr_name&&crr_pwd)
		// 	{		
		// 		$.psot('/user/login_handle/',{'username':$uname.val(),'pwd':$upwd.val()},function(data){
		// 			var name = data['name'],pwd = data['pwd']
		// 			alert(data)
		// 			if(name&&pwd)
		// 			{
		// 				jumpNow = true;
		// 			}
		// 			else
		// 			{
		// 				jumpNow = false;
		// 				if(name==0)
		// 				{
		// 					$uname.next().html('用户名不存在,请先注册再登陆!').show();
		// 					ev.preventDefault();
		// 				}
		// 				if(pwd==0)
		// 				{
		// 					$upwd.next().html('密码错误,请核对后重新输入!').show();
		// 				};
		// 			}
		// 		})
				
		// 		if (jumpNow) 
		// 		{
		// 			return true;
		// 		}
		// 		else
		// 		{
		// 			return false;
		// 		}
		// 	}
		// 	else
		// 	{
		// 		return false;
		// 		// ev.preventDefault();
		// 	}
		// })




