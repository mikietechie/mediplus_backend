(() => {
    "use strict";

    const postFormData = (action, formData) => fetch(action, {
      method: 'POST',
      body: formData,
      headers: {'X-Requested-With': 'XMLHttpRequest'}
  })
  
    /**
     * Easy selector helper function
     */
    const select = (el, all = false) => {
      el = el.trim()
      if (all) {
        return [...document.querySelectorAll(el)]
      } else {
        return document.querySelector(el)
      }
    }
  
    /**
     * Easy event listener function
     */
    const on = (type, el, listener, all = false) => {
      let selectEl = select(el, all)
      if (selectEl) {
        if (all) {
          selectEl.forEach(e => e.addEventListener(type, listener))
        } else {
          selectEl.addEventListener(type, listener)
        }
      }
    }
    const getValue = (element) => element.value
    const getInputValue = (inputID) => getValue(select(inputID))
    const setValue = (element, value) => {element.value = value}
    const setInputValue = (inputID, value) => setValue(select(inputID), value)
    const focus = (inputID) => select(inputID).focus()
    const scrollTo = (inputID) => window.scrollTo(0, select(inputID).offsetTop)
    const getAttr = (element, attr) => element.getAttribute(attr)
    const onclicked = (element, listener) => element.addEventListener("click", listener)
  
    /**
     * Easy on scroll event listener 
     */
    const onscroll = (el, listener) => {
      el.addEventListener('scroll', listener)
    }
  
    /**
     * Easy on submit event listener 
     */
    const onsubmit = (el, listener) => {
      el.addEventListener('submit', listener)
    }
  
    /**
     * Back to top button
     */
    let $backtotop = select('.back-to-top')
    if ($backtotop) {
      const toggleBacktotop = () => {
        if (window.scrollY > 100) {
          $backtotop.classList.add('active')
        } else {
          $backtotop.classList.remove('active')
        }
      }
      window.addEventListener('load', toggleBacktotop)
      document.addEventListener("scroll", toggleBacktotop)
    }

    /**
     * Preloader
     */
    let preloader = select('#preloader');
    if (preloader) {
        window.addEventListener("load", () => preloader.remove())
    }
  
    /**
     * Navbar links active state on scroll
     */
    
    let navbarlinks = select('#navbar .scrollto', true)
    const navbarlinksActive = () => {
      navbarlinks.forEach(navbarlink => {
        if (!navbarlink.href) return
        if (window.location.pathname === navbarlink.pathname){
          navbarlink.classList.add('active')
        } else {
          navbarlink.classList.remove('active')
        }
      })
      /*
      let position = window.scrollY + 200
      navbarlinks.forEach(navbarlink => {
        if (!navbarlink.hash) return
        let section = select(navbarlink.hash)
        if (!section) return
        if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
          navbarlink.classList.add('active')
        } else {
          navbarlink.classList.remove('active')
        }
      })*/
    }
    window.addEventListener('load', navbarlinksActive)
    //  onscroll(document, navbarlinksActive)
    
  
    /**
     * Toggle .header-scrolled class to #header when page is scrolled
     */
    let $selectHeader = select('#header')
    if ($selectHeader) {
      const headerScrolled = () => {
        if (window.scrollY > 100) {
          $selectHeader.classList.add('header-scrolled')
        } else {
          $selectHeader.classList.remove('header-scrolled')
        }
      }
      window.addEventListener('load', headerScrolled)
      onscroll(document, headerScrolled)
    }
  
    /**
     * Mobile nav toggle
     */
    on('click', '.mobile-nav-toggle', function(e) {
      select('#navbar').classList.toggle('navbar-mobile')
      this.classList.toggle('bx-menu')
      this.classList.toggle('bx-window-close')
    })
  
    /**
     * Mobile nav dropdowns activate
     */
    on('click', '.navbar .dropdown > a', function(e) {
      if (select('#navbar').classList.contains('navbar-mobile')) {
        e.preventDefault()
        this.nextElementSibling.classList.toggle('dropdown-active')
      }
    }, true)

    /**
     * Snackbar service
     */
    let $snackbar = document.querySelector(".snackbar")
    let $snackbarAlert = $snackbar.querySelector(".alert")
    let $snackbarMessage = $snackbarAlert.querySelector(".snackbar-message")
    $snackbar.querySelector("button").addEventListener("click", () => {
        $snackbar.querySelector(".snackbar-message").innerHTML = ''
        $snackbar.style.visibility = "hidden"
    })
    /**
     * Show snackbar func
     */
    const showSnackbar = (message, _class="info") => {
        $snackbarAlert.classList.replace($snackbarAlert.classList[2], `alert-${_class}`)
        $snackbarMessage.innerHTML = `${$snackbarMessage.innerHTML}` + message
        $snackbar.style.visibility = "visible"
    }
    /**
   * Snackbar service
   */
      let $alertbar = select(".alertbar")
      let $alertbarAlert = $alertbar.querySelector(".alert")
      let $alertbarQuestion = $alertbarAlert.querySelector(".alertbar-question")
      let $alertbarPositiveButton = $alertbarAlert.querySelector(".positive")
      let $alertbarNegativeButton = $alertbarAlert.querySelector(".negative")
      let $alertbarCloseButton = $alertbarAlert.querySelector(".btn-close")
      /**
      * Show alertbar func
      */
      const closeAlertBar = () => {
          $alertbar.querySelector(".alertbar-question").innerHTML = ''
          $alertbar.style.visibility = "hidden"
      }
      const showAlertbar = (
        question, on_confirm=()=>null, on_reject=()=>null,  _class="dark",
        positive=`<i class="bx bx-circle"></i> Yes`,
        negative=`<i class="bx bx-x"></i> No`
        ) => {
          $alertbarAlert.classList.replace($alertbarAlert.classList[2], `alert-${_class}`)
          $alertbarQuestion.innerHTML = question
          $alertbarPositiveButton.innerHTML = positive
          $alertbarNegativeButton.innerHTML = negative
          $alertbar.style.visibility = "visible"
          onclicked($alertbarPositiveButton, () => {
            closeAlertBar()
            on_confirm()
          })
          onclicked($alertbarNegativeButton, () => {
            closeAlertBar()
            on_reject()
          })
          onclicked($alertbarCloseButton, () => {
            closeAlertBar()
          })
      }
    

    /**
     * E-Commerce specific logic
     */
    let $currentUserUsernameInput = select("#current-user-username")
    let $currentUserIDInput = select("#current-user-id")
    let $activeCartIDInput = select("#active-cart-id")
    let $activeCartNameInput = select("#active-cart-name")

    /*
    let $filterProductsForm = select("#filter-products-form")
    if ($filterProductsForm) {
      onsubmit($filterProductsForm, (e) => {
        e.preventDefault()
        if ($filterProductsForm.querySelector("#category-name").selectedOptions.length) {
          alert("hi")
        }
        $filterProductsForm.submit()
      })
    }
    */

    let $productElements = select(".product", true);
    let $activeCartName = select(".active-cart-name", true)
    let $activeCartTotal = select(".active-cart-total", true)

    const updateActiveCart = async () => {
        let res = await fetch(`/api/carts_detail_api_view/mini_data/?id=${$activeCartIDInput.value}`)
        let cart = await res.json()
        $activeCartTotal.forEach(el => {el.innerText = cart.total})
        showSnackbar(`${cart.name} successfully updated to ${cart.items_count} items at $${cart.total}`)
    }

    const updateWatchList = async () => {
      alert("Updated Watch List")
    }


    $productElements.forEach(productElement => {
      const $addWatchForm = productElement.querySelector(".add-watch-form")
      if ($addWatchForm) {
        $addWatchForm.addEventListener("submit", async (e) => {
          e.preventDefault();
          const formData = new FormData($addWatchForm)
          let res = await postFormData($addWatchForm.getAttribute("action"), formData)
          try {
            if (res.ok) {
              showSnackbar(`<p class="text-success">Successfully added ${productElement.getAttribute("product-name")} to your watchlist!</p>`)
            } else {
              showSnackbar(`<p class="text-warning">Could not add ${productElement.getAttribute("product-name")} to your watchlist. Most probably its already on your watchlist!</p>`) 
            }
          } catch (error) {
            console.log(error)
            showSnackbar(`<p class="text-danger">Failed to add ${productElement.getAttribute("product-name")} to your watchlist!</p>`)
          }
  
        })
      }

      const $addCartItemForm = productElement.querySelector(".add-cart-item-form")
      if ($addCartItemForm) {
        const $addCartItemFormQuantityInput = $addCartItemForm.querySelector(".quantity-input")
        const updateAddCartItemForm = (increment=true, number=0) => {
            let currentQuantity = parseFloat($addCartItemFormQuantityInput.value)
            let productQuantity = parseFloat(productElement.getAttribute("product-quantity"))
            if (number) {
                currentQuantity = number
            } else if (increment) {
                currentQuantity++
            } else {
                currentQuantity--
            }
            if (currentQuantity > productQuantity) {
              currentQuantity = productQuantity
            } else if (currentQuantity < 0) {
              currentQuantity = 0
            }
            $addCartItemFormQuantityInput.value = currentQuantity
            const $addCartItemFormProductQuantity = $addCartItemForm.querySelector(".product-quantity")
            const $addCartItemFormProductTotal = $addCartItemForm.querySelector(".total")
            if ($addCartItemFormProductQuantity && $addCartItemFormProductTotal) {
              $addCartItemForm.querySelector(".product-quantity").innerText = currentQuantity
              $addCartItemForm.querySelector(".total").innerText = Number(currentQuantity * productElement.getAttribute("product-selling-price")).toFixed(2)
            }
        }
        const $addCartItemFormIncrementButton = $addCartItemForm.querySelector(".increment")
        const $addCartItemFormDecrementButton = $addCartItemForm.querySelector(".decrement")
        if ($addCartItemFormIncrementButton && $addCartItemFormDecrementButton) {
          $addCartItemFormIncrementButton.addEventListener("click", () => updateAddCartItemForm(true))
          $addCartItemFormDecrementButton.addEventListener("click", () => updateAddCartItemForm(false))
        }
        $addCartItemFormQuantityInput.addEventListener("input", (e) => updateAddCartItemForm(number=e.targe.value))
        $addCartItemForm.addEventListener("submit", async (e) => {
            e.preventDefault()
            let formData = new FormData($addCartItemForm)
            let res = await postFormData($addCartItemForm.getAttribute("action"), formData)
            try {
                if (res.ok) {
                    let cartItem = await res.json()
                    showSnackbar(`<p class="text-success">Successfully added ${cartItem.product.name} <span class="badge bg-black">x${cartItem.quantity}</span>!</p>`)
                    updateActiveCart()
                } else {
                  showSnackbar(`
                  <p class="text-warning">
                    Failed to add ${productElement.getAttribute("product-name")} <span class="badge bg-black">x${parseFloat($addCartItemForm.querySelector(".quantity-input").value)}</span>!
                  </p>`)
                }
            } catch (error) {
              console.log(error)
                showSnackbar(`<p class="text-danger">A server error occured!</p>`)
            }
        })
      }

      const $deleteCartItemButton = productElement.querySelector(".deleteCartItemForm")
      if ($deleteCartItemButton) {
        onclicked($deleteCartItemButton, () => showAlertbar(`Do you truly wish to remove ${getAttr(productElement, "product-name")} from your cart?`, async () => {
          const res = await fetch(`/api/cart_items_detail_api_view/data/?id=${getAttr(productElement, "cart-item-id")}`, {method: "DELETE"})
          try {
            if (res.ok) {
                showSnackbar(`<p class="text-success">Successfully removed ${getAttr(productElement, "product-name")} from your cart!</p>`)
                productElement.style.display = "none"
                updateActiveCart()
            } else {
              showSnackbar(`
              <p class="text-warning">
                Failed to remove ${getAttr(productElement, "product-name")} from your cart!
              </p>`)
            }
          } catch (error) {
            console.log(error)
            showSnackbar(`<p class="text-danger">A server error occured!</p>`)
          }
        })
      )
      }

      const $deleteWatchItemButton = productElement.querySelector(".deleteWatchItemForm")
      if ($deleteWatchItemButton) {
        onclicked($deleteWatchItemButton, () => showAlertbar(`Do you truly wish to remove ${getAttr(productElement, "product-name")} from your watchlist?`, async () => {
            const res = await fetch(`/api/watches_detail_api_view/data/?id=${getAttr(productElement, "watch-id")}`, {method: "DELETE"})
            try {
              if (res.ok) {
                  showSnackbar(`<p class="text-success">Successfully removed ${getAttr(productElement, "product-name")} from your watchlist!</p>`)
                  productElement.style.display = "none"
                  updateWatchList()
              } else {
                showSnackbar(`
                <p class="text-warning">
                  Failed to remove ${getAttr(productElement, "product-name")} from your watch list!
                </p>`)
              }
            } catch (error) {
              console.log(error)
              showSnackbar(`<p class="text-danger">A server error occured!</p>`)
            }
          })
        )
      }
    })
})()