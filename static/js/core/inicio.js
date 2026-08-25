// =========================================================
// VISUAL HD PRODUCCIONES - JAVASCRIPT
// =========================================================

// Mobile Menu Toggle
const mobileBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');
const mobileMenuClose = document.getElementById('mobileMenuClose');
const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');

if (mobileBtn && mobileMenu) {
    const closeMobileMenu = () => {
        mobileMenu.classList.remove('open');
        mobileMenuOverlay?.classList.remove('open');
        document.body.classList.remove('mobile-menu-locked');
    };

    mobileBtn.addEventListener('click', () => {
        mobileMenu.classList.add('open');
        mobileMenuOverlay?.classList.add('open');
        document.body.classList.add('mobile-menu-locked');
    });

    mobileMenuClose?.addEventListener('click', closeMobileMenu);
    mobileMenuOverlay?.addEventListener('click', closeMobileMenu);

    document.querySelectorAll('.mobile-link').forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });

    document.addEventListener('keydown', event => {
        if (event.key === 'Escape') closeMobileMenu();
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) closeMobileMenu();
    });
}

// Header Scroll Effect & Back to Top visibility
const header = document.getElementById('mainHeader');
const backToTopBtn = document.getElementById('backToTopBtn');

window.addEventListener('scroll', () => {
    if (header) {
        if (window.scrollY > 30) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }

    if (backToTopBtn) {
        if (window.scrollY > 400) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    }
});

// Back to Top click
if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// =========================================================
// LIGHTBOX SYSTEM
// =========================================================
const lightboxModal = document.getElementById('lightboxModal');
const lightboxImg = document.getElementById('lightboxImg');
const lightboxCaption = document.getElementById('lightboxCaption');
const lightboxCloseBtn = document.getElementById('lightboxCloseBtn');
const lightboxPrevBtn = document.getElementById('lightboxPrevBtn');
const lightboxNextBtn = document.getElementById('lightboxNextBtn');

// Auto-populate gallery items from DOM
let galleryItems = [];
let currentLightboxIndex = 0;

function refreshGalleryItems() {
    const triggerElements = document.querySelectorAll('.gallery-item, .flyer-card, .hero-visual-card-main, .hero-floating-card, .studio-image-wrap, [data-lightbox]');
    galleryItems = [];
    triggerElements.forEach(el => {
        const img = el.querySelector('img');
        if (img) {
            const src = el.getAttribute('data-lightbox-src') || img.currentSrc || img.getAttribute('src') || '';
            const caption = el.getAttribute('data-caption') || img.getAttribute('alt') || '';
            galleryItems.push({ src, caption, el });
        }
    });
}

function openLightbox(src, caption) {
    if (!lightboxModal || !lightboxImg) return;
    
    refreshGalleryItems();
    const index = galleryItems.findIndex(item => item.src === src || (src && item.src.includes(src.split('/').pop())));
    currentLightboxIndex = index !== -1 ? index : 0;
    
    lightboxImg.src = src;
    if (lightboxCaption) {
        lightboxCaption.textContent = caption || (galleryItems[currentLightboxIndex] ? galleryItems[currentLightboxIndex].caption : '');
    }
    lightboxModal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    if (lightboxModal) {
        lightboxModal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function nextLightboxImage() {
    if (galleryItems.length === 0) return;
    currentLightboxIndex = (currentLightboxIndex + 1) % galleryItems.length;
    updateLightbox();
}

function prevLightboxImage() {
    if (galleryItems.length === 0) return;
    currentLightboxIndex = (currentLightboxIndex - 1 + galleryItems.length) % galleryItems.length;
    updateLightbox();
}

function updateLightbox() {
    const item = galleryItems[currentLightboxIndex];
    if (lightboxImg && item) {
        lightboxImg.src = item.src;
        if (lightboxCaption) lightboxCaption.textContent = item.caption;
    }
}

// Event Delegation for opening lightbox
document.addEventListener('click', (e) => {
    const trigger = e.target.closest('.gallery-item, .flyer-card, .hero-visual-card-main, .hero-floating-card, .studio-image-wrap, [data-lightbox]');
    if (trigger) {
        e.preventDefault();
        const img = trigger.querySelector('img');
        if (img) {
            const src = trigger.getAttribute('data-lightbox-src') || img.currentSrc || img.getAttribute('src');
            const caption = trigger.getAttribute('data-caption') || img.getAttribute('alt') || '';
            openLightbox(src, caption);
        }
    }
});

// Lightbox Controls Event Listeners
lightboxCloseBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    closeLightbox();
});

lightboxPrevBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    prevLightboxImage();
});

lightboxNextBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    nextLightboxImage();
});

lightboxModal?.addEventListener('click', (e) => {
    if (e.target === lightboxModal) {
        closeLightbox();
    }
});

// Keyboard Navigation
document.addEventListener('keydown', (e) => {
    if (!lightboxModal || !lightboxModal.classList.contains('active')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') nextLightboxImage();
    if (e.key === 'ArrowLeft') prevLightboxImage();
});

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', refreshGalleryItems);
