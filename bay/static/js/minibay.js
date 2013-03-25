if ($('#minibay-search').length) {
    $('input')[0].focus();
    $('input')[0].select();
}
if ($('#minibay-listen').length) {
    $('input')[0].focus();
    $('input')[0].select();
}

if ($('form.search').length) {
    $('form.search')[0].onsubmit = function() {
        window.location.href = '/bay/search/' + document.getElementById('q').value;
        return false;
    }
}
