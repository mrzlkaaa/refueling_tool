export default function dateStringFormatter(v){
    let date = new Date(v)
    return date.toDateString()
}