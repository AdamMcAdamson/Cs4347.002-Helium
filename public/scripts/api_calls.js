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
              <button onclick="bookCheckoutModal('` + data[i].Isbn + `', '` + data[i].Title.replace("'", "\\'") + `')" class="btn btn-primary p-2 checkout-book-btn" type="button" data-bs-toggle="modal" data-bs-target="#checkout-book-modal" id="book-checkout-btn-` + i + `" bookid="book-` + i + `" isbn="` + data[i].Isbn + `">Checkout Book</button>
            </div>
        </li>`
      }
      
      // console.log(data);
  }).catch(err => {
      // Do something for an error here
  });
}

function bookCheckoutModal(isbn, title){
  
  var modal_elem = document.getElementById('checkout-book-card-id');
  var modal_book_title_elem = document.getElementById('checkout-book-title');
 
  modal_elem.setAttribute("isbn", isbn);
  modal_book_title_elem.innerText = title;

  var alert_elem = document.getElementById('checkout-book-alert')
  while (alert_elem.lastChild) {
    alert_elem.removeChild(alert_elem.lastChild);
  }
}

function bookCheckoutForm(event){
  event.preventDefault()
  var checkout_book_form = document.getElementById("checkout-book-form")
  if (!checkout_book_form.checkValidity()) {
    event.stopPropagation()
    checkout_book_form.classList.add('was-validated')
    return
  }
  var isbn = document.getElementById('checkout-book-card-id').getAttribute("isbn");
  var card_id = parseInt(document.getElementById('checkout-book-card-id').value.substring(2));
  var alert_elem = document.getElementById('checkout-book-alert')
  
  var base_query = "book/checkout"
  var query = base_query + "?isbn=" + isbn + "&card_id=" + card_id

  fetch(query, { 
    method: "POST"
  }).then(response => {
    return response.json().then(data => ({status: response.status, message: data.message, data: data}))
  }).then(res => {
    
    console.log(alert_elem.getAttributeNames())

    console.log(res.status)

    while (alert_elem.lastChild) {
      alert_elem.removeChild(alert_elem.lastChild);
    }
    
    if (res.status != 200) {
      alert_elem.innerHTML += `
      <div class="alert alert-warning d-flex align-items-center alert-dismissible fade show" role="alert">
        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Warning:"><use xlink:href="#exclamation-triangle-fill"/></svg>
        <div>
          <strong>Error:</strong> ` + res.message + `
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
      </div>
      `
    } else {
      alert_elem.innerHTML += `
      <div class="alert alert-success d-flex align-items-center alert-dismissible fade show" role="alert">
        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
        <div>
          ` + res.message + `
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
      `
    }
    //var data = res.data

    
    console.log("HIHIHIH");
  }).catch(err => {
    // Do something for an error here
  });
}

function createBorrower(){
  
  var borrower_list = document.getElementById('book-search-res');
  var SSN = document.getElementById('validationSSN').value;
  var name = document.getElementById('validationName').value;
  var address = document.getElementById('validationAddress').value;
  var phone = document.getElementById('validationPhone').value;


  var base_query = "borrower/create"
  var query = base_query + "?snn=" + SSN + "&name=" + name + "&address=" + address + "&phone=" + phone

  fetch(query).then(response => {
      return response.json();
  }).then(res => {
      var data = res
      
  }).catch(err => {
      // Do something for an error here
  });
  //return response.json();
  
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

    // var checkout_book_btns = document.getElementsByClassName("checkout-book-btn")
    // console.log(checkout_book_btns.length)
    // for (let i = 0; i < checkout_book_btns.length; i++){
    //   console.log("HIHIHI");
    //   console.log(checkout_book_btns[i].getAttributeNames())
    //   checkout_book_btns[i].addEventListener("hover", (event) =>{
    //     event.preventDefault()
    //   });// bookCheckoutModal.bind(checkout_book_btns[i]))
    // }

    var checkout_book_modal_btn = document.getElementById("checkout-book-modal-btn")
    checkout_book_modal_btn.addEventListener("click", bookCheckoutForm)
})
