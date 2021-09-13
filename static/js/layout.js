const body = document.querySelector('body');
const nav_desk = document.querySelector('.navbar-desktop');
const nav_mobile = document.querySelector('.navbar-mobile');
const burger_btn = document.querySelector('.burger_btn');
const menu = nav_mobile.querySelector('.menu');

function layout() {
  if(body.classList.contains('mobile'))
  {
      nav_desk.classList.add('d-none');
      nav_mobile.classList.remove('d-none');
  }
}

function open_menu(){
  if(menu.classList.contains('closed'))
  {
     menu.classList.remove('closed');
  }
  else {
    menu.classList.add('closed');
  }
}

function close_menu() {
  menu.classList.remove('closed');
}

window.addEventListener('DOMContentLoaded', layout);
burger_btn.addEventListener('click', open_menu);
