function luuPhieuKham(){
	let inputs = document.querySelectorAll(" tr > td:nth-child(5) > input")
	let id_thuoc = document.querySelectorAll(" tr > td:nth-child(2)")
	let ids = [];
	let soLuong = []
	for (var i = 0; i < inputs.length; i++){
		soLuong[i] = Number(inputs[i].value)
		ids[i] = Number(id_thuoc[i].innerText)
	}

	fetch("/api/luuPhieuKham", {
		method: "post",
		body: JSON.stringify({
			"soLuong": soLuong,
			"id": ids
		}), headers: {
			'Content-Type': 'application/json'
		}
	}).then(res => res.json()).then(data => {
        alert(data.message);
	})
}

function update_soLuong(id, obj){
    fetch(`/api/thanhtoan/${id}`, {
        method: "PUT",
        body: JSON.stringify({
			"soLuong": obj.value
		}), headers: {
			'Content-Type': 'application/json'
		}
	}).then(res => res.json()).then(data => {
        document.getElementById("total_price").innerText = data;
	})
}

function pay(){

  fetch('/api/luuHD',{
    method: "post",
    body: JSON.stringify({
      "tienThuoc": Number(document.getElementById("tienThuoc").value.substring(0, document.getElementById("tienThuoc").value.indexOf("V") - 1)),
      "tienKham": Number(document.getElementById("tienKham").value.substring(0, document.getElementById("tienKham").value.indexOf("V") - 1)),
      "tongTien": Number(document.getElementById("tongTien").value.substring(0, document.getElementById("tongTien").value.indexOf("V") - 1))


    }),
    headers:{
    'Content-Type': 'application/json'
    }
  }).then(res =>res.json()).then(data=>{

   alert(data.message)
  })

}
