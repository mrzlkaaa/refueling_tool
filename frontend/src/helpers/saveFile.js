export default function saveFile(data, filename="file.PDC") {
    const url = window.URL.createObjectURL(new Blob(data, {type: "text/plain; charset=utf-8"}))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${filename}`) //or any other extension
    document.body.appendChild(link)
    console.log("preparing for download...")
    link.click()
}