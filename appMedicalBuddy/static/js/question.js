function add_question1(){
if (confirm("Bạn chắc chắn đặt câu hỏi ?") === true) {
  fetch('/api/cauhoi',{
    method: "post",
    body: JSON.stringify({
      "topic":document.getElementById("topic").value,
      "message":document.getElementById("message").value
    }),
    headers:{
    'Content-Type': 'application/json'
    }
  }).then(res =>res.json()).then(data=>{
     alert(data.message)
  })
  }
  console.log(document.getElementById("topic").value + " " + document.getElementById("message").value)
}


//// change password form
//            if (forms.changePasswordForm.length) {
//                var $changePasswordForm = forms.changePasswordForm;
//                $changePasswordForm.submit(function () {
//                    $.ajax({
//                        type: "POST",
//                        data: $changePasswordForm.serialize(),
//                        url: "/api/change-password",
//                        success: function success(data, textStatus, jqXHR) {
//                            alert(data.message);
//                            $changePasswordForm.get(0).reset();
//                        },
//                        error: function error(jqXHR, textStatus, errorThrown) {
//                            alert(jqXHR.responseJSON.message);
//                        }
//                    })
//                    return false;
//                })
//
//            }(jQuery);