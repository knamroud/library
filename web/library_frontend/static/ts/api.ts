export { Requests };
class Requests {
    base_url = "";
    constructor() {
        this.base_url = "http://" + window.location.host + "/api";
    }

    register(username: string, password: string, email: string, first_name: string, last_name: string, phone: string) {
        let data = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone
        };
        let results = { "ok": false, "data": "" };
        fetch(this.base_url + "/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
            redirect: "follow"
        }).then(response => {
            if (response.status == 200) {
                response.json().then(data => {
                    results.ok = true;
                    localStorage.setItem("token", data.token);
                    window.location.href = "/home";
                });
            }
            else {
                response.json().then(data => {
                    results.ok = false;
                    results.data = data.message;
                });
            }
        }
        );
        return results;
    }

    login(username: string, password: string) {
        let data = {
            "username": username,
            "password": password
        };
        let results = { "ok": false, "data": "" };
        fetch(this.base_url + "/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
            redirect: "follow"
        }).then(response => {
            if (response.status == 200) {
                response.json().then(data => {
                    results.ok = true;
                    localStorage.setItem("token", data.token);
                    window.location.href = "/home";
                });
            }
            else {
                response.json().then(data => {
                    results.ok = false;
                    results.data = data.message;
                });
            }
        });
        return results;
    }

    logout() {
        fetch(this.base_url + "/auth/logout", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Token": localStorage.getItem("token") || ""
            },
            redirect: "follow"
        }).then(response => {
            localStorage.removeItem("token");
            window.location.href = "/login";
        });
    }
}
