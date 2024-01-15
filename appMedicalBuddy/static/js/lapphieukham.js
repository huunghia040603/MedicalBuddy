
function layngay(){
    var d = new Date();
    document.getElementById("idngaykham1").value=d.toLocaleDateString();
}

//----------Xuất phiếu-----------
 function xuatphieu(){

  fetch('/api/lapphieukham',{
    method: "post",
    body: JSON.stringify({
      "hoTen": document.getElementById("tenBN")? document.getElementById("tenBN").value : "",
	  "trieuChung": document.getElementById("trieuchung")? document.getElementById("trieuchung").value : "",
	  "chungDoan": document.getElementById("dudoanbenh")? document.getElementById("dudoanbenh").value : ""
    }),
    headers:{
    'Content-Type': 'application/json'
    }
  }).then(res =>res.json()).then(data=>{

   alert(data.message)
  })

 }

//-------------Check Mat table----------------
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
      {
      if (confirm("Bạn chắc chắn xuất phiếu ?") === true) {
         localStorage.clear("clickcount");
        document.getElementById("modalKiemTra").id="modalKiemTra1";
        window.location = "/hoadon";
        }
        }
  })

}


//-----------Lưu Tạm Thời------------------
function luuTamThoi(obj){
    let href = "/api/luutamthoi"
    if (obj.id === "xuatPhieu")
        href = "/api/lapphieukham"
	let tick = document.getElementById("table").querySelectorAll(" input[type='checkbox']:checked")
	let a = [];
	for (var i = 0; i < tick.length; i++)
		a[i] = Number(tick[i].parentElement.id.substring(5)) + 5

	fetch(href, {
		method: "post",
		body: JSON.stringify({
			"tenBenhNhan": document.getElementById("tenBN")? document.getElementById("tenBN").value : "",
			"trieuChung": document.getElementById("trieuchung")? document.getElementById("trieuchung").value : "",
			"duDoanLoaiBenh": document.getElementById("dudoanbenh")? document.getElementById("dudoanbenh").value : "",
			"id": a
		}), headers: {
			'Content-Type': 'application/json'
		}
	}).then(res => res.json()).then(data => {
        alert("Lưu thành công");
        location.reload();
	})
}
