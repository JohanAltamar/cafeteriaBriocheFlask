const toggleDrawer = () => {
  if (drawer.classList.contains("toggleVisibilityFlex")) {
    drawerContainer.classList.remove("fadeInLeft");
    drawerContainer.classList.add("fadeOutLeft");
    drawer.classList.add("background-out");
    drawer.classList.remove("background-in");

    setTimeout(() => {
      drawer.classList.remove("toggleVisibilityFlex");
    }, 800);
  } else {
    drawer.classList.add("toggleVisibilityFlex");
    drawerContainer.classList.add("fadeInLeft");
    drawerContainer.classList.remove("fadeOutLeft");
    drawer.classList.remove("background-out");
    drawer.classList.add("background-in");
  }
};

const collapseItem = (element) => {
  console.log(element);
  const sibling = element.nextElementSibling;
  const chevronDown = element.getElementsByTagName("i")[1];
  const chevronUp = element.getElementsByTagName("i")[2];

  if (sibling.style.maxHeight) {
    sibling.style.maxHeight = null;
    sibling.classList.remove("toggleVisibilityBlock");
    chevronDown.style.display = "block";
    chevronUp.style.display = "none";
  } else {
    chevronDown.style.display = "none";
    chevronUp.style.display = "block";
    sibling.classList.add("toggleVisibilityBlock");
    sibling.style.maxHeight = sibling.scrollHeight + "px";
  }
};

const menuButton = document.getElementsByClassName("menu-button")[0];
const drawer = document.getElementsByClassName("drawer")[0];
const drawerContainer = document.getElementsByClassName("drawer-container")[0];
const drawerBackground = document.getElementsByClassName(
  "drawer-background"
)[0];

menuButton.addEventListener("click", toggleDrawer);
drawerBackground.addEventListener("click", toggleDrawer);

const drawerItems = document.getElementsByClassName("drawer-list-item");

for (let i = 0; i < drawerItems.length; i++) {
  const element = drawerItems[i];
  element.addEventListener("click", () => collapseItem(element));
}
