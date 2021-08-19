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
    const getInputValue = (inputID) => select(inputID).value;
    const focus = (inputID) => select(inputID).focus();
    const scrollTo = (inputID) => window.scrollTo(0, select(inputID).offsetTop)
  
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
    let $alert = $snackbar.querySelector(".alert")
    let $snackbarMessage = $alert.querySelector(".snackbar-message")
    $snackbar.querySelector("button").addEventListener("click", () => {
        $snackbar.querySelector(".snackbar-message").innerHTML = ''
        $snackbar.style.visibility = "hidden"
    })
    /**
     * Show snackbar func
     */
    const showSnackbar = (message, _class="info") => {
        $alert.classList.replace($alert.classList[2], `alert-${_class}`)
        $snackbarMessage.innerHTML = `${$snackbarMessage.innerHTML}` + message
        $snackbar.style.visibility = "visible"
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
    $productElements.forEach(productElement => {
      let $addWatchForm = productElement.querySelector(".add-watch-form")
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
        let $productElementForm = productElement.querySelector(".add-cart-item-form")
        if (!$productElementForm) return
        const updateProductElementForm = (increment=true, number=0) => {
            let currentQuantity = parseFloat($productElementForm.querySelector(".quantity-input").value)
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
            $productElementForm.querySelector(".quantity-input").value = currentQuantity
            $productElementForm.querySelector(".product-quantity").innerText = currentQuantity
            $productElementForm.querySelector(".total").innerText = Number(currentQuantity * productElement.getAttribute("product-selling-price")).toFixed(2)
        }
        $productElementForm.querySelector(".increment").addEventListener("click", () => updateProductElementForm(true))
        $productElementForm.querySelector(".decrement").addEventListener("click", () => updateProductElementForm(false))
        $productElementForm.querySelector(".quantity-input").addEventListener("input", (e) => updateProductElementForm(number=e.targe.value))
        $productElementForm.addEventListener("submit", async (e) => {
            e.preventDefault()
            let formData = new FormData($productElementForm)
            let res = await postFormData($productElementForm.getAttribute("action"), formData)
            try {
                if (res.ok) {
                    let cartItem = await res.json()
                    console.log(cartItem)
                    showSnackbar(`<p class="text-success">Successfully added ${cartItem.product.name} <span class="badge bg-black">x${cartItem.quantity}</span>!</p>`)
                    updateActiveCart()
                } else {
                  showSnackbar(`
                  <p class="text-warning">
                    Failed to add ${productElement.getAttribute("product-name")} <span class="badge bg-black">x${parseFloat($productElementForm.querySelector(".quantity-input").value)}</span>!
                  </p>`)
                }
            } catch (error) {
              console.log(error)
                showSnackbar(`<p class="text-danger">A server error occured!</p>`)
            }
        })
    })
})()