"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Requests = void 0;
var Requests = /** @class */ (function () {
    function Requests() {
        this.base_url = "";
        this.base_url = "http://" + window.location.host + "/api";
    }
    Requests.prototype.register = function (username, password, email, first_name, last_name, phone) {
        var data = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone
        };
        var results = { "ok": false, "data": "" };
        fetch(this.base_url + "/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
            redirect: "follow"
        }).then(function (response) {
            if (response.status == 200) {
                response.json().then(function (data) {
                    results.ok = true;
                    localStorage.setItem("token", data.token);
                    window.location.href = "/home";
                });
            }
            else {
                response.json().then(function (data) {
                    results.ok = false;
                    results.data = data.message;
                });
            }
        });
        return results;
    };
    Requests.prototype.login = function (username, password) {
        var data = {
            "username": username,
            "password": password
        };
        var results = { "ok": false, "data": "" };
        fetch(this.base_url + "/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
            redirect: "follow"
        }).then(function (response) {
            if (response.status == 200) {
                response.json().then(function (data) {
                    results.ok = true;
                    localStorage.setItem("token", data.token);
                    window.location.href = "/home";
                });
            }
            else {
                response.json().then(function (data) {
                    results.ok = false;
                    results.data = data.message;
                });
            }
        });
        return results;
    };
    Requests.prototype.logout = function () {
        fetch(this.base_url + "/auth/logout", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Token": localStorage.getItem("token") || ""
            },
            redirect: "follow"
        }).then(function (response) {
            localStorage.removeItem("token");
            window.location.href = "/login";
        });
    };
    return Requests;
}());
exports.Requests = Requests;
//# sourceMappingURL=api.js.map