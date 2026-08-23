
(() => {
  document.querySelectorAll('img[data-fallback]').forEach(img => {
    img.addEventListener('error', () => {
      img.style.display='none';
      const fb=img.parentElement.querySelector('.paper-fallback');
      if(fb) fb.style.display='grid';
    });
    img.addEventListener('load', () => {
      const fb=img.parentElement.querySelector('.paper-fallback');
      if(fb) fb.style.display='none';
    });
  });
})();
