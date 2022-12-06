// function getQuotes(){
//   var res_loc = document.getElementById('res');
//   var list = document.getElementById('res-list');

//   fetch("quote").then(response => {
//       return response.json();
//   }).then(res => {
//       var data = res
      
//       // clear list
//       while (list.lastChild) {
//           list.removeChild(list.lastChild);
//       }
      
//       // populate list
//       for (var i = 0; i < data.length; i++){
//           list.innerHTML += `<li class='list-group-item'>` + data[i].quote + " - " + data[i].author + `</li>`;
//       }
      
//       // insert response
//       res_loc.textContent = JSON.stringify(data, null, 2);
      
//       console.log(data);
//   }).catch(err => {
//       // Do something for an error here
//   });
// }

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
      
  }).catch(err => {
      // Do something for an error here
  });
}

function bookCheckoutModal(isbn, title){
  
  var modal_elem = document.getElementById('checkout-book-card-id');
  var modal_book_title_elem = document.getElementById('checkout-book-title');
 
  // Set modal data for /book/checkout request 
  modal_elem.setAttribute("isbn", isbn);
  modal_book_title_elem.innerText = title;

  // Remove old alerts
  var alert_elem = document.getElementById('checkout-book-alert')
  while (alert_elem.lastChild) {
    alert_elem.removeChild(alert_elem.lastChild);
  }
}

function bookCheckoutForm(event){
  event.preventDefault()
  var checkout_book_form = document.getElementById("checkout-book-form")

  // Form Validation
  if (!checkout_book_form.checkValidity()) {
    event.stopPropagation();
    checkout_book_form.classList.add('was-validated');
    return
  }
  checkout_book_form.classList.add('was-validated');

  // Get query parameters
  var isbn = document.getElementById('checkout-book-card-id').getAttribute("isbn");
  var card_id = parseInt(document.getElementById('checkout-book-card-id').value.substring(2));
  var alert_elem = document.getElementById('checkout-book-alert');
  
  // Build query
  var base_query = "book/checkout";
  var query = base_query + "?isbn=" + isbn + "&card_id=" + card_id;

  // API Call
  fetch(query, { 
    method: "POST"
  }).then(response => {
    return response.json().then(data => ({status: response.status, message: data.message, data: data}));
  }).then(res => {

    // Remove Old Alert
    while (alert_elem.lastChild) {
      alert_elem.removeChild(alert_elem.lastChild);
    }
    
    if (res.status != 200) { // Not Successful Checkout
      alert_elem.innerHTML += `
      <div class="alert alert-warning d-flex align-items-center alert-dismissible fade show" role="alert">
        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Warning:"><use xlink:href="#exclamation-triangle-fill"/></svg>
        <div>
          <strong>Error:</strong> ` + res.message + `
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
      </div>
      `;
    } else {  // Successful Checkout
      alert_elem.innerHTML += `
      <div class="alert alert-success d-flex align-items-center alert-dismissible fade show" role="alert">
        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
        <div>
          ` + res.message + `
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
      `;
    }

  }).catch(err => {
    // Do something for an error here
  });
}

function bookCheckinSearch(){

  var book_loan_list = document.getElementById('book-checkin-res');

  var search_query = {
    q: document.getElementById('bookCheckinQuery').value,
    p: 1
  }

  if (search_query.q === null || search_query.q === "") return

  var base_query = "book/checkin"
  var query = base_query + "?q=" + search_query.q // + "&p=" + search_query.p

  fetch(query).then(response => {
      return response.json();
  }).then(res => {
      var data = res
      
      // @TODO: Remove dummy data and clear list operation
      // clear list
      while (book_loan_list.lastChild) {
        book_loan_list.removeChild(book_loan_list.lastChild);
      }
      
      // no books match query
      if (data.length === 0){
        book_loan_list.innerHTML += `<h3 style="text-align:center;">No book loans found.</h3>`
      }

      // populate list
      for (var i = 0; i < data.length; i++){
        book_loan_list.innerHTML += `<li id="book-loan-`+ data[i].Loan_id + `" isbn="` + data[i].Isbn + `" class="card m-2 box-shadow dummy d-flex flex-md-row align-items-center">
            <div class="card-body d-flex flex-column align-items-start">
              <h3>` + data[i].Isbn + `</h3>
              <p class="card-test mb-auto">Checked out by: ` + data[i].Bname.replace("'", "\\'") + `</p>
              <p class="card-test mb-auto">Card ID: ID` +  ("00000" + data[i].Card_id).slice(-6) + `</p>
              <div class="mb-1 text-muted" id="book-due-` + i + `">Checked out: ` + data[i].Date_out + `, Due: ` + data[i].Due_date + `</div>
            </div>
            <div class="col-2 align-self-center m-4 mt-0 mb-2">
              <button onclick="bookCheckin('` + data[i].Loan_id + `')" class="btn btn-primary p-2 checkin-book-btn" type="button">Check-in Book</button>
            </div>
        </li>`
      }
      
  }).catch(err => {
      // Do something for an error here
  });
}

