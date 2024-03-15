fetch("/logedinfo",{method:'POST'})
.then(
    function(ret){
        if (ret.status ==200){
            return ret.json()
        }
    }
).then(function(data){
    let menu = document.getElementsByTagName("mt-vsiderbar")[0]
    let dest = document.getElementById("user")
    let username  = document.createElement("p")
    while(dest.hasChildNodes()){dest.remove(dest.childNodes[0])}
    if (data.loged){
       
        username.innerHTML= ` Usuario:  ${data.nombre}`
        dest.append(username)
        let logout = document.createElement("form")
        logout.setAttribute("action","/logout")
        logout.setAttribute("method","post")
        let buton = document.createElement("button")
        buton.innerHTML="Cerrar sessión"

        logout.append(buton)
        dest.append(logout)
        let rutas = JSON.parse(menu.getAttribute("items"))

        rutas.push({'Tittle':'Su catalogo', 'Adr':'catalogo.html'})

        menu.setAttribute("items", JSON.stringify(rutas))
       
    }else{
        dest.append(document.createElement("h1"))
    }
    
})