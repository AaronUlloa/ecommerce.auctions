// var modals = document.getElementsByClassName("modal");
// var spans = document.getElementsByClassName("close");

// for (var i = 0; i < spans.length; i++) {
//   spans[i].onclick = function () {
//     var modal = this.parentNode.parentNode;
//     modal.style.display = "none";
//   };
// }

// window.onclick = function (event) {
//   for (var i = 0; i < modals.length; i++) {
//     if (event.target == modals[i]) {
//       modals[i].style.display = "none";
//     }
//   }
// };
var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];

span.onclick = function () {
  modal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};
// var modalLinks = document.getElementsByClassName("modal-link");

// for (var i = 0; i < modalLinks.length; i++) {
//   modalLinks[i].addEventListener("click", function () {
//     var target = this.getAttribute("data-target");
//     var modal = document.getElementById(target);
//     modal.style.display = "block";
//   });
// }







