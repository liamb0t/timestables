const customSelectBtn = document.getElementById('custom-select');
const options = document.getElementById("selectOptions");

customSelectBtn.addEventListener('click', toggleOptions)

function toggleOptions() {
    if (options.style.display === "none") {
      options.style.display = "block";
      document.addEventListener("click", handleOutsideClick);
    } else {
      options.style.display = "none";
      document.addEventListener("click", handleOutsideClick);
    }
}

function handleOutsideClick(event) {
    
    if (!options.contains(event.target) && !customSelectBtn.contains(event.target)) {
        options.style.display = "none";
        document.removeEventListener("click", handleOutsideClick);
    }
}
  