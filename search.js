const template = Handlebars.compile(document.querySelector('#book_card').innerHTML);

document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('form').onsubmit = function () {

    request = new XMLHttpRequest();
    request.open('POST','/convert');
    const search_by = document.querySelector('#search_by').value;
    const search_book = document.querySelector('#search_book').value;

    const addon = new FormData();
    addon.append('search_by',search_by);
    addon.append('search_book',search_book);
    request.send(addon);

    request.onload = function () {
      const data = JSON.parse(this.responseText);
      console.log(data);
      if (data["success"]){
        books = data["books"];
        content = template({books:books})
      }
      else{
        content = data["error"];
      }


      document.querySelector('#books').innerHTML += content;
