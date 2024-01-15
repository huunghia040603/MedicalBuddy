
function kiemtrangay(){
    today = new Date();
    date = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`;
    if (date.lastIndexOf("-") - date.indexOf("-") === 2)
        date = date.replace(date.substring(date.indexOf("-") + 1, date.lastIndexOf("-")), `0${today.getMonth() + 1}`)
    if (date.length - date.lastIndexOf("-") === 2)
        date = date.replace(date.substring(date.lastIndexOf("-") + 1), `0${today.getDate()}`)
    document.getElementById("ngayKham").min = date + "T" + today.toLocaleTimeString(); ;

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
  })
}
