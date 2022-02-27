
   
    let searchForm = document.getElementById('searchForm')
    let pageLinks = document.getElementsByClassName('page-link')

    if(searchForm){
        for(let i=0; pageLinks.length > i; i++){
            pageLinks[i].addEventListener('click',function (e){
                e.preventDefault()
                console.log('button-click')

            let page = this.dataset.page
            console.log('page',page)
            searchForm.innerHTML +=`<input value=${page} name="page" hidden />`
            searchForm.submit()
            })
        }
    }

  