/**
 * LocalMeet Client-Side Validation
 * @version 2025.12
 */

const FormValidator = {
  validateEventForm: function (form) {
    const errors = [];

    const title = form.querySelector("#title");
    if (title) {
      const titleValue = title.value.trim();
      if (titleValue.length < 3 || titleValue.length > 200) {
        errors.push("Title must be between 3 and 200 characters");
        this.markFieldInvalid(title);
      } else {
        this.markFieldValid(title);
      }
    }

    const location = form.querySelector("#location");
    if (location) {
      const locationValue = location.value.trim();
      if (locationValue.length < 3 || locationValue.length > 300) {
        errors.push("Location must be between 3 and 300 characters");
        this.markFieldInvalid(location);
      } else {
        this.markFieldValid(location);
      }
    }

    const price = form.querySelector("#price");
    if (price) {
      const priceValue = parseFloat(price.value);
      if (isNaN(priceValue) || priceValue < 0 || priceValue > 10000) {
        errors.push("Price must be between $0 and $10,000");
        this.markFieldInvalid(price);
      } else {
        this.markFieldValid(price);
      }
    }

    const maxAttendees = form.querySelector("#max_attendees");
    if (maxAttendees) {
      const maxValue = parseInt(maxAttendees.value);
      if (isNaN(maxValue) || maxValue < 1 || maxValue > 10000) {
        errors.push("Max attendees must be between 1 and 10,000");
        this.markFieldInvalid(maxAttendees);
      } else {
        this.markFieldValid(maxAttendees);
      }
    }

    const description = form.querySelector("#description");
    if (description) {
      const descValue = description.value.trim();
      if (descValue.length < 10 || descValue.length > 5000) {
        errors.push("Description must be between 10 and 5000 characters");
        this.markFieldInvalid(description);
      } else {
        this.markFieldValid(description);
      }
    }

    const date = form.querySelector("#date");
    const time = form.querySelector("#time");
    if (date && time && date.value && time.value) {
      const eventDateTime = new Date(date.value + "T" + time.value);
      const now = new Date();
      if (eventDateTime <= now) {
        errors.push("Event date and time must be in the future");
        this.markFieldInvalid(date);
        this.markFieldInvalid(time);
      } else {
        this.markFieldValid(date);
        this.markFieldValid(time);
      }
    }

    const regDeadline = form.querySelector("#registration_deadline");
    if (
      regDeadline &&
      date &&
      time &&
      regDeadline.value &&
      date.value &&
      time.value
    ) {
      const deadlineDate = new Date(regDeadline.value);
      const eventDateTime = new Date(date.value + "T" + time.value);
      if (deadlineDate >= eventDateTime) {
        errors.push("Registration deadline must be before the event starts");
        this.markFieldInvalid(regDeadline);
      } else {
        this.markFieldValid(regDeadline);
      }
    }

    return errors;
  },

  validateUserProfileForm: function (form) {
    const errors = [];

    const firstName = form.querySelector("#first_name");
    if (firstName) {
      const nameValue = firstName.value.trim();
      const namePattern = /^[a-zA-Z\s\-']+$/;
      if (nameValue.length < 1 || nameValue.length > 100) {
        errors.push("First name must be between 1 and 100 characters");
        this.markFieldInvalid(firstName);
      } else if (!namePattern.test(nameValue)) {
        errors.push(
          "First name can only contain letters, spaces, hyphens, and apostrophes"
        );
        this.markFieldInvalid(firstName);
      } else {
        this.markFieldValid(firstName);
      }
    }

    const lastName = form.querySelector("#last_name");
    if (lastName) {
      const nameValue = lastName.value.trim();
      const namePattern = /^[a-zA-Z\s\-']+$/;
      if (nameValue.length < 1 || nameValue.length > 100) {
        errors.push("Last name must be between 1 and 100 characters");
        this.markFieldInvalid(lastName);
      } else if (!namePattern.test(nameValue)) {
        errors.push(
          "Last name can only contain letters, spaces, hyphens, and apostrophes"
        );
        this.markFieldInvalid(lastName);
      } else {
        this.markFieldValid(lastName);
      }
    }

    const phone = form.querySelector("#phone_number");
    if (phone && phone.value.trim()) {
      const phoneValue = phone.value.trim();
      const phonePattern = /^[\d\s\-\+\(\)]+$/;
      if (phoneValue.length > 20) {
        errors.push("Phone number cannot exceed 20 characters");
        this.markFieldInvalid(phone);
      } else if (!phonePattern.test(phoneValue)) {
        errors.push("Invalid phone number format");
        this.markFieldInvalid(phone);
      } else {
        this.markFieldValid(phone);
      }
    }

    const bio = form.querySelector("#bio");
    if (bio && bio.value.trim()) {
      if (bio.value.length > 1000) {
        errors.push("Bio cannot exceed 1000 characters");
        this.markFieldInvalid(bio);
      } else {
        this.markFieldValid(bio);
      }
    }

    return errors;
  },

  markFieldInvalid: function (field) {
    field.classList.add("is-danger");
    field.classList.remove("is-success");
  },

  markFieldValid: function (field) {
    field.classList.add("is-success");
    field.classList.remove("is-danger");
  },

  displayErrors: function (errors) {
    const existingNotification = document.querySelector(
      ".validation-notification"
    );
    if (existingNotification) {
      existingNotification.remove();
    }

    if (errors.length > 0) {
      const notification = document.createElement("div");
      notification.className = "notification is-danger validation-notification";
      notification.innerHTML = `
        <button class="delete"></button>
        <strong>Please correct the following errors:</strong>
        <ul>
          ${errors.map((error) => `<li>${error}</li>`).join("")}
        </ul>
      `;

      const form = document.querySelector("form");
      if (form) {
        form.insertAdjacentElement("beforebegin", notification);
        notification.querySelector(".delete").addEventListener("click", () => {
          notification.remove();
        });
        notification.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    }
  },
};

document.addEventListener("DOMContentLoaded", () => {
  const eventForm = document.querySelector('form[action*="event"]');
  if (eventForm) {
    const inputs = eventForm.querySelectorAll("input, textarea");
    inputs.forEach((input) => {
      input.addEventListener("blur", () => {
        FormValidator.validateEventForm(eventForm);
      });
    });

    eventForm.addEventListener("submit", (e) => {
      const errors = FormValidator.validateEventForm(eventForm);
      if (errors.length > 0) {
        e.preventDefault();
        FormValidator.displayErrors(errors);
      }
    });
  }

  const profileForm = document.querySelector('form[action*="profile"]');
  if (profileForm) {
    const inputs = profileForm.querySelectorAll("input, textarea");
    inputs.forEach((input) => {
      input.addEventListener("blur", () => {
        FormValidator.validateUserProfileForm(profileForm);
      });
    });

    profileForm.addEventListener("submit", (e) => {
      const errors = FormValidator.validateUserProfileForm(profileForm);
      if (errors.length > 0) {
        e.preventDefault();
        FormValidator.displayErrors(errors);
      }
    });
  }

  const textareas = document.querySelectorAll("textarea[maxlength]");
  textareas.forEach((textarea) => {
    const maxLength = textarea.getAttribute("maxlength");
    const counter = document.createElement("p");
    counter.className = "help has-text-right";
    counter.textContent = `0 / ${maxLength}`;
    textarea.parentElement.appendChild(counter);

    textarea.addEventListener("input", () => {
      const currentLength = textarea.value.length;
      counter.textContent = `${currentLength} / ${maxLength}`;
      if (currentLength > maxLength * 0.9) {
        counter.classList.add("has-text-warning");
      } else {
        counter.classList.remove("has-text-warning");
      }
    });

    textarea.dispatchEvent(new Event("input"));
  });

  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach((input) => {
    input.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (file) {
        const allowedTypes = [
          "image/jpeg",
          "image/jpg",
          "image/png",
          "image/gif",
          "image/webp",
        ];
        if (!allowedTypes.includes(file.type)) {
          alert(
            "Invalid file type. Please upload an image (JPG, PNG, GIF, or WEBP)."
          );
          input.value = "";
        } else if (file.size > 10 * 1024 * 1024) {
          // 10MB limit
          alert("File size must be less than 10MB.");
          input.value = "";
        }
      }
    });
  });
});
