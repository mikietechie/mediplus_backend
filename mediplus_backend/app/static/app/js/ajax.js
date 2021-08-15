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