display("userInput", "block")
display("returnedRoutes", "none");

document.addEventListener("DOMContentLoaded", function() {
    click("goButton", function() {
        display("userInput", "none");  
        display("returnedRoutes", "block");
    });
});


