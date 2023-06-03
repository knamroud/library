window.onload = function () {
    // use api.ts to register a new user
    let api = new Requests();
    let register_form = document.getElementById("register-form");
    register_form?.addEventListener("submit", function (event) {
        event.preventDefault();
        let password = (<HTMLInputElement>document.getElementById("password"))?.value;
        let password_confirm = (<HTMLInputElement>document.getElementById("password-confirm"))?.value;
        if (password != password_confirm) {
            alert("Passwords do not match");
            return;
        }
        let results = api.register((<HTMLInputElement>document.getElementById("username"))?.value, password, (<HTMLInputElement>document.getElementById("email"))?.value, (<HTMLInputElement>document.getElementById("first-name"))?.value, (<HTMLInputElement>document.getElementById("last-name"))?.value, (<HTMLInputElement>document.getElementById("phone"))?.value);
        if (!results.ok) {
            alert(results.data);
        }
    });
}