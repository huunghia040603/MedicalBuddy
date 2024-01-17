function getThang() {
fetch('/api/stats',{
    method:'post',
    body:JSON.stringify({
        "thang":document.getElementById("thang").value
    }),
    headers:{
    'Content-Type': 'application/json'
    }
}).then(res => res.json()).then(data => {

})
}