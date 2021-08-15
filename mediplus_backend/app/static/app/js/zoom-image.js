document.addEventListener("DOMContentLoaded", () => {
    let modalElement = document.createElement("div")
    modalElement.innerHTML = `
    <div class="modal fade" id="view-image-modal" style="opacity: 0.9;" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="view-image-modal-label" aria-hidden="true">
        <div class="modal-dialog modal-fullscreen">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="view-image-modal-label"></h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body text-center justify-content-center">
                    <img src="" class="mx-auto my-auto" alt="" style="max-width: 80vw; max-height: 80vh;">
                </div>
                <div class="modal-footer">
                    <p class="text-center"></p>
                </div>
            </div>
        </div>
    </div>
    `;
    document.querySelector("body").appendChild(modalElement);
    let zoomableImages = document.querySelectorAll(".zoomable-image");
    let viewImageModal = document.getElementById("view-image-modal");
    zoomableImages.forEach((zoomableImage) => {
        zoomableImage.setAttribute("data-bs-toggle", "modal")
        zoomableImage.setAttribute("data-bs-target", "#view-image-modal")
        zoomableImage.addEventListener("click", (e) => {
            viewImageModal.querySelector("h5").innerHTML = zoomableImage.getAttribute("title");
            viewImageModal.querySelector("p").innerHTML = zoomableImage.getAttribute("alt");
            viewImageModal.querySelector("img").src  = zoomableImage.getAttribute("src");
        })
    })

})