/* === COPY BUTTONS on every code block === */
document.querySelectorAll('pre').forEach(pre => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'copy-btn';
    b.setAttribute('aria-label', 'Copy to clipboard');
    b.innerHTML = '<svg class="i-copy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg><svg class="i-ok" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>';
    b.addEventListener('click', async () => {
        const text = [...pre.childNodes].filter(n => n !== b).map(n => n.textContent).join('');
        try { await navigator.clipboard.writeText(text); b.classList.add('copied'); setTimeout(() => b.classList.remove('copied'), 1500); } catch (_) {}
    });
    pre.appendChild(b);
});

