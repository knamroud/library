"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var api_1 = require("./api");
window.onload = function () {
    var api = new api_1.Requests();
    var register_form = document.getElementById("register-form");
    register_form === null || register_form === void 0 ? void 0 : register_form.addEventListener("submit", function (event) {
        var _a, _b, _c, _d, _e, _f, _g;
        event.preventDefault();
        var password = (_a = document.getElementById("password")) === null || _a === void 0 ? void 0 : _a.value;
        var password_confirm = (_b = document.getElementById("password_confirm")) === null || _b === void 0 ? void 0 : _b.value;
        if (password != password_confirm) {
            alert("Passwords do not match");
            return;
        }
        var results = api.register((_c = document.getElementById("username")) === null || _c === void 0 ? void 0 : _c.value, password, (_d = document.getElementById("email")) === null || _d === void 0 ? void 0 : _d.value, (_e = document.getElementById("first_name")) === null || _e === void 0 ? void 0 : _e.value, (_f = document.getElementById("last_name")) === null || _f === void 0 ? void 0 : _f.value, (_g = document.getElementById("phone")) === null || _g === void 0 ? void 0 : _g.value);
        if (!results.ok) {
            alert(results.data);
        }
    });
};
//# sourceMappingURL=register.js.map