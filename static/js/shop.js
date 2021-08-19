
    const items = document.querySelectorAll(".item");
    const btns = document.querySelectorAll(".add_card");
    const cart_container = document.querySelector(".cart_container");
    const cart_value = document.querySelector("input[name=cart_items]");
    var list = [];


    function clear_list(){
      localStorage.removeItem("cart");
    }

    function open_cart(open){
      popoulate_cart();
      if (cart_container.classList.contains("d-none") || open)
      {
        cart_container.classList.remove("d-none");
      }
      else {
        cart_container.classList.add("d-none");
      }
    }

    function popoulate_cart(){
            const li_items = cart_container.querySelectorAll("tr");
            const empty = cart_container.querySelector("#empty");
            console.log(list.length);
            if (list.length < 1 && empty.classList.contains("d-none"))
            {
               empty.classList.remove("d-none");
               console.log("y")
            }
            else
            {
             if (empty.classList.contains("d-none"))
              {
                empty.classList.add("d-none");
                console.log("x")
            }
              li_items.forEach((item, i) => {
                if (list.includes(item.dataset.id)){
                  var close = item.querySelector("button")
                  item.classList.remove("d-none");
                  close.addEventListener("click", remove_item)
                }
               else if (!item.classList.contains("d-none")) {
                 item.classList.add("d-none");
               }
              });
            }
            cart_value.value = list;
    }

    function remove_item(e){
      console.log(this.dataset.id)
      var newlist = list.filter(num => num != this.dataset.id);
      localStorage['cart'] = JSON.stringify(newlist);
      cart_check();
      open_cart(true);
      popoulate_cart();
      cart_value.value = newlist;
    }

    function addto_cart(e){
        list.push(this.value);
        localStorage['cart'] = JSON.stringify(list);
        cart_check();
        open_cart(true);
        window.scrollTo(0,0);
        cart_value.value = list;
    }

    function cart_check(){
      if (localStorage['cart'] != undefined)
      {
          list = JSON.parse(localStorage["cart"]);
      }
      if (list.length > 0)
      {
        const cart_icon = document.querySelector('#cart');
        cart_icon.innerHTML = '<span class="iconify " data-icon="clarity:shopping-cart-outline-badged" style="font-size: 33px;""></span>';
      }
    }

    function show_details(e){
      detail = this.querySelector(".detail");
      detail.classList.toggle("open");
      localStorage.setItem('detail', this.dataset.id);
    }

    items.forEach((item) => {
      item.addEventListener('click', show_details);
    });

    cart_check();

    btns.forEach((item, i) => {item.addEventListener
      ("click", addto_cart)
    });