function bookCheckin(loan_id){
  
  var book_loan_list = document.getElementById('book-checkin-res');
  var loan_elem = document.getElementById('book-loan-' + loan_id);
  
  var base_query = "book/checkin"
  var query = base_query + "?loan_id=" + loan_id

  // Remove old alerts
  // var alert_elem = document.getElementById('checkout-book-alert')
  // while (alert_elem.lastChild) {
  //   alert_elem.removeChild(alert_elem.lastChild);
  // }

  fetch(query, { 
    method: "POST"
  }).then(response => {
    book_loan_list.removeChild(loan_elem)
    return response.json().then(data => ({status: response.status, message: data.message, data: data}));
  }).then(res => {
    
    if (res.status != 400) { // Not Successful Checkout
      alert(res.message)
    } else {  // Successful Checkout
      console.log(res.message)
    }

  }).catch(err => {
    // Do something for an error here
  });
}

function createBorrower(){
  
  // var borrower_list = document.getElementById('book-search-res');
  var ssn = document.getElementById('validationSSN').value;
  var name = document.getElementById('validationName').value;
  var address = document.getElementById('validationAddress').value;
  var phone = document.getElementById('validationPhone').value;

  var alert_elem = document.getElementById('borrower-alert')

  var base_query = "borrower/create"
  var query = base_query + "?ssn=" + ssn + "&name=" + name + "&address=" + address + "&phone=" + phone

  fetch(query, { 
    method: "POST"
  }).then(response => {
    return response.json().then(data => ({status: response.status, message: data.message, data: data}))
  }).then(res => {
      
    // Remove old alerts
    while (alert_elem.lastChild) {
      alert_elem.removeChild(alert_elem.lastChild);
    }
    
    if (res.status != 200) { // Not Successful Creation
      alert_elem.innerHTML += `
      <div class="alert alert-warning d-flex align-items-center alert-dismissible fade show" role="alert">
        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Warning:"><use xlink:href="#exclamation-triangle-fill"/></svg>
        <div>
          <strong>Error:</strong> ` + res.message + `
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
      </div>
      `
    } else { // Successful Creation
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

  }).catch(err => {
      // Do something for an error here
  });
}

function getFines(){
  
  var fines_list = document.getElementById('fines-res');
  var paid = false

  var base_query = "fines/all"
  var query;
  if (!paid){
    query = base_query
  } else {
    query = base_query + "?paid=FALSE"
  }

  fetch(query).then(response => {
    return response.json()
  }).then(res => {

    var data = res

    console.log(data)

    while (fines_list.lastChild) {
      fines_list.removeChild(fines_list.lastChild);
    }

    var prev_id = -1;
    var fine_group = "";
    var base_elem_start = `<li class="card m-2 box-shadow dummy d-flex flex-md-row align-items-center">
      <div class="card-body d-flex flex-column align-items-start">`;
    var elem_mid = ""
    var fine_amt = 0;
    
    var base_elem_end = "</ul></li>";  

    console.log("Data: ")
    console.log(data)

    for (var i = 0; i < data.length; i++){
      var fine = data[i]
      if (fine.Card_id == prev_id){
        console.log("HI")
        fine_group += `
          <li class="card m-2 box-shadow dummy d-flex flex-md-row align-items-center">
            <div class="card-body d-flex flex-column align-items-start">
              <p class="card-test mb-auto">ISBN: ` + fine.Isbn + `, Due: ` +  fine.Due_date + `</p>
              <p class="card-test mb-auto">Fine Amount: ` +  (fine.Fine_amt/100).toFixed(2) + ", Paid: <b>" + p + `</b></p>
            </div>
            <div class="col-2 align-self-center m-4 mt-0 mb-2">
              <button onclick="bookCheckin('` + fine.Loan_id + `')" class="btn btn-primary p-2 checkin-book-btn" type="button">Check-in Book</button>
            </div>
          </li>`
        fine_amt += fine.Fine_amt
      } else {
        console.log("DUP")
        var p = -1;
        if(fine.Paid == 0) {
          p = "No"
        } else {
          p = "Yes"
        }

        console.log(prev_id)
        elem_mid = "<h3>Card ID: ID" + ("00000" + data[i].Card_id).slice(-6) + "</h3><h5>Total Fine: " + (fine_amt/100).toFixed(2) + `</h5><ul class="list-group col-12">`
        if (prev_id != -1){
          console.log("ADD")
          fines_list.innerHTML += base_elem_start + elem_mid + fine_group + base_elem_end;
        }
        fine_amt = fine.Fine_amt
        fine_group = `
          <li class="card m-2 box-shadow dummy d-flex flex-md-row align-items-center">
            <div class="card-body d-flex flex-column align-items-start">
              <p class="card-test mb-auto">ISBN: ` + fine.Isbn + `, Due: ` +  fine.Due_date + `</p>
              <p class="card-test mb-auto">Fine Amount: ` +  (fine.Fine_amt/100).toFixed(2) + ", Paid: <b>" + p + `</b></p>
            </div>
            <div class="col-2 align-self-center m-4 mt-0 mb-2">
              <button onclick="bookCheckin('` + fine.Loan_id + `')" class="btn btn-primary p-2 checkin-book-btn" type="button">Check-in Book</button>
            </div>
          </li>`
        prev_id = fine.Card_id
      }
    }
    // fine = data[data.length-1]
    // if(fine.Paid == 0) {
    //   p = "No"
    // } else {
    //   p = "Yes"
    // }
    // elem_mid = "<h3>" + fine.Card_id + "</h3><h5>Total Fine: " + (Fine_amt/100).toFixed(2) + `</h5><ul class="list-group mt-2">`
    // if (prev_id != -1){
    //   console.log("ADD")
    //   fines_list.innerHTML += base_elem_start + elem_mid + fine_group + base_elem_end;
    // }
  }).catch(err => {
    // Do something for an error here
  });

}

function updateFines(){
  var query ="fines/update"
  fetch(query, {
    method: "PUT"
  }).then(response => {
    return response.json()
  }).then(res => {
    getFines();
  }).catch(err => {
    // Do something for an error here
  });

}

window.addEventListener("load", () => {
    // var button = document.getElementById("res-btn");
    // button.addEventListener("click", getQuotes);

    var book_search_input = document.getElementById("bookSearchQuery");
    book_search_input.addEventListener("keypress", (event) => {
      if (event.key === "Enter"){
        event.preventDefault();
        book_search_input.blur();
        bookSearch();
      }
    });
    
    var book_search_btn = document.getElementById("book-search-btn");
    book_search_btn.addEventListener("click", bookSearch);

    var checkout_book_modal_btn = document.getElementById("checkout-book-modal-btn");
    checkout_book_modal_btn.addEventListener("click", bookCheckoutForm);

    var book_checkin_input = document.getElementById("bookCheckinQuery");
    book_checkin_input.addEventListener("keypress", (event) => {
      if (event.key === "Enter"){
        event.preventDefault();
        book_checkin_input.blur();
        bookCheckinSearch();
      }
    });

    var book_checkin_btn = document.getElementById("book-checkin-btn");
    book_checkin_btn.addEventListener("click", bookCheckinSearch);

    var book_checkin_btn = document.getElementById("update-fines-btn");
    book_checkin_btn.addEventListener("click", updateFines);

    getFines()
})
