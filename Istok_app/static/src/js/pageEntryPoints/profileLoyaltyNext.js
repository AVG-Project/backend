

document.addEventListener('DOMContentLoaded', function() {


    document.getElementById('loyalty__copy-link-btn').addEventListener('click', function() {
        const link = this.getAttribute('data-link');
        navigator.clipboard.writeText(link).then(function() {
        }, (error) => {
            console.error('Ошибка при копировании ссылки: ', error);
        });
    });
});