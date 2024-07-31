document.addEventListener('DOMContentLoaded', function() {
    var fileUploadForm = document.getElementById('file_upload_form');
    if (fileUploadForm) {

        fileUploadForm.onsubmit = function(event) {
            event.preventDefault();
        
            var fileInput = document.getElementById('file_input');
            var file = fileInput.files[0];
            if (!file) {
                alert('Please select a file');
                return;
            }

            var formData = new FormData();
            formData.append('file', file);
            formData.append('title', document.querySelector('#file_upload_form input[name="title"]').value);
            formData.append('password', document.querySelector('#file_upload_form input[name="password"]').value);
        
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/file_add', true);
        
            xhr.upload.onprogress = function(event) {
                if (event.lengthComputable) {
                    var percentComplete = (event.loaded / event.total) * 100;
                    document.getElementById('upload_progress').value = percentComplete;
                    document.getElementById('progress_text').innerText = percentComplete.toFixed(2) + '%';
                }
            };

            xhr.onload = function() {
                if (xhr.status === 200) {
                    window.location.href = '/index';
                } else {
                    alert('File upload failed');
                }
            };
        
            xhr.send(formData);
        };
    } else {
        console.error('Form element with id "file_upload_form" not found.');
    }
});
