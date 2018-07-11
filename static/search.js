const template = Handlebars.compile(document.querySelector('#book_card').innerHTML);

document.addEventListener('DOMContentLoaded', function() {
      document.querySelector('form').onsubmit = function() {

        request = new XMLHttpRequest();
        request.open('POST', '/searching');
        const search_by = document.querySelector('#search_by').value;
        const search_book = document.querySelector('#search_book').value;

        const addon = new FormData();
        addon.append('search_by', search_by);
        addon.append('search_book', search_book);
        request.send(addon);

        request.onload = function() {
          document.querySelector('#books').innerHTML = '';
          const data = JSON.parse(this.responseText);

          const message = data["message"]


          document.querySelector('#message').innerHTML = message;
          if (data["success"]) {
            const titles = data["titles"]
            const authors = data["authors"]
            const ids = data["ids"]
            console.log(titles);
            for(var i=0;i<titles.length;i++)
            {
              const content = template({"title":titles[i],"author":authors[i],"id":ids[i]});
              document.querySelector('#books').innerHTML += content;
            }
          }
          // else {
          //   const content = data["error"];
          //   document.querySelector('#books').innerHTML += content;
          // }



        }

        return false;
      };
    });
