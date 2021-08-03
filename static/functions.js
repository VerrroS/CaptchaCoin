const stats = document.querySelector("#stats");
const stats_container = document.querySelector(".stats_container");
const work_input = document.querySelector("#work_input");
const work_submit = document.querySelector("#work_submit")


$('.robot_ripples').ripples();

function open_stats()
{
  if (stats_container.classList.contains("inactive"))
  {
      stats_container.classList.remove("inactive");
  }
  else {
    stats_container.classList.add("inactive");
  }
}

let time
function timer(e){
  now = Date.now()
  if (e.type == "focus")
  {
    start = e.timeStamp;
    console.log("test", e.timeStamp);
  }
  else
  {
    end = e.timeStamp;
    console.log("test_end", e.timeStamp);
    time = Math.round(end - start)/1000;
    console.log("time", time);
    work_submit.value = time;
  }
}

stats.addEventListener('click', open_stats);
work_input.addEventListener('focus', timer);
work_submit.addEventListener('click', timer);
