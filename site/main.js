function responsive_control() {
    // Get the element with the id "myTopnav"
    let x = document.getElementById("topNav");
  
    // Check if the class name of the element is "topnav"
    if (x.className === "topnav") {
      // If it is, add the "responsive" class to the element
      x.className += " responsive";
    } else {
      // If it's not, remove the "responsive" class from the element
      x.className = "topnav";
    }
  }