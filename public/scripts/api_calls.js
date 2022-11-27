function getQuotes(){
    var res_loc = document.getElementById('res');
    var list = document.getElementById('res-list');

    fetch("quote").then(response => {
        return response.json();
    }).then(res => {
        var data = res
        
        // clear list
        while (list.firstChild) {
            list.removeChild(list.firstChild);
        }
        
        // populate list
        for (var i = 0; i < data.length; i++){
            list.innerHTML += `<li class='list-group-item'>` + data[i].quote + " - " + data[i].author + `</li>`;
        }
        
        // insert response
        res_loc.textContent = JSON.stringify(data, null, 2);
        
        console.log(data);
    }).catch(err => {
        // Do something for an error here
    });
}

window.addEventListener("load", () => {
    var button = document.getElementById("res-btn");
    button.addEventListener("click", getQuotes);
})
