/* Au Fil de la Reliure – petits scripts (menu mobile, filtres, visionneuse) */
(function () {
  'use strict';

  /* ---- Menu mobile ---- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('menu-principal');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
        toggle.focus();
      }
    });
  }

  /* ---- Année du pied de page ---- */
  var year = document.querySelectorAll('[data-year]');
  for (var y = 0; y < year.length; y++) year[y].textContent = new Date().getFullYear();

  /* ---- Filtres de la galerie ---- */
  var filters = document.querySelectorAll('.filter');
  var items = document.querySelectorAll('.gallery-item');
  for (var i = 0; i < filters.length; i++) {
    filters[i].addEventListener('click', function () {
      var value = this.getAttribute('data-filter');
      for (var j = 0; j < filters.length; j++) filters[j].setAttribute('aria-pressed', String(filters[j] === this));
      for (var k = 0; k < items.length; k++) {
        items[k].hidden = !(value === 'all' || items[k].getAttribute('data-category') === value);
      }
    });
  }

  /* ---- Visionneuse photo ---- */
  var dialog = document.querySelector('.lightbox');
  if (dialog && typeof dialog.showModal === 'function') {
    var img = dialog.querySelector('img');
    var caption = dialog.querySelector('figcaption');
    var links = document.querySelectorAll('[data-lightbox]');
    for (var l = 0; l < links.length; l++) {
      links[l].addEventListener('click', function (e) {
        e.preventDefault();
        img.src = this.getAttribute('href');
        img.alt = this.querySelector('img') ? this.querySelector('img').alt : '';
        caption.textContent = this.getAttribute('data-caption') || '';
        dialog.showModal();
      });
    }
    dialog.querySelector('.lightbox-close').addEventListener('click', function () { dialog.close(); });
    // Fermer en cliquant à côté de la photo
    dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
  }
})();
