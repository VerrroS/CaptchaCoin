const work_input = document.querySelector("#work_input");
const work_submit = document.querySelector("#work_submit")
const captcha = document.querySelector("#captcha");
const alert = document.querySelector(".alert");
const stats_container = document.querySelector(".stats_container");
const sound = document.querySelector(".sound");


function position() {
  if (!isMobile)
  {
    console.log(stats_width);
    stats_container.style.setProperty('left', `-${250 + 5}px`);
    stats_container.style.setProperty('top', "20%");
    stats_container.style.setProperty('display', "flex");
  }

  captcha_coords = captcha.getBoundingClientRect()
  if (alert != null)
  {
      if(isMobile && !alert.classList.contains("alert_mobile")){
          alert.classList.add("alert_mobile");
      }
      else if(!isMobile){
          const coords = {
          top: captcha_coords.top - (25),
          left: captcha_coords.left - (25),
        }
          alert.style.setProperty('left', `${coords.left}px`);
          alert.style.setProperty('top', `${coords.top}px`);
      }
      if(localStorage["sound"] != null){
         if (alert.classList.contains("point")){
           document.querySelector(".win").play();
         }
         else{
           document.querySelector(".loose").play();
         }
      }
    }
}

function open_stats() {
  if (stats_container.classList.contains("active")) {
     stats_container.classList.remove("active"); }
  else {
     stats_container.classList.add("active");
 }
}

let time
let start
function timer(e){
 if (e.type == 'click'){
   end = e.timeStamp;
   time = Math.round(end - start)/1000;
   work_submit.value = time;
 }
 else
 {
   if (work_input.dataset.added == "0")
   {
     start = e.timeStamp;
     work_input.dataset.added = "1"
   }
 }
}


function timer_stop(){
 work_input.dataset.added = "0";
}

function sound_toggle(){
 if (localStorage["sound"] == null){
   localStorage["sound"] = "on";
   sound.src = "/static/on.svg"
 }
 else {
   localStorage.removeItem('sound')
    sound.src = "/static/off.svg"
 }
}

function sound_check(){
 if (isMobile){
   sound.classList.add("d-none");
   localStorage.removeItem('sound')
 }
 if (localStorage["sound"] != null){
   sound.src = "/static/on.svg"
 }
 else {
   localStorage.removeItem('sound')
    sound.src = "/static/off.svg"
 }
}


sound.addEventListener('click', sound_toggle);
stats_container.addEventListener('click', open_stats);
window.addEventListener('resize', position);
window.addEventListener('DOMContentLoaded', position);
window.addEventListener('DOMContentLoaded', sound_check);
window.addEventListener('DOMContentLoaded', timer);
work_input.addEventListener('focus', timer);
work_input.addEventListener('focusout', timer_stop);
work_submit.addEventListener('click', timer);
