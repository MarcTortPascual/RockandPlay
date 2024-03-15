
fetch("/catalogo",{method: 'POST'})
.then(ret=>ret.json())
.then(function(data){


    let target = document.querySelector("#juegos")
    for (let game of data.video_games){
        let localdiv = document.createElement("div")
        localdiv.setAttribute("class","boxgames")
        let element = document.createElement("h1")
        element.style.gridArea = "titulo"
        element.setAttribute("class","juegotitulo")
        element.innerHTML=game.display_name
        localdiv.append(element)
        element = document.createElement("h2")
        element.style.gridArea = "desarollador"
        element.innerHTML=game.developer
        localdiv.append(element)
        element = document.createElement("p")
        element.style.gridArea = "genero"
        element.innerHTML = game.genere
        localdiv.append(element)
        element = document.createElement("p")
        element.style.gridArea = "descripcion"
        element.innerHTML = game.description
        localdiv.append(element)
        localdiv.append(element)
        element = document.createElement("img")
        element.style.gridArea = "img"
        element.setAttribute("class","imgjuegos")
        element.setAttribute("src",game.image)
        element.style.width = "95%"
        
        localdiv.append(element)
        let form = document.createElement("form")
        form.setAttribute("method","post")
        if (game.subscrito){

            element = document.createElement("button")
            element.setAttribute("id","sub")
            element.setAttribute("type","submit")
            form.setAttribute("action","/cancelar")
            form.setAttribute("class","juegoboton")
            element.setAttribute("name","game")
            element.setAttribute("value",game.display_name)
           
            element.innerHTML="cancelar"
            form.style.gridArea = "boton"
    
            form.append(element)
            localdiv.append(form)
        }else if (!game.subscrito){
            form.setAttribute("action","/apcetar")
            form.setAttribute("class","juegoboton")
            element = document.createElement("button")
            element.setAttribute("id","nosub")
            element.setAttribute("type","submit")
            element.setAttribute("name","game")
            element.setAttribute("value",game.display_name)
            
            element.innerHTML="subscribirse"
            form.style.gridArea = "boton"
          
            form.append(element)
            localdiv.append(form)
        }
        


        target.append(localdiv)
       
        console.log(game)
        
        
    }

    
})
