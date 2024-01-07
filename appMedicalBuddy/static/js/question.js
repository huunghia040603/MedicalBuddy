// Add Question
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



function add_booking(){
  fetch('/api/ngaykham',{
    method: "post",
    body: JSON.stringify({
      "ngayKham":document.getElementById("ngayKham").value,
      "tenBN":document.getElementById("tenBN").value,
      "emailBN":document.getElementById("emailBN").value
    }),
    headers:{
    'Content-Type': 'application/json'
    }
  }).then(res =>res.json()).then(data=>{
     if (data.status===200)
     {
       document.getElementsByClassName("errorform")[0].style.display="none";
       document.getElementsByClassName("successform")[0].style.display="block";
        document.getElementsByClassName("booking")[0].disabled=true;
      }
       else
       {
       alert(data.message);
        document.getElementsByClassName("successform")[0].style.display="none";
       document.getElementsByClassName("errorform")[0].style.display="block";
        }
//     alert(data.message)
  })
}

function kiemtrangay(){
    today = new Date();
    date = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`;
    if (date.lastIndexOf("-") - date.indexOf("-") === 2)
        date = date.replace(date.substring(date.indexOf("-") + 1, date.lastIndexOf("-")), `0${today.getMonth() + 1}`)
    if (date.length - date.lastIndexOf("-") === 2)
        date = date.replace(date.substring(date.lastIndexOf("-") + 1), `0${today.getDate()}`)
    document.getElementById("ngayKham").min = date + "T" + today.toLocaleTimeString(); ;

}

function layngay(){
    var d = new Date();
    document.getElementById("idngaykham1").value=d.toLocaleDateString();
}

function CheckMK(){
fetch('/api/check',{
    method: "post",
    body: JSON.stringify({
      "matkhau":document.getElementById("matkhau").value
    }),
    headers:{
    'Content-Type': 'application/json'
    }
  }).then(res =>res.json()).then(data=>{
     alert(data.message);
     if (data.status===400)
        window.location = "/log-out";
      else
        document.getElementById("modalKiemTra").id="modalKiemTra1";







//     alert(data.message)
  })

}
 // Back To To


    // Back To Top
//    function backToTop1(button) {
//            var $button = $(button);
//            $(window).on('scroll', function () {
//                if ($(this).scrollTop() >= 500) {
//                    $button.addClass('visible');
//                } else {
//                    $button.removeClass('visible');
//                }
//            });
//            $button.on('click', function () {
//                $('body,html').animate({
//                    scrollTop: 0
//                }, 1000);
//            });
//
//    }
//
//backToTop1('.js-backToTop');

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