export function toggleBlock(e) {
    if (e.display == "block") {
        e.display = "none"
    } else {
        e.display = "block"
    }
}
export function dateStringFormatter(v){
    let date = new Date(v)
    return date.toDateString()
}
export function saveFile(data, filename="file.PDC") {
    const url = window.URL.createObjectURL(new Blob(data, {type: "text/plain; charset=utf-8"}))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${filename}`) //or any other extension
    document.body.appendChild(link)
    console.log("click")
    link.click()
}