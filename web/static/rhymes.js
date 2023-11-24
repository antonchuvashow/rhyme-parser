function getPopularity(tags) {
    var popularityTag = tags.find(tag => tag.startsWith('f:'));
    if (popularityTag) {
        return parseFloat(popularityTag.split(':')[1]);
    }
    return 0;
}

function createProgressBar(value, maxValue) {
    var progressBar = document.createElement('progress');
    progressBar.max = maxValue;
    progressBar.value = value;
    return progressBar;
}
function createLogProgressBar(value, maxValue) {
    var progressBar = document.createElement('progress');
    progressBar.max = Math.log10(maxValue *10000 + 1);
    progressBar.value = Math.log10(value*10000 + 1);
    return progressBar;
}

var container = document.getElementById("cards-container");

jsonData.forEach(function (wordData, index) {
    var card = document.createElement('div');
    card.className = 'card';


    var scoreProgressBar = createProgressBar(wordData.score, 100);
    var popularityProgressBar = createLogProgressBar(getPopularity(wordData.tags), 100);

    card.innerHTML = `
            <h2>${wordData.word}</h2>
            <div>Rhymiiiness</div>
            <div class="score-bar" title="${wordData.score}%">${scoreProgressBar.outerHTML}
            </div>
            <div>Popularity</div>
            <div class="popularity-bar" title="${getPopularity(wordData.tags)} words per million">${popularityProgressBar.outerHTML}
            </div>
        `;
    card.style.animationDelay = index * 0.02 + 's';
    console.log(card.style.animationDelay);
    container.appendChild(card);
});