function status(){
    fetch("/api/hdbenhnhan",{
        method: "post"
    }).then(res => res.json()).then(data => {
        alert(data.message);

    })
}