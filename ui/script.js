document.querySelector("#input_submit").onclick = function(e) {
    const file_inp = document.querySelector("#input_file")
    const image_out = document.querySelector("#output_image")
    const image_res = document.querySelector("#result_image")
    if (file_inp.files !== undefined && file_inp.files[0] !== undefined) {
        const file = file_inp.files[0]
        const type = file.type
        console.log(type)
        if (type == "image/jpeg" || type == "image/png") {
            image_out.file = file
            const reader = new FileReader();
            reader.onload = function(e) {
                image_out.src = e.target.result
                fetch('/detect', {
                    method: 'POST',
                    headers: {
                        "Content-Type": "text/base64"
                    },
                    body: e.target.result
                }).then((e) => e.text())
                  .then((e) => image_res.src = e)
            }
            reader.readAsDataURL(file)
        }
    }
}
