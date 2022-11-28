function getQuotes(){
  var res_loc = document.getElementById('res');
  var list = document.getElementById('res-list');

  fetch("quote").then(response => {
      return response.json();
  }).then(res => {
      var data = res
      
      // clear list
      while (list.lastChild) {
          list.removeChild(list.lastChild);
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

function bookSearch(){
  // var res_loc = document.getElementById('res');
  var book_search_list = document.getElementById('book-search-res');

  var search_query = {
    q: document.getElementById('bookSearchQuery').value,
    p: 1
  }

  if (search_query.q === null || search_query.q === "") return

  var base_query = "book/search"
  var query = base_query + "?q=" + search_query.q + "&p=" + search_query.p

  fetch(query).then(response => {
      return response.json();
  }).then(res => {
      var data = res
      
      // @TODO: Remove dummy data and clear list operation
      // clear list
      while (book_search_list.lastChild) {
        book_search_list.removeChild(book_search_list.lastChild);
      }
      
      // no books match query
      if (data.length === 0){
        book_search_list.innerHTML += `<h3 style="text-align:center;">No books found.</h3>`
      }

      // populate list
      for (var i = 0; i < data.length; i++){
        book_search_list.innerHTML += `<li id="book-`+ i + `" isbn="` + data[i].Isbn + `" class="card m-2 box-shadow dummy d-flex flex-md-row align-items-center">
            <div class="flex-shrink-0">
              <img class="book-img d-none d-md-block" src="` + data[i].Cover_url + `">
            </div>
            <div class="card-body d-flex flex-column align-items-start">
              <h3>` + data[i].Title + `</h3>
              <p class="card-test mb-auto" id="book-authors-` + i + `">By: ` + data[i].Author_names + `</p>
              <div class="mb-1 text-muted" id="book-isbn-` + i + `">Isbn: ` + data[i].Isbn + `</div>
            </div>
            <div class="col-2 align-self-center m-4 mt-0 mb-2">
              <button class="btn btn-primary p-2" type="button" id="book-checkout-btn-` + i + `" bookid="book-` + i + `" isbn="` + data[i].Isbn + `">Checkout Book</button>
            </div>
        </li>`
      }
      
      // console.log(data);
  }).catch(err => {
      // Do something for an error here
  });
}

window.addEventListener("load", () => {
    var button = document.getElementById("res-btn");
    button.addEventListener("click", getQuotes);

    var book_search_input = document.getElementById("bookSearchQuery");
    book_search_input.addEventListener("keypress", (event) => {
      if (event.key === "Enter"){
        event.preventDefault();
        book_search_input.blur();
        bookSearch();
      }
    });
    
    var book_search_btn = document.getElementById("book-search-btn");
    book_search_btn.addEventListener("click", bookSearch)
})
