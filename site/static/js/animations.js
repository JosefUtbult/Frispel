// 
// home page - animation of image
//

(function(){
  const el = document.querySelector('.home-img');
  if (!el) return;

  // kör bara parallax på desktop / stora skärmar
  const desktopMQ = window.matchMedia('(min-width: 1442px)');
  let rafId = null;
  const speed = 0.5; // justera (0.1-0.6)

  function applyParallax() {
    // säkerställ att elementet finns och vi är på desktop
    if (!desktopMQ.matches) return;
    const offset = window.scrollY * speed;
    // sätter bakgrundens Y-position i pixlar (kan vara negativ)
    el.style.backgroundPosition = `center ${-offset}px`;
  }

  function onScroll() {
    if (rafId === null) {
      rafId = requestAnimationFrame(function() {
        applyParallax();
        rafId = null;
      });
    }
  }

  // event listeners - passiva för bättre scrollprestanda
  window.addEventListener('scroll', onScroll, { passive: true });

  // reagera på media query-förändring (resize): start/stop + återställ värden
  function mqChange(e) {
    if (e.matches) {
      // blev desktop -> kör en gång för att positionera korrekt
      applyParallax();
    } else {
      // blev mobil/tablet -> återställ så bilden är statisk och visas från toppen
      el.style.backgroundPosition = 'top center';
    }
  }

  if (desktopMQ.addEventListener) {
    desktopMQ.addEventListener('change', mqChange);
  } else if (desktopMQ.addListener) { // äldre browser fallback
    desktopMQ.addListener(mqChange);
  }

  // initialt läge
  if (!desktopMQ.matches) {
    el.style.backgroundPosition = 'top center';
  } else {
    applyParallax();
  }

})();