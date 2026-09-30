(function () {
    const heading = document.getElementById('animated-name');
    if (!heading) return;

    const name = heading.textContent.trim();
    heading.textContent = '';
    let letterIndex = 0;

    name.split(/(\s+)/).forEach((part) => {
        if (/^\s+$/.test(part)) {
            heading.append(document.createTextNode(part));
            return;
        }

        const word = document.createElement('span');
        word.className = 'name-word';
        word.setAttribute('aria-hidden', 'true');

        Array.from(part).forEach((character) => {
            const letter = document.createElement('span');
            letter.className = 'name-letter';
            letter.textContent = character;
            letter.style.setProperty('--letter-index', letterIndex);
            letter.style.setProperty('--letter-start', letterIndex % 2 === 0 ? '-0.35em' : '0.35em');
            word.appendChild(letter);
            letterIndex += 1;
        });

        heading.appendChild(word);
    });
})();
