window.addEventListener("load", () => {
  'use strict'

  // @TODO: Include validation code for each form which requires it
  // and remove global default validation code below:
  /*
  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')
  
  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
  .forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }
      form.classList.add('was-validated')
    }, false)
  })  
  */

  var borrowerManagementForm = document.querySelector('#borrower-management-form')
  borrowerManagementForm.addEventListener('submit', function(event){
    event.preventDefault()
    if (!borrowerManagementForm.checkValidity()) {
      event.stopPropagation()
      borrowerManagementForm.classList.add('was-validated')
      return
    }
    createBorrower()
    
    // @TODO: Call borrower/create endpoint and handle duplicate SSN error
    borrowerManagementForm.classList.add('was-validated')
  }, false)


  var bookSearchForm = document.querySelector('#book-search-form')
  bookSearchForm.addEventListener('submit', function(event){
    event.preventDefault()
    // @TODO: Fetch Search endpoint and populate table
  }, false)
})