(function myFunction() {
    function display(id, value) {
        document.getElementById(id).style.display = value;
    }

    function click(id, fn) {
        document.getElementById(id).addEventListener("click", fn);
    }

    document.addEventListener("DOMContentLoaded", function() {
        
        click("backButton", function() {
            display("userInput", "block");
            display("returnedRoutes", "none");
        });

        click("goButton", function() {
            display("userInput", "none");
            display("returnedRoutes", "block");
        });
    });
}())