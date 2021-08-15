
(() => {
    let emailForm = document.querySelector("#email-form");
    if (emailForm) {
        document.querySelector(".show-loading").style.display = "none";
        document.querySelector(".show-error").style.display = "none";
        document.querySelector(".show-success").style.display = "none";
        const displayLoading = () => {
            document.querySelector(".show-loading").style.display = "block";
            document.querySelector(".show-error").style.display = "none";
            document.querySelector(".show-success").style.display = "none";
        }
        const displaySuccess = () => {
            document.querySelector(".show-loading").style.display = "none";
            document.querySelector(".show-error").style.display = "none";
            document.querySelector(".show-success").style.display = "block";
        }
        const displayError = () => {
            document.querySelector(".show-loading").style.display = "none";
            document.querySelector(".show-error").style.display = "block";
            document.querySelector(".show-success").style.display = "none";
        }
        emailForm.addEventListener("submit", (e) => {
            e.preventDefault();
            let email = emailForm.querySelector("#email").value;
            let name = emailForm.querySelector("#name").value;
            let subject = emailForm.querySelector("#subject").value;
            let message = emailForm.querySelector("#message").value;
            let processedMessage = `${message}\nFrom ${name}`;
            displayLoading();
            sendEmail(email, subject, processedMessage, toEmail=null, csrfmiddlewaretoken=null)
            .then((res) => {
                if (res.ok) {
                    displaySuccess()
                    emailForm.reset();
                } else {
                    displayError()
                }
            })
            .catch(() => {displayError()})  
        })
    }
})()