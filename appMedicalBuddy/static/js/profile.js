function doimatkhau(){
fetch('/api/change-password',{
    method: "post",
    body: JSON.stringify({
      "matkhaucu":document.getElementById("input-old-password").value,
      "matkhaumoi":document.getElementById("input-new-password").value

    }),
    headers:{
    'Content-Type': 'application/json'
    }
  }).then(res =>res.json()).then(data=>{
     alert(data.message);
     location.reload()
  })

}


