document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });



      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");

        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // get data from inputs and show them in summary:
      //get data inputs:
      const categories = (document.querySelectorAll("input[name='categories']:checked"))
      let categoriesList = []
      for (let i=0; i<categories.length; i++){
        var category = categories[i].nextElementSibling.nextElementSibling.innerHTML
        categoriesList.push(category)
        categoriesList.join(' ')
      }
      const quantity = document.getElementById('id_quantity')
      const institution = document.querySelector("input[name='institution']:checked").nextElementSibling.nextElementSibling.firstElementChild.innerText
      const street = document.getElementById('id_address')
      const city = document.getElementById('id_city')
      const postcode = document.getElementById('id_postcode')
      const phone = document.getElementById('id_phone_0')
      const date = document.getElementById('id_date')
      const time = document.getElementById('id_time')
      const comments = document.getElementById('id_comments')

      function form_summary() {
      //where to place it:
      let cat_li = document.getElementById('sum_cat')
      let inst_li = document.getElementById('sum_inst')
      let street_li = document.getElementById('sum_street')
      let city_li = document.getElementById('sum_city')
      let postecode_li = document.getElementById('sum_postcode')
      let phone_li = document.getElementById('sum_phone')
      let date_li = document.getElementById('sum_date')
      let time_li = document.getElementById('sum_time')
      let comment_li = document.getElementById('sum_comment')
      //do the summary:
      cat_li.lastElementChild.innerText = quantity.value +" "+ "worki" + " " + "przedmiotów z kategorii:" +" "+ categoriesList
      inst_li.lastElementChild.innerText = 'Dla:' + ' ' + institution
      street_li.innerText = street.value
      city_li.innerText = city.value
      postecode_li.innerText = postcode.value
      phone_li.innerText = phone.value
      date_li.innerText = date.value
      time_li.innerText = time.value
      comment_li.innerText = comments.value
    }
    //add eventlistener on summary button:
    const btn_sum = document.getElementById('btn_sum')
    btn_sum.addEventListener("click", (event) => form_summary())

    }


    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */

    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
      $.ajax({
        url : "/add_donation/",
        type : "POST",
        data : $('#form-send').serialize(),
        success : function(json) {
            // let messageElement = $('<div><h3>'+json.msg+'</h3></div>')
            // $('.form--steps-container').prepend(messageElement); // add success message
            console.log(json); // log the returned json to the console
            console.log("success");
            window.location.href = "/confirmation/"

        },})
  }};
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});


