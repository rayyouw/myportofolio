document.addEventListener('submit', function (event) {
    const form = event.target.closest('form[data-loading-message]');
    if (!form) return;

    showToast(
        form.dataset.loadingTitle || 'Processing',
        form.dataset.loadingMessage,
        'normal',
        30000
    );
});
