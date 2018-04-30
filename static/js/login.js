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
		var re = /^[a-zA-Z0-9_]{5,20}$/
		obj.next().hide();
		if (!re.test(obj.val()))
			{
				obj.next().html('请输入5-10位英文/数字/下划线字符的用户名').show();
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
			// console.log($('#login_form').serializeArray(),$('#login_form').serialize())
			// $.ajaxSetup({
			// 			data:{'csrfmiddlewaretoken':'{{csrf_token}}'}
			// 		})
			$.ajax({
							url:'/user/login_handle/',
							type:'post', 
							// async:false,
							data:$('#login_form').serializeArray(), 
							/*{'csrfmiddlewaretoken':$('[name="csrfmiddlewaretoken"]').val()},*/
							dataType:'json',
							success:function(data)
							{
								var name = data['name'],pwd = data['pwd'],url=data['url'];
								if(name&&pwd)
								{
									// window.location.href = url
									// 如果前一页是注册页或者是直接进入登录页
									('register'.indexOf(document.referrer)|| 'login'.indexOf(location.href))?window.location.href ='/':window.location.href =document.referrer;
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


