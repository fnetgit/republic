document.addEventListener("DOMContentLoaded", function () {
    const telefoneInput = document.getElementById("telefone");

    telefoneInput.addEventListener("input", function (e) {
        let input = e.target.value;
        input = input.replace(/\D/g, ""); // Remove tudo que não é número

        if (input.length > 0) {
            input = input.replace(/^(\d{0,2})(\d{0,5})(\d{0,4}).*/, function (match, p1, p2, p3) {
                let result = "";
                if (p1) result += "(" + p1;
                if (p1 && p1.length === 2) result += ") ";
                if (p2) result += p2;
                if (p3) result += "-" + p3;
                return result;
            });
        }

        e.target.value = input;
    });
});
