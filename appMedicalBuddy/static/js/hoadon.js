function luuTamThoi(){
	let tick = document.querySelectorAll(" tr > td:nth-child(5) > input").length
	let a = [];
	for (var i = 0; i < tick; i++)
		a[i] =document.querySelectorAll(" tr > td:nth-child(5) > input")[i].value

	fetch("/api/hoadon", {
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
