if ($('#minibay-search')) {
    $('input')[0].focus();
}
if ($('form.search')) {
    $('form.search')[0].onsubmit = function() {
        window.location.href = '/bay/search/' + document.getElementById('q').value;
        return false;
    }
}
