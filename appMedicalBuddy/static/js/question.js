// --------------------Add Question--------------
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



//--------Cập Nhật  giá thuốc----------------
function CapNhat(obj){
  fetch('/api/capnhatthuoc',{
    method: "post",
    body: JSON.stringify({
      "tenThuoc":obj.value
    }),
    headers:{
    'Content-Type': 'application/json'
    }
  }).then(res =>res.json()).then(data=>{
     location.reload();
  })

}


 //-----Thêm Thuốc---------
// function Add_thuoc() {
//let element = document.getElementById('node');
// let dem=1;
//
//                                      if(typeof(Storage) !== "undefined") {
//                                        if (localStorage.clickcount) {
//                                          localStorage.clickcount = Number(localStorage.clickcount)+1;
//                                        } else {
//                                          localStorage.clickcount = 2;
//                                        }
//                                        dem= localStorage.clickcount;
//                                      } else {
//                                        document.getElementById("result").innerHTML = "Rất tiếc, trình duyệt của bạn không hỗ trợ Local Storage...";
//                                      }
//
//
//let x = `<form id="changePasswordForm1" method="post" style="margin:0;height:40px;padding:0 12px">
//                                    <div class="row" >
//                                        <div class="col-lg-1" style="padding:0 4px 0 20px" >
//                                            <div class="form-group focused" style="padding:0">
//                                                <input type="text"  id="input-old-password${dem}"
//                                                       class="form-control form-control-alternative"
//                                                       placeholder="Auto"
//                                                       name="oldPassword" value=${dem} style="padding:0 12px">
//                                            </div>
//                                        </div>
//                                        <div class="col-lg-4" style="padding:0 4px 0 0">
//                                            <div class="form-group focused">
//                                                <input type="text" list="browsers1" id="browser1"
//                                                       class="form-control form-control-alternative"
//                                                       placeholder="Vui lòng chọn thuốc....."
//                                                       name="newPassword">
//                                                <datalist id="browsers1">
//                                                    {%for t in ds_Thuoc%}
//                                                    <option value="{{t.tenThuoc}}"/>
//                                                    {% endfor%}
//                                                </datalist>
//                                            </div>
//                                        </div>
//                                        <div class="col-lg-1" style="padding:0 4px 0 0">
//                                            <div class="form-group">
//                                                <input type="text"
//                                                       class="form-control form-control-alternative"
//                                                       placeholder="Auto"
//                                                       name="confirmPassword">
//                                            </div>
//                                        </div>
//
//                                        <div class="col-lg-2" style="padding:0 4px 0 0">
//                                            <div class="form-group">
//                                                <input type="text"
//                                                       class="form-control form-control-alternative"
//                                                       placeholder="Số lương tính theo ĐVT"
//                                                       name="confirmPassword">
//                                            </div>
//                                        </div>
//                                        <div class="col-lg-2" style="padding:0 4px 0 0">
//                                            <div class="form-group">
//                                                <input type="text"
//                                                       class="form-control form-control-alternative"
//                                                       placeholder="Auto"
//                                                       name="confirmPassword">
//                                            </div>
//                                        </div>
//                                        <div class="col-lg-2" style="padding:0 20px 0 0">
//                                            <div class="form-group">
//                                                <input type="text"
//                                                       class="form-control form-control-alternative"
//                                                       placeholder="Auto"
//                                                       name="confirmPassword">
//                                            </div>
//                                        </div>
//                                    </div>
//                                </form>`
//// Vị trí 1: beforeend
//element.insertAdjacentHTML("beforeend", x);
//
//
//}


