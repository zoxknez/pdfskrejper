// Main JavaScript fajl za PDF Scraper

$(document).ready(function() {
    console.log('PDF Scraper Web App loaded!');
    
    // Auto-hide alerts nakon 5 sekundi
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Tooltip inicijalizacija
    var tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Job Status Auto-Refresh
function startJobStatusMonitoring(jobId) {
    const interval = setInterval(function() {
        $.ajax({
            url: `/api/job/${jobId}/status`,
            method: 'GET',
            success: function(data) {
                updateJobStatus(data);
                
                // Zaustavi monitoring ako je job završen
                if (data.status === 'completed' || data.status === 'failed') {
                    clearInterval(interval);
                    location.reload(); // Reload stranicu
                }
            },
            error: function() {
                console.error('Failed to fetch job status');
                clearInterval(interval);
            }
        });
    }, 3000); // Proveri svake 3 sekunde
}

function updateJobStatus(data) {
    // Update progress bar
    if (data.progress !== undefined) {
        $('#jobProgress').css('width', data.progress + '%');
        $('#jobProgress').text(data.progress + '%');
    }
    
    // Update stats
    if (data.total_downloaded !== undefined) {
        $('#totalDownloaded').text(data.total_downloaded);
    }
    
    if (data.total_failed !== undefined) {
        $('#totalFailed').text(data.total_failed);
    }
    
    // Update status badge
    updateStatusBadge(data.status);
}

function updateStatusBadge(status) {
    const badge = $('#statusBadge');
    badge.removeClass('bg-primary bg-success bg-danger bg-secondary');
    
    switch(status) {
        case 'completed':
            badge.addClass('bg-success').html('<i class="bi bi-check-circle"></i> Završeno');
            break;
        case 'running':
            badge.addClass('bg-primary').html('<i class="bi bi-arrow-clockwise"></i> U toku');
            break;
        case 'failed':
            badge.addClass('bg-danger').html('<i class="bi bi-x-circle"></i> Neuspešno');
            break;
        default:
            badge.addClass('bg-secondary').html('<i class="bi bi-clock"></i> Na čekanju');
    }
}

// Confirm dialog za brisanje
function confirmDelete(message) {
    return confirm(message || 'Da li ste sigurni da želite da obrišete ovo?');
}

// Copy to clipboard funkcija
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Kopirano u clipboard!', 'success');
    }, function() {
        showToast('Greška pri kopiranju', 'error');
    });
}

// Toast notifikacije
function showToast(message, type = 'info') {
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    // Dodaj toast u container
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    container.innerHTML = toastHtml;
    const toast = new bootstrap.Toast(container.querySelector('.toast'));
    toast.show();
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('sr-RS') + ' ' + date.toLocaleTimeString('sr-RS');
}
