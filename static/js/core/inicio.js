document.addEventListener('DOMContentLoaded', function () {
    const elements = document.querySelectorAll('.reveal');
    if (!('IntersectionObserver' in window) || elements.length === 0) {
        elements.forEach(function (el) { el.classList.add('visible'); });
        return;
    }

    const observer = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });

    elements.forEach(function (el) { observer.observe(el); });
});
