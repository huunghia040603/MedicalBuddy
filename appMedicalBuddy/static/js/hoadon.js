function pay(){
	let inputs = document.querySelectorAll(" tr > td:nth-child(5) > input")
	let id_thuoc = document.querySelectorAll(" tr > td:nth-child(2)")
	let ids = [];
	let soLuong = []
	for (var i = 0; i < inputs.length; i++){
		soLuong[i] = Number(inputs[i].value)
		ids[i] = Number(id_thuoc[i].innerText)
	}

	fetch("/api/thanhtoan", {
		method: "post",
		body: JSON.stringify({
			"soLuong": soLuong,
			"id": ids
		}), headers: {
			'Content-Type': 'application/json'
		}
	}).then(res => res.json()).then(data => {
        alert("Lưu thành công");
        location.reload();
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
