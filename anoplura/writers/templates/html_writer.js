document.querySelector('thead')
    .addEventListener('click', function(event) {
        if (! event.target.matches('button')) { return; }
        const cls = event.target.classList;
        const trs = document.querySelectorAll('tr.term');
        const buttons = document.querySelectorAll('button.toggle');
        if (cls.contains('closed')) {
            trs.forEach(function(tr) {  tr.classList.remove('closed'); });
            buttons.forEach(function(b) {  b.classList.remove('closed'); });
        } else {
            trs.forEach(function(tr) {  tr.classList.add('closed'); });
            buttons.forEach(function(b) {  b.classList.add('closed'); });
        }
 });

 document.querySelector('tbody')
    .addEventListener('click', function(event) {
        if (! event.target.matches('button')) { return; }
        const taxonId = event.target.dataset.taxonId;
        const selector = `[data-taxon-id="${taxonId}"]`;
        const elts = document.querySelectorAll(selector);
        elts.forEach(function(tr) {  tr.classList.toggle('closed'); });
    });


function toggleColors() {
    for (let i = 0; i < 14; ++i) {
        document.querySelectorAll(`.c${i}`).forEach(function (span) {
            span.classList.toggle(`cc${i}`);
        });
        document.querySelectorAll(`.b${i}`).forEach(function (span) {
            span.classList.toggle(`bb${i}`);
        });
    }
}

document.querySelectorAll('input[type=radio]').forEach(function(item) {
    item.addEventListener('change', function(event) {
        toggleColors();
    });
});


document.querySelector('#by-part').checked = true;
