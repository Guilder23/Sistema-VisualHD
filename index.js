// =========================================================
// VISUAL HD PRODUCCIONES - JAVASCRIPT
// =========================================================

// Mobile Menu Toggle
const mobileBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');

if (mobileBtn && mobileMenu) {
    mobileBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('open');
    });

    document.querySelectorAll('.mobile-link').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.remove('open');
        });
    });
}

// Header Scroll Effect
window.addEventListener('scroll', () => {
    const header = document.getElementById('mainHeader');
    if (header) {
        if (window.scrollY > 30) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }

    // Back to Top Button visibility
    const backToTopBtn = document.getElementById('backToTopBtn');
    if (backToTopBtn) {
        if (window.scrollY > 400) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    }
});

// Back to Top click
const backToTopBtn = document.getElementById('backToTopBtn');
if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// Lightbox Logic
const lightboxModal = document.getElementById('lightboxModal');
const lightboxImg = document.getElementById('lightboxImg');
const lightboxCaption = document.getElementById('lightboxCaption');

const galleryImages = [
    { src: 'static/img/visualhd/cover_quince_anos.jpeg', caption: 'Sesión Fotográfica 15 Años - Portada Visual HD' },
    { src: 'static/img/visualhd/cover_promo_kinder.jpeg', caption: 'Paquete de Promoción Kinder 2026 - Portada' },
    { src: 'static/img/visualhd/flyer_promo_kinder.png', caption: 'Flyer Oficial Paquete de Promoción Kinder 2026' },
    { src: 'static/img/visualhd/marco_cuadro_1.jpeg', caption: 'Enmarcación Clásica y Moderna en Trupan y Acrílico' },
    { src: 'static/img/visualhd/marco_cuadro_2.jpeg', caption: 'Enmarcaciones de Lujo para Graduaciones y 15 Años' },
    { src: 'static/img/visualhd/marco_cuadro_3.jpeg', caption: 'Cuadros Personalizados de Alta Calidad' },
    { src: 'static/img/visualhd/flyer_quince_anos.jpeg', caption: 'Flyer Oficial de Sesiones de 15 Años' },
    { src: 'static/img/visualhd/galeria_15anos_1.jpeg', caption: 'Galería 15 Años - Retrato 01' },
    { src: 'static/img/visualhd/galeria_15anos_2.jpeg', caption: 'Galería 15 Años - Retrato 02' },
    { src: 'static/img/visualhd/galeria_15anos_3.jpeg', caption: 'Galería 15 Años - Retrato 03' },
    { src: 'static/img/visualhd/galeria_15anos_4.jpeg', caption: 'Galería 15 Años - Retrato 04' },
    { src: 'static/img/visualhd/galeria_15anos_5.jpeg', caption: 'Galería 15 Años - Retrato 05' },
    { src: 'static/img/visualhd/galeria_15anos_6.jpeg', caption: 'Galería 15 Años - Retrato 06' },
    { src: 'static/img/visualhd/galeria_15anos_7.jpeg', caption: 'Galería 15 Años - Retrato 07' },
    { src: 'static/img/visualhd/galeria_15anos_8.jpeg', caption: 'Galería 15 Años - Retrato 08' },
    { src: 'static/img/visualhd/galeria_15anos_9.jpeg', caption: 'Galería 15 Años - Retrato 09' },
    { src: 'static/img/visualhd/galeria_15anos_10.jpeg', caption: 'Galería 15 Años - Retrato 10' },
    { src: 'static/img/visualhd/galeria_15anos_11.jpeg', caption: 'Galería 15 Años - Retrato 11' },
    { src: 'static/img/visualhd/galeria_15anos_12.jpeg', caption: 'Galería 15 Años - Retrato 12' },
    { src: 'static/img/visualhd/hero_house_facade.jpeg', caption: 'Fachada del Estudio Visual HD Producciones en San Julián' }
];

let currentLightboxIndex = 0;

function openLightbox(src, caption) {
    const index = galleryImages.findIndex(img => img.src === src || src.endsWith(img.src.replace('static/', '')));
    currentLightboxIndex = index !== -1 ? index : 0;
    
    if (lightboxImg && lightboxModal) {
        lightboxImg.src = src;
        if (lightboxCaption) {
            lightboxCaption.textContent = caption || (galleryImages[currentLightboxIndex] ? galleryImages[currentLightboxIndex].caption : '');
        }
        lightboxModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeLightbox(e) {
    if (lightboxModal) {
        lightboxModal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function nextLightboxImage() {
    currentLightboxIndex = (currentLightboxIndex + 1) % galleryImages.length;
    updateLightbox();
}

function prevLightboxImage() {
    currentLightboxIndex = (currentLightboxIndex - 1 + galleryImages.length) % galleryImages.length;
    updateLightbox();
}

function updateLightbox() {
    const item = galleryImages[currentLightboxIndex];
    if (lightboxImg && item) {
        lightboxImg.src = item.src;
        if (lightboxCaption) lightboxCaption.textContent = item.caption;
    }
}

// Keyboard controls
document.addEventListener('keydown', (e) => {
    if (!lightboxModal || !lightboxModal.classList.contains('active')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') nextLightboxImage();
    if (e.key === 'ArrowLeft') prevLightboxImage();
});
