let cookies = document.cookie.split(";")
let CSRF_MiddlewareToken = null
for(let cookieString of cookies) {
    if (cookieString.startsWith("csrftoken")) {
        CSRF_MiddlewareToken = cookieString.split("=")[1].trim()
        break;
    }
}

const postFormData = (action, formData) => fetch(action, {
    method: 'POST',
    body: formData,
    headers: {'X-Requested-With': 'XMLHttpRequest'}
  })

const sendEmail = (fromEmail, subject, message, toEmail=null, csrfmiddlewaretoken=null) => {
    let formData = new FormData()
    let currentcsrfmiddlewaretoken = csrfmiddlewaretoken || CSRF_MiddlewareToken
    formData.append("from_email", fromEmail)
    formData.append("to_email", toEmail)
    formData.append("csrfmiddlewaretoken", currentcsrfmiddlewaretoken)
    formData.append("subject", subject)
    formData.append("message", message)
    return postFormData("/api/email/", formData)
}

const sendReaction = (user, model, instance_id, is_like, expression) => {
    let formData = new FormData()
    formData.append("csrfmiddlewaretoken", CSRF_MiddlewareToken)
    formData.append("user", user)
    formData.append("model", model)
    formData.append("instance_id", instance_id)
    formData.append("is_like", is_like)
    formData.append("expressexpression", expression)
    return postFormData("api/generic_api_view/reaction/data/", formData)
}

(function () {
    "use strict";
    const directPostForms = document.querySelectorAll(".direct-post-form")

    directPostForms.forEach((form) => {
        form.addEventListener(("submit"), (event) => {
            event.preventDefault();

            let thisForm = this;
            let action = thisForm.getAttribute("action")
            //  let recaptcha = thisForm.getAttribute('data-recaptcha-site-key');

            if (! action) {
                alert("The form's action property is not set!")
                return;
            }

            let formData = new FormData(thisForm)
            /*
            if ( recaptcha ) {
                if(typeof grecaptcha !== "undefined" ) {
                    grecaptcha.ready(function() {
                        try {
                            grecaptcha.execute(recaptcha, {action: 'main_email_form_submit'})
                            .then(token => {
                            formData.set('recaptcha-response', token);
                            return postFormData(action, formData);
                            })
                        } catch(error) {
                            alert(`${error}`)
                        }
                    });
                } else {
                    alert('The reCaptcha javascript API url is not loaded!')
                }
            } else {
            return postFormData(action, formData);
            }
            */
            postFormData(action, formData)
            .then(
                response => {
                    if (response.ok) {
                        return response.text()
                    } else {
                        throw new Error(`${response.status} ${response.statusText} ${response.url}`)
                    }
                }
            )
            .then(data => {
                if (thisForm.getAttribute("on-successful-post")) {
                    return eval(`${thisForm.getAttribute("on-successful-post")}(${data})`)
                } else {
                    try {
                        thisForm.querySelector('.sent-message').style.display="block";
                    } catch (error) {}
                    try {
                        thisForm.querySelector('.loading').style.display="none";
                    } catch (error) {}
                    thisForm.reset(); 
                }
            })
            .catch((error) => {
                try {
                    thisForm.querySelector('.error-message').style.display="block";
                } catch (error) {}
                try {
                    thisForm.querySelector('.loading').style.display="none";
                } catch (error) {}
            })

        })
    })
})();