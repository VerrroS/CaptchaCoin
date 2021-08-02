const stats = document.querySelector("#stats");
const stats_container = document.querySelector("#stats_container");

function open_stats()
{
  if (stats_container.classList.contains("hidden"))
  {
      stats_container.classList.remove("hidden");
  }
  else {
    stats_container.classList.add("hidden");
  }
}

stats.addEventListener('click', open_stats);
