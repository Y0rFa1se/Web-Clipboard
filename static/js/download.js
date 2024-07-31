document.addEventListener('DOMContentLoaded', function() {
    var downloadForm = document.getElementById('download_form');
    if (downloadForm) {
        downloadForm.onsubmit = function(event) {
            event.preventDefault();
            
            var progressElement = document.getElementById('download_progress');
            var progressTextElement = document.getElementById('progress_text');
            
            var formData = new FormData(downloadForm);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', downloadForm.action, true);

            xhr.responseType = 'blob'; // 응답 유형을 Blob으로 설정

            xhr.onprogress = function(event) {
                if (event.lengthComputable) {
                    var percentComplete = (event.loaded / event.total) * 100;
                    progressElement.value = percentComplete;
                    progressTextElement.innerText = percentComplete.toFixed(2) + '%';
                }
            };

            xhr.onload = function() {
                if (xhr.status === 200) {
                    var blob = new Blob([xhr.response], { type: 'application/octet-stream' });
                    var url = window.URL.createObjectURL(blob);
                    
                    var a = document.createElement('a');
                    a.href = url;
                    a.download = 'downloaded_file'; // 다운로드할 파일명 설정
                    document.body.appendChild(a);
                    a.click();
                    
                    window.URL.revokeObjectURL(url);
                    
                    // 다운로드 후 페이지 리디렉션
                    setTimeout(function() {
                        window.location.href = '{{ url_for("test") }}';
                    }, 2000); // 2초 후 리디렉션
                } else {
                    alert('File download failed');
                }
            };

            xhr.send(formData);
        };
    } else {
        console.error('Download form with id "download_form" not found.');
    }
});
