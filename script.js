const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');
tabButtons.forEach((button) => button.addEventListener('click', () => {
  tabButtons.forEach((item) => item.classList.remove('active'));
  tabContents.forEach((item) => item.classList.remove('active'));
  button.classList.add('active');
  document.getElementById(button.dataset.tab).classList.add('active');
}));

const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
  if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
}), { threshold: .12 });
document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));

const prismStyles = document.createElement('style');
prismStyles.textContent = `
  .glass-card,.analysis-window,.insight-panel,.cta-card{position:relative;isolation:isolate}
  .glass-card::before,.analysis-window::before,.insight-panel::before,.cta-card::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;border-radius:inherit;background:linear-gradient(115deg,rgba(122,235,255,.12),transparent 28%,rgba(187,143,255,.16) 52%,transparent 72%,rgba(255,161,216,.11));background-size:220% 220%;animation:prism-shift 8s ease-in-out infinite alternate}
  .glass-card::after,.analysis-window::after{content:"";position:absolute;inset:1px;pointer-events:none;border-radius:inherit;background:linear-gradient(135deg,rgba(255,255,255,.18),transparent 23%,transparent 72%,rgba(177,245,255,.12));mix-blend-mode:screen}
  .page-glow{opacity:.31}.glow-one{background:linear-gradient(135deg,#6d53ff,#53e3ff)}.glow-two{background:linear-gradient(135deg,#ff82c8,#38dff3)}
  .hero-visual{filter:drop-shadow(0 0 28px rgba(116,203,255,.14))}.score-ring{box-shadow:0 0 22px #78dbff44,0 0 38px #b987ff28}
  @keyframes prism-shift{0%{background-position:0% 50%}100%{background-position:100% 50%}}
  @media(prefers-reduced-motion:reduce){.glass-card::before,.analysis-window::before,.insight-panel::before,.cta-card::before{animation:none}}
`;
document.head.appendChild(prismStyles);
