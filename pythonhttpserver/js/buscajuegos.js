fetch("/getgames",{method: 'POST'})
.then((data)=>data.json())
.then(function(info){
    let form = document.getElementsByClassName("formulario")[0]
    let global = document.createElement("div")
    for (let game of info.video_games){
        let divthis = document.createElement("div")
        let label = document.createElement("label")
        label.innerHTML = game.display_name + ": "
        divthis.append(label)
        let check = document.createElement("input")
        check.setAttribute("type","checkbox")
        check.setAttribute("name","juegos")
        check.setAttribute("value",game.display_name)
        divthis.append(check)

        global.append(divthis)
      

        
    }
    form.append(global)
    
    let ok = document.createElement("button")
    let diventer= document.createElement("div")
    diventer.setAttribute("id","enter")
    ok.setAttribute("type","submit")
    ok.setAttribute("class","enter")
    ok.innerHTML ="Registrarse"
    diventer.append(ok)
    form.append(diventer)
    
    

})