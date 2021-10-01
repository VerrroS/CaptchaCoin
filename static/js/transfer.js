const search = document.querySelector(".search");
const suggestions = document.querySelector(".suggestions");
const results = document.querySelectorAll(".person");
const adress_btn = document.querySelector(".adress_btn");
const adress = document.querySelector(".adress");
const download_btn = document.querySelectorAll("#download");


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


 function open_stats() {
   if (info_container.classList.contains("active")) {
      info_container.classList.remove("active"); }
   else {
      info_container.classList.add("active");
  }
}

  function open_stats_mobile(){
    console.log("open");
    const info_field = document.createElement('div');
    const form = info_container.innerHTML;
    console.log(form);
    info_field.innerHTML = form;
    adress.append(info_field);
  }

  function choose_person(e){
    let key = this.querySelector("span").innerHTML;
    search.value = key;
  }


function post_download(e){
  let id = this.dataset.id;
  $.get( "/download/", {
    download_id: "robot.jpg"
    });
}

  download_btn.forEach((item, i) => {
    item.addEventListener("click", post_download);
  });

  search.addEventListener("change", display_matches);
  search.addEventListener("keyup", display_matches);
  results.forEach((item, i) => {
  item.addEventListener("click", choose_person);
  });
