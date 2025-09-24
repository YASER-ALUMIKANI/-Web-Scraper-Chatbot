(function () {
  "use strict";

  const navToggle = document.querySelector(".navbar__toggle");
  const navMenu = document.querySelector(".navbar__links");

  if (navToggle && navMenu) {
    const closeMenu = () => {
      navToggle.setAttribute("aria-expanded", "false");
      navMenu.setAttribute("aria-expanded", "false");
      navMenu.classList.remove("is-open");
    };

    navToggle.addEventListener("click", () => {
      const expanded = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!expanded));
      navMenu.setAttribute("aria-expanded", String(!expanded));
      navMenu.classList.toggle("is-open", !expanded);
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 768) {
        navMenu.removeAttribute("aria-expanded");
        navMenu.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      } else if (!navMenu.hasAttribute("aria-expanded")) {
        navMenu.setAttribute("aria-expanded", "false");
      }
    });

    navMenu.addEventListener("click", (event) => {
      if (event.target instanceof HTMLAnchorElement && window.innerWidth <= 768) {
        closeMenu();
      }
    });
  }

  // Smooth scrolling for internal anchors respecting reduced motion
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!prefersReducedMotion) {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", (event) => {
        const targetId = anchor.getAttribute("href");
        if (!targetId || targetId === "#") return;
        const targetEl = document.querySelector(targetId);
        if (!targetEl) return;
        event.preventDefault();
        targetEl.scrollIntoView({ behavior: "smooth" });
        try {
          targetEl.focus({ preventScroll: true });
        } catch (error) {
          targetEl.focus();
        }
      });
    });
  }

  // FAQ accordion
  document.querySelectorAll("[data-accordion]").forEach((item) => {
    const button = item.querySelector("button");
    const content = item.querySelector(".faq__content");
    if (!button || !content) return;

    button.addEventListener("click", () => {
      const expanded = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!expanded));
      content.hidden = expanded;
    });
  });

  // Lightbox functionality
  const lightbox = document.getElementById("lightbox");
  const lightboxImage = lightbox?.querySelector(".lightbox__image");
  const lightboxCaption = lightbox?.querySelector(".lightbox__caption");
  const lightboxClose = lightbox?.querySelector(".lightbox__close");
  let lastFocusedElement = null;

  const trapFocus = (event) => {
    if (!lightbox || lightbox.getAttribute("aria-hidden") === "true") return;
    const focusable = lightbox.querySelectorAll("button, [href], input, select, textarea, [tabindex]:not([tabindex='-1'])");
    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (event.key === "Tab") {
      if (event.shiftKey) {
        if (document.activeElement === first) {
          event.preventDefault();
          last.focus();
        }
      } else if (document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  };

  const closeLightbox = () => {
    if (!lightbox) return;
    lightbox.setAttribute("aria-hidden", "true");
    lightboxImage?.setAttribute("src", "");
    lightboxImage?.setAttribute("alt", "");
    lightboxCaption && (lightboxCaption.textContent = "");
    document.removeEventListener("keydown", trapFocus);
    document.removeEventListener("keydown", onKeydown);
    if (lastFocusedElement instanceof HTMLElement) {
      lastFocusedElement.focus();
    }
  };

  const onKeydown = (event) => {
    if (event.key === "Escape") {
      closeLightbox();
    }
  };

  document.querySelectorAll('[data-lightbox="open"]').forEach((trigger) => {
    trigger.addEventListener("click", () => {
      if (!(lightbox && lightboxImage && lightboxCaption && lightboxClose)) return;
      const src = trigger.getAttribute("data-image-src");
      const alt = trigger.getAttribute("data-image-alt") || "Gallery image";
      lightboxImage.setAttribute("src", src || "");
      lightboxImage.setAttribute("alt", alt);
      lightboxCaption.textContent = alt;
      lightbox.setAttribute("aria-hidden", "false");
      lastFocusedElement = document.activeElement;
      lightboxClose.focus();
      document.addEventListener("keydown", trapFocus);
      document.addEventListener("keydown", onKeydown);
    });
  });

  document.querySelectorAll('[data-lightbox="close"]').forEach((element) => {
    element.addEventListener("click", closeLightbox);
  });

  if (lightbox) {
    lightbox.addEventListener("click", (event) => {
      if (event.target === lightbox) {
        closeLightbox();
      }
    });
  }

  // Banner rotation highlight
  const banners = Array.from(document.querySelectorAll(".banner"));
  if (banners.length > 1) {
    let activeIndex = 0;
    banners[activeIndex].classList.add("is-active");
    setInterval(() => {
      banners[activeIndex].classList.remove("is-active");
      activeIndex = (activeIndex + 1) % banners.length;
      banners[activeIndex].classList.add("is-active");
    }, 8000);
  }
})();
