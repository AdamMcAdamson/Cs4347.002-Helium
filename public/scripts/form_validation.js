window.addEventListener("load", () => {
  'use strict'

  var borrowerManagementForm = document.querySelector('#borrower-management-form')
  borrowerManagementForm.addEventListener('submit', function(event){
    event.preventDefault()
    if (!borrowerManagementForm.checkValidity()) {
      event.stopPropagation()
      borrowerManagementForm.classList.add('was-validated')
      return
    }
    createBorrower()
    
    borrowerManagementForm.classList.add('was-validated')
  }, false)


  var bookSearchForm = document.querySelector('#book-search-form')
  bookSearchForm.addEventListener('submit', function(event){
    event.preventDefault()
  }, false)

  var bookSearchForm = document.querySelector('#book-checkin-form')
  bookSearchForm.addEventListener('submit', function(event){
    event.preventDefault()
  }, false)
})