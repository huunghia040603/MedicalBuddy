function trangthai(){
    let trangThai = document.querySelectorAll(" table td:last-child > select")
    let a = []
    for (var tt = 0; tt < trangThai.length; tt++)
        a[tt] = trangThai[tt].value

    fetch("/api/suatrangthai", {
        method: "post",
        body: JSON.stringify({
            "trangThai": a
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        alert(data);
        location.reload();
    })
}