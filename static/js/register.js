const cpy_btn = document.querySelectorAll(".cpy_btn")


function copy(e) {
  let copyText = this.dataset.value;
    /* Copy the text inside the text field */
   navigator.clipboard.writeText(copyText);
   this.innerHTML = "Copied";
}

cpy_btn.forEach((item, i) => {
  item.addEventListener('click', copy);
});
