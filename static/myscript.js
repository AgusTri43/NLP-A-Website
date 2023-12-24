// File: static/myscript.js

function summarizeText() {
    // Mendapatkan teks dari textarea
    var originalText = document.getElementById("text").value;

    // Menampilkan loader
    document.getElementById("loader").style.display = "block";

    // Mengirim permintaan AJAX ke server
    $.ajax({
        type: "POST",
        url: "/",
        data: { text: originalText },
        success: function(response) {
            // Menyembunyikan loader
            document.getElementById("loader").style.display = "none";

            // Menampilkan hasil summarization pada elemen dengan id "text_result"
            document.getElementById("text_result").innerHTML = "<strong>Original Text:</strong><br>" + originalText + "<br><br><strong>Summary:</strong><br>" + response;

            // (Opsional) Tambahkan logika atau tindakan lain setelah mendapatkan hasil
        },
        error: function(error) {
            // Menyembunyikan loader
            document.getElementById("loader").style.display = "none";

            // Menampilkan pesan kesalahan jika ada
            alert("Error occurred: " + error.responseText);
        }
    });
}