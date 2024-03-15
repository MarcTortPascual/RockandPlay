import { search, searchtex } from "./busqueda.js"
fetch("../db/biblio/libros.xml")
.then(ret=>ret.text())
.then(function(data){
    let autores = []
    let generos = []
    let parser = new DOMParser()
    let xml = parser.parseFromString(data,"text/xml")
    let libros = xml.getElementsByTagName("libro")
    let select = document.getElementById("autor")
    let select2 = document.getElementById("genero")
    let librodiv = document.createElement("div")
    let body = document.getElementById("libros")
    let html = document.createElement("h1")
    for (let libro of libros){
        let genero = libro.getElementsByTagName("genero")[0]
        if (generos.includes(genero.innerHTML)===false){
            let it1 = document.createElement("option")
            it1.setAttribute("value", genero.innerHTML)
            it1.innerHTML=genero.innerHTML
            select2.append(it1) 
            generos.push(genero.innerHTML)
        }
        let autor = libro.getElementsByTagName("autor")[0]
        if (autores.includes(autor.innerHTML)===false){
            let it = document.createElement("option")
            it.setAttribute("value", autor.innerHTML)
            it.innerHTML=autor.innerHTML
            select.append(it)
            autores.push(autor.innerHTML)
        }
        librodiv = document.createElement("div")
        librodiv.setAttribute("class", "libro")
        for (let item of libro.children){
            if (item.tagName=="titulo"){
                html = document.createElement("h1")
                html.innerHTML = item.innerHTML
                librodiv.append(html)
            }
            if (item.tagName=="isbn" || item.tagName=="autor" || item.tagName=="genero" || item.tagName=="descripcion" ){
                html = document.createElement("p")
                html.innerHTML = item.innerHTML
                librodiv.append(html)
            }
            if (item.tagName=="miniatura"){
                html = document.createElement("img")
                html.setAttribute ("src",item.getAttribute("src"))
                html.style.width ="30%"
                librodiv.append(html)
            }
        }
        body.append(librodiv)
    }

    
})


let select = document.getElementById("autor")
select.addEventListener("change",function(){search("../db/biblio/libros.xml","autor",document.getElementById("libros"),"libro")})
libros.xml
let select2 = document.getElementById("genero")
select2.addEventListener("change",function(){search("../db/biblio/libros.xml","genero",document.getElementById("libros"),"libro")})
let titulo = document.getElementById("titulo")
titulo.addEventListener("input",function(){searchtex("../db/biblio/libros.xml","titulo",document.getElementById("libros"),"libro")})