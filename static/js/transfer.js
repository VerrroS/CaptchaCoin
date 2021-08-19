const search = document.querySelector(".search");
const suggestions = document.querySelector(".suggestions");
const results = document.querySelectorAll(".person");
const info_container = document.querySelector(".info_container");
const info_btn = info_container.querySelector(".vertical");


function display_matches(){
  regex = new RegExp(`${search.value}`, "gi")
  results.forEach((item, i) => {
     if(regex.test(item.dataset.name) && search.value.length != 0)
     {
       item.classList.remove("d-none")}

   else if (!item.classList.contains("d-none")){
     item.classList.add("d-none")
   }});
}

 function position(){
   if(isMobile){
     stats_height = info_container.querySelector("form").getBoundingClientRect().height;
     info_container.style.setProperty('top', "0px");
     info_container.style.setProperty('left', "50%");
   }
   else {
     stats_width = info_container.querySelector("form").getBoundingClientRect().width;
     info_container.style.setProperty('left', `-${stats_width + 5}px`);
     info_container.style.setProperty('top', "20%");
   }
 }

 function open_stats() {
   if (info_container.classList.contains("active")) {
      info_container.classList.remove("active"); }
   else {
      info_container.classList.add("active");
  }
  position();
}

  position();
  info_btn.addEventListener('click', open_stats);
  search.addEventListener("change", display_matches);
  search.addEventListener("keyup", display_matches);
  window.addEventListener('resize', position);
