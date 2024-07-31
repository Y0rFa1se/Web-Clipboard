function pbcopy() {
    var copy_txt = document.getElementById("copy_txt");

    copy_txt.select();
    copy_txt.setSelectionRange(0, 99999);

    // First try using navigator.clipboard.writeText
    navigator.clipboard.writeText(copy_txt.value)
        .then(() => {
            alert("Content copied");
        })
        .catch(err => {
            console.error('Failed to copy text with navigator.clipboard: ', err);
            // Fallback to document.execCommand('copy')
            try {
                document.execCommand('copy');
                alert("Content copied with execCommand");
            } catch (err) {
                console.error('Failed to copy text with execCommand: ', err);
                alert("Failed to copy content");
            }
        });
}
